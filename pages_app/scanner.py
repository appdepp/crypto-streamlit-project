from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from config import DEFAULT_SYMBOLS, SCANNER_TIMEFRAMES
from components.layout import scan_cards, section
from pages_app.multi_tf import analyze_symbol_timeframes
from services.binance import get_24h_tickers, get_klines
from services.indicators import add_indicators
from services.scoring import score_market


def _bias(avg: int) -> str:
    if avg >= 82:
        return "Strong Buy"
    if avg >= 66:
        return "Buy"
    if avg <= 28:
        return "Strong Sell"
    if avg <= 42:
        return "Sell"
    return "Neutral"


def render(favorites: list[str], selected_timeframes: list[str]):
    section("Market scanner", "Top-пары, карточки и таблица")
    scan_count = st.slider("Монет", 5, 60, 20)
    mode = st.radio("Режим", ["Один таймфрейм", "Несколько таймфреймов"], horizontal=True)
    scan_interval = st.selectbox("Таймфрейм", ["15m", "1h", "4h", "1d"], index=2)
    scan_tfs = st.multiselect("Таймфреймы сканера", SCANNER_TIMEFRAMES, default=[tf for tf in selected_timeframes if tf in SCANNER_TIMEFRAMES] or SCANNER_TIMEFRAMES)
    source = st.radio("Пары", ["Top Binance volume", "Default list", "Favorites"], horizontal=True)
    if st.button("Запустить сканер", type="primary", use_container_width=True):
        if source == "Top Binance volume":
            tickers = get_24h_tickers().head(scan_count)
            symbols = tickers["symbol"].tolist()
            changes = dict(zip(tickers["symbol"], tickers["priceChangePercent"]))
        elif source == "Favorites":
            symbols = favorites[:scan_count]
            changes = {}
        else:
            symbols = DEFAULT_SYMBOLS[:scan_count]
            changes = {}
        rows = []
        progress = st.progress(0)
        for i, s in enumerate(symbols):
            try:
                if mode == "Несколько таймфреймов":
                    tf_rows, avg, bias = analyze_symbol_timeframes(s, scan_tfs or SCANNER_TIMEFRAMES, 300)
                    last = tf_rows[-1]
                    rows.append({"symbol": s, "signal": bias, "score": avg, "price": last["price"], "rsi": last["rsi"], "adx": last["adx"], "timeframes": " / ".join([f"{r['timeframe']}:{r['score']}" for r in tf_rows]), "change": changes.get(s, "")})
                else:
                    df = add_indicators(get_klines(s, scan_interval, 300))
                    sc = score_market(df)
                    rows.append({"symbol": s, "signal": sc["signal"], "score": sc["total"], "trend": sc["trend"], "momentum": sc["momentum"], "rsi": round(sc["rsi"], 1), "adx": round(sc["adx"], 1), "price": sc["price"], "change": changes.get(s, "")})
            except Exception:
                rows.append({"symbol": s, "signal": "Error", "score": 0, "rsi": "—", "adx": "—", "price": None, "change": changes.get(s, "")})
            progress.progress((i + 1) / max(1, len(symbols)))
        st.session_state.last_scan = pd.DataFrame(rows).sort_values("score", ascending=False)
    result = st.session_state.get("last_scan")
    if result is not None and not result.empty:
        scan_cards(result.head(20))
        with st.expander("Таблица"):
            st.dataframe(result, use_container_width=True, hide_index=True)
            fig = px.bar(result.head(25), x="symbol", y="score", color="signal", title=None, template="plotly_dark")
            fig.update_layout(height=360, margin=dict(l=4, r=4, t=10, b=4), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
