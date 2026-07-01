from __future__ import annotations

import plotly.express as px
import streamlit as st

from config import INTERVALS
from components.ui import price_fmt, render_asset_card
from services.binance import get_24h_tickers, normalize_symbol
from services.scoring import load_symbol, score_market


def render(state: dict) -> None:
    c1, c2, c3 = st.columns([1.2, 1, 1])
    symbol = normalize_symbol(c1.text_input("Pair", state["symbol"], key="dash_symbol"))
    interval = c2.selectbox("Timeframe", INTERVALS, index=INTERVALS.index(state["interval"]), key="dash_interval")
    if c3.button("Add favorite", use_container_width=True) and symbol not in st.session_state.favorites:
        st.session_state.favorites.append(symbol)
    st.session_state.symbol = symbol
    st.session_state.interval = interval

    try:
        df = load_symbol(symbol, interval, state["limit"])
        score = score_market(df)
        tickers = get_24h_tickers()
        row = tickers[tickers.symbol == symbol]
        render_asset_card(symbol, score, None if row.empty else row.iloc[0].priceChangePercent)

        cols = st.columns(6)
        for col, (_, ticker) in zip(cols, tickers.head(6).iterrows()):
            col.metric(ticker.symbol.replace("USDT", ""), price_fmt(ticker.lastPrice), f"{ticker.priceChangePercent:+.2f}%")

        fig = px.bar(tickers.head(20).sort_values("priceChangePercent"), x="priceChangePercent", y="symbol", orientation="h", template="plotly_dark")
        fig.update_layout(height=520, margin=dict(l=4, r=4, t=10, b=4), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as exc:
        st.error(f"Dashboard error: {exc}")
