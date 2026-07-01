from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from binance_api import get_24h_ticker, get_klines, get_symbol_price, validate_symbol
from indicators import calculate_macd, calculate_rsi, combined_signal, macd_signal, rsi_signal

TOP_CRYPTO_PAIRS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "LTCUSDT",
    "XRPUSDT", "DOGEUSDT", "DOTUSDT", "TRXUSDT", "AVAXUSDT",
]

PERIODS = ["5m", "15m", "30m", "1h", "6h", "12h", "1d", "3d", "1w", "1M"]

st.set_page_config(page_title="Crypto RSI/MACD Analyzer", page_icon="📊", layout="wide")


@st.cache_data(ttl=60, show_spinner=False)
def load_klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    return get_klines(symbol, interval, limit)


@st.cache_data(ttl=30, show_spinner=False)
def load_price(symbol: str) -> float:
    return get_symbol_price(symbol)


@st.cache_data(ttl=30, show_spinner=False)
def load_24h(symbol: str) -> dict:
    return get_24h_ticker(symbol)


def analyze_period(symbol: str, interval: str, limit: int, rsi_buy: int, rsi_sell: int) -> dict:
    df = load_klines(symbol, interval, limit)
    rsi_series = calculate_rsi(df["close"])
    macd_df = calculate_macd(df["close"])

    rsi_value = float(rsi_series.iloc[-1])
    macd_value = float(macd_df["macd"].iloc[-1])
    signal_value = float(macd_df["signal"].iloc[-1])

    rsi_text = rsi_signal(rsi_value, rsi_buy, rsi_sell)
    macd_text = macd_signal(macd_value, signal_value)

    return {
        "Период": interval,
        "RSI": round(rsi_value, 2),
        "RSI сигнал": rsi_text,
        "MACD": round(macd_value, 6),
        "Signal line": round(signal_value, 6),
        "MACD сигнал": macd_text,
        "Итог": combined_signal(rsi_text, macd_text),
    }


def price_chart(symbol: str, interval: str, limit: int) -> go.Figure:
    df = load_klines(symbol, interval, limit).copy()
    rsi = calculate_rsi(df["close"])
    macd = calculate_macd(df["close"])

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df["open_time"], open=df["open"], high=df["high"], low=df["low"], close=df["close"],
        name="Цена",
    ))
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["close"].rolling(20).mean(), name="SMA 20"))
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["close"].rolling(50).mean(), name="SMA 50"))

    max_row = df.loc[df["close"].idxmax()]
    min_row = df.loc[df["close"].idxmin()]
    fig.add_annotation(x=max_row["open_time"], y=max_row["close"], text=f"Max {max_row['close']:.2f}", showarrow=True)
    fig.add_annotation(x=min_row["open_time"], y=min_row["close"], text=f"Min {min_row['close']:.2f}", showarrow=True)

    fig.update_layout(
        title=f"{symbol}: график цены",
        xaxis_title="Дата",
        yaxis_title="Цена",
        height=650,
        xaxis_rangeslider_visible=False,
    )
    return fig


def main() -> None:
    st.title("📊 Crypto RSI/MACD Analyzer")
    st.caption("Streamlit-версия твоего Telegram-бота: Binance price data, RSI, MACD и сигналы по таймфреймам.")

    with st.sidebar:
        st.header("Настройки")
        mode = st.radio("Выбор пары", ["Топ пары", "Ввести вручную"])
        if mode == "Топ пары":
            symbol = st.selectbox("Пара", TOP_CRYPTO_PAIRS, index=0)
        else:
            symbol = st.text_input("Пара Binance", value="BTCUSDT").upper().strip()

        selected_periods = st.multiselect("Таймфреймы для анализа", PERIODS, default=["15m", "1h", "6h", "1d", "1w"])
        chart_interval = st.selectbox("Таймфрейм графика", PERIODS, index=6)
        candles_limit = st.slider("Количество свечей", min_value=60, max_value=500, value=200, step=20)

        st.divider()
        rsi_buy = st.slider("RSI покупка ниже", 10, 50, 40)
        rsi_sell = st.slider("RSI продажа выше", 50, 90, 70)
        run = st.button("🚀 Анализировать", use_container_width=True)

    if not symbol:
        st.warning("Введите торговую пару, например BTCUSDT.")
        return

    if run:
        st.cache_data.clear()

    try:
        if not validate_symbol(symbol):
            st.error(f"Пара {symbol} не найдена на Binance.")
            return

        price = load_price(symbol)
        ticker = load_24h(symbol)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Текущая цена", f"{price:,.6f} USDT")
        col2.metric("24h изменение", f"{ticker['price_change_percent']:.2f}%")
        col3.metric("24h High", f"{ticker['high_price']:,.6f}")
        col4.metric("24h Low", f"{ticker['low_price']:,.6f}")

        if not selected_periods:
            st.warning("Выбери хотя бы один таймфрейм для анализа.")
            return

        with st.spinner("Загружаю данные и считаю индикаторы..."):
            rows = [analyze_period(symbol, period, candles_limit, rsi_buy, rsi_sell) for period in selected_periods]
            result_df = pd.DataFrame(rows)

        st.subheader("Сигналы по таймфреймам")
        st.dataframe(result_df, use_container_width=True, hide_index=True)

        st.subheader("График")
        st.plotly_chart(price_chart(symbol, chart_interval, candles_limit), use_container_width=True)

        with st.expander("Пояснение логики"):
            st.markdown(
                f"""
                - **RSI ниже {rsi_buy}** → возможная перепроданность / сигнал в сторону покупки.  
                - **RSI выше {rsi_sell}** → возможная перекупленность / сигнал в сторону продажи.  
                - **MACD выше сигнальной линии** → бычий импульс.  
                - **MACD ниже сигнальной линии** → медвежий импульс.  

                Это не финансовая рекомендация. Индикаторы лучше использовать вместе с уровнем риска, трендом, объемами и новостями.
                """
            )

    except Exception as exc:
        st.error("Ошибка при получении или обработке данных.")
        st.code(str(exc))


if __name__ == "__main__":
    main()
