from __future__ import annotations

import streamlit as st

from config import INTERVALS
from components.charts import candlestick_chart
from components.ui import render_asset_card
from services.binance import normalize_symbol
from services.scoring import load_symbol, score_market


def render(state: dict) -> None:
    a, b, c = st.columns([1.2, .8, .8])
    symbol = normalize_symbol(a.text_input("Pair", state["symbol"], key="chart_symbol"))
    interval = b.selectbox("Timeframe", INTERVALS, index=INTERVALS.index(state["interval"]), key="chart_interval")
    limit = c.slider("Candles", 120, 1000, int(state["limit"]), 40, key="chart_limit")
    st.session_state.symbol = symbol
    st.session_state.interval = interval
    st.session_state.limit = limit

    with st.expander("Indicators", expanded=False):
        cols = st.columns(5)
        show_ema = cols[0].toggle("EMA", True)
        show_bb = cols[1].toggle("Bollinger", False)
        show_volume = cols[2].toggle("Volume", True)
        show_rsi = cols[3].toggle("RSI", True)
        show_macd = cols[4].toggle("MACD", True)
    try:
        df = load_symbol(symbol, interval, limit)
        score = score_market(df)
        render_asset_card(symbol, score)
        st.plotly_chart(candlestick_chart(df, show_ema, show_bb, show_volume, show_rsi, show_macd), use_container_width=True)
        with st.expander("Indicator values", expanded=False):
            cols = ["close", "rsi", "macd", "macd_signal", "adx", "atr", "ema20", "ema50", "ema200"]
            st.dataframe(df.dropna().tail(1)[cols], use_container_width=True, hide_index=True)
    except Exception as exc:
        st.error(f"Chart error: {exc}")
