from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from binance_api import BinanceDataError, get_24h_tickers, get_klines, get_server_time
from config import APP_TITLE, DEFAULT_SYMBOLS, INTERVALS
from indicators import add_indicators, score_market
from ui import candlestick_chart, gauge, inject_css, signal_class

st.set_page_config(page_title=APP_TITLE, page_icon="📈", layout="wide")
inject_css()

if "favorites" not in st.session_state:
    st.session_state.favorites = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["symbol", "amount", "buy_price"])


def load_symbol(symbol: str, interval: str, limit: int):
    df = get_klines(symbol, interval, limit)
    return add_indicators(df)


def render_score_cards(score: dict):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total score", f"{score['total']}/100", score["signal"])
    c2.metric("Trend", f"{score['trend']}/100")
    c3.metric("Momentum", f"{score['momentum']}/100")
    c4.metric("Volume", f"{score['volume']}/100")
    c5.metric("ADX", f"{score['adx']:.1f}")


with st.sidebar:
    st.title("⚡ Crypto Terminal")
    st.caption("Binance public market data · Streamlit Cloud ready")
    symbol = st.text_input("Пара", value="BTCUSDT").upper().replace("/", "").strip()
    interval = st.selectbox("Таймфрейм", INTERVALS, index=5)
    limit = st.slider("Количество свечей", 100, 1000, 500, step=50)
    show_ema = st.toggle("EMA 20/50/200", value=True)
    show_bb = st.toggle("Bollinger Bands", value=True)
    st.divider()
    if st.button("⭐ Добавить в избранное", use_container_width=True):
        if symbol and symbol not in st.session_state.favorites:
            st.session_state.favorites.append(symbol)
            st.success(f"{symbol} добавлена")
    st.caption(f"Binance server time: {get_server_time()}")

st.title("📈 Crypto Terminal 2.0")
st.caption("Терминал для быстрого анализа крипторынка: свечи, индикаторы, скоринг, сканер, heatmap и портфель.")

tabs = st.tabs(["📊 Dashboard", "🕯️ Chart", "🔎 Scanner", "🔥 Heatmap", "⭐ Favorites", "💼 Portfolio", "⚙️ Settings"])

with tabs[0]:
    st.subheader("Market overview")
    try:
        tickers = get_24h_tickers().head(100)
        top = tickers.head(4)
        cols = st.columns(4)
        for col, (_, row) in zip(cols, top.iterrows()):
            col.metric(row["symbol"], f"${row['lastPrice']:,.4g}", f"{row['priceChangePercent']:.2f}%")

        c1, c2 = st.columns([1.2, 1])
        with c1:
            chart_df = tickers.head(25).copy()
            fig = px.bar(chart_df, x="symbol", y="priceChangePercent", title="Top 25 by volume · 24h %", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.dataframe(
                tickers[["symbol", "lastPrice", "priceChangePercent", "quoteVolume"]].head(30),
                use_container_width=True,
                hide_index=True,
            )
    except Exception as exc:
        st.error(f"Не удалось загрузить обзор рынка: {exc}")

with tabs[1]:
    st.subheader(f"Chart · {symbol}")
    try:
        df = load_symbol(symbol, interval, limit)
        score = score_market(df)
        st.markdown(f"Сигнал: <span class='{signal_class(score['signal'])}'>{score['signal']}</span>", unsafe_allow_html=True)
        render_score_cards(score)
        g1, g2, g3, g4 = st.columns(4)
        g1.plotly_chart(gauge(score["trend"], "Trend"), use_container_width=True)
        g2.plotly_chart(gauge(score["momentum"], "Momentum"), use_container_width=True)
        g3.plotly_chart(gauge(score["volume"], "Volume"), use_container_width=True)
        g4.plotly_chart(gauge(score["total"], "Total"), use_container_width=True)
        st.plotly_chart(candlestick_chart(df, symbol, show_ema, show_bb), use_container_width=True)

        latest = df.dropna().iloc[-1]
        st.write("Последние значения индикаторов")
        st.dataframe(pd.DataFrame([{
            "price": latest["close"], "rsi": latest["rsi"], "macd": latest["macd"],
            "macd_signal": latest["macd_signal"], "adx": latest["adx"], "atr": latest["atr"],
            "ema20": latest["ema20"], "ema50": latest["ema50"], "ema200": latest["ema200"],
        }]), use_container_width=True, hide_index=True)
    except BinanceDataError as exc:
        st.error(str(exc))
        st.info("Для Streamlit Cloud использован data-api.binance.vision. Если Binance снова блокирует IP, можно подключить альтернативный источник данных.")
    except Exception as exc:
        st.exception(exc)

with tabs[2]:
    st.subheader("Market scanner")
    st.caption("Сканирует выбранные USDT-пары и считает общий рейтинг по тренду, momentum, объёму и волатильности.")
    scan_count = st.slider("Сколько монет сканировать", 5, 50, 20, key="scan_count")
    scan_interval = st.selectbox("Таймфрейм сканера", ["15m", "1h", "4h", "1d"], index=2)
    source = st.radio("Источник списка", ["Top Binance volume", "Default list", "Favorites"], horizontal=True)
    if st.button("Запустить сканер", type="primary"):
        rows = []
        progress = st.progress(0)
        if source == "Top Binance volume":
            symbols = get_24h_tickers().head(scan_count)["symbol"].tolist()
        elif source == "Favorites":
            symbols = st.session_state.favorites[:scan_count]
        else:
            symbols = DEFAULT_SYMBOLS[:scan_count]
        for i, s in enumerate(symbols):
            try:
                d = load_symbol(s, scan_interval, 300)
                sc = score_market(d)
                rows.append({"symbol": s, "signal": sc["signal"], "score": sc["total"], "trend": sc["trend"], "momentum": sc["momentum"], "rsi": round(sc["rsi"], 1), "adx": round(sc["adx"], 1), "price": sc["price"]})
            except Exception as exc:
                rows.append({"symbol": s, "signal": "Error", "score": 0, "trend": 0, "momentum": 0, "rsi": None, "adx": None, "price": None})
            progress.progress((i + 1) / len(symbols))
        result = pd.DataFrame(rows).sort_values("score", ascending=False)
        st.dataframe(result, use_container_width=True, hide_index=True)
        fig = px.bar(result, x="symbol", y="score", color="signal", title="Scanner score", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("Market heatmap")
    try:
        tickers = get_24h_tickers().head(60)
        fig = px.treemap(
            tickers,
            path=["symbol"],
            values="quoteVolume",
            color="priceChangePercent",
            color_continuous_scale="RdYlGn",
            title="USDT market heatmap · size = volume, color = 24h %",
        )
        fig.update_layout(template="plotly_dark", height=720)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as exc:
        st.error(f"Heatmap недоступна: {exc}")

with tabs[4]:
    st.subheader("Favorites")
    st.write(st.session_state.favorites)
    remove = st.selectbox("Удалить из избранного", [""] + st.session_state.favorites)
    if st.button("Удалить") and remove:
        st.session_state.favorites = [x for x in st.session_state.favorites if x != remove]
        st.rerun()
    if st.session_state.favorites:
        fav_rows = []
        for s in st.session_state.favorites:
            try:
                d = load_symbol(s, interval, 300)
                sc = score_market(d)
                fav_rows.append({"symbol": s, "price": sc["price"], "signal": sc["signal"], "score": sc["total"], "rsi": round(sc["rsi"], 1), "adx": round(sc["adx"], 1)})
            except Exception:
                pass
        st.dataframe(pd.DataFrame(fav_rows), use_container_width=True, hide_index=True)

with tabs[5]:
    st.subheader("Virtual portfolio")
    st.caption("Локальный демо-портфель. Данные хранятся в session_state, после перезапуска браузера могут сброситься.")
    c1, c2, c3 = st.columns(3)
    p_symbol = c1.text_input("Symbol", "BTCUSDT", key="p_symbol").upper().strip()
    amount = c2.number_input("Amount", min_value=0.0, value=0.01, step=0.01, format="%.8f")
    buy_price = c3.number_input("Buy price", min_value=0.0, value=50000.0, step=100.0)
    if st.button("Добавить позицию"):
        new = pd.DataFrame([{"symbol": p_symbol, "amount": amount, "buy_price": buy_price}])
        st.session_state.portfolio = pd.concat([st.session_state.portfolio, new], ignore_index=True)
    if not st.session_state.portfolio.empty:
        pf = st.session_state.portfolio.copy()
        current_prices = []
        for s in pf["symbol"]:
            try:
                current_prices.append(float(load_symbol(s, "1h", 100).iloc[-1]["close"]))
            except Exception:
                current_prices.append(None)
        pf["current_price"] = current_prices
        pf["cost"] = pf["amount"] * pf["buy_price"]
        pf["value"] = pf["amount"] * pf["current_price"]
        pf["pnl"] = pf["value"] - pf["cost"]
        pf["pnl_%"] = pf["pnl"] / pf["cost"] * 100
        st.metric("Portfolio value", f"${pf['value'].sum():,.2f}", f"${pf['pnl'].sum():,.2f}")
        st.dataframe(pf, use_container_width=True, hide_index=True)
        fig = px.pie(pf, values="value", names="symbol", title="Allocation", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Очистить портфель"):
            st.session_state.portfolio = st.session_state.portfolio.iloc[0:0]
            st.rerun()
    else:
        st.info("Добавь первую позицию выше.")

with tabs[6]:
    st.subheader("Settings / README")
    st.markdown("""
    **Как обновлять приложение:** измени файлы → `git add .` → `git commit -m "..."` → `git push`.

    **Важно:** сигналы — это аналитический скоринг, а не финансовая рекомендация. Для реальной торговли нужно добавить риск-менеджмент, бэктесты и проверку стратегии.
    """)
