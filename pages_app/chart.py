from __future__ import annotations

import pandas as pd
import streamlit as st
from components.charts import candlestick_chart, gauge
from components.layout import signal_badge
from services.binance import get_klines
from services.indicators import add_indicators
from services.scoring import score_market


def render(symbol: str, interval: str, limit: int, show_ema: bool, show_bb: bool):
    st.subheader(f"Chart · {symbol}")
    df = add_indicators(get_klines(symbol, interval, limit))
    score = score_market(df)
    st.markdown(f"Сигнал: {signal_badge(score['signal'], score['total'])}", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Price", f"${score['price']:,.4g}")
    c2.metric("Total", f"{score['total']}/100", score["signal"])
    c3.metric("RSI", f"{score['rsi']:.1f}")
    c4.metric("ADX", f"{score['adx']:.1f}")
    g1, g2, g3, g4 = st.columns(4)
    g1.plotly_chart(gauge(score["trend"], "Trend", compact=True), use_container_width=True)
    g2.plotly_chart(gauge(score["momentum"], "Momentum", compact=True), use_container_width=True)
    g3.plotly_chart(gauge(score["volume"], "Volume", compact=True), use_container_width=True)
    g4.plotly_chart(gauge(score["total"], "Total", compact=True), use_container_width=True)
    st.plotly_chart(candlestick_chart(df, symbol, show_ema, show_bb, compact=True), use_container_width=True)
    latest = df.dropna().iloc[-1]
    st.caption("Последние значения индикаторов")
    st.dataframe(pd.DataFrame([{
        "price": latest["close"], "rsi": latest["rsi"], "macd": latest["macd"], "macd_signal": latest["macd_signal"],
        "adx": latest["adx"], "atr": latest["atr"], "ema20": latest["ema20"], "ema50": latest["ema50"], "ema200": latest["ema200"],
    }]), use_container_width=True, hide_index=True)
