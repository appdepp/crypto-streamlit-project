from __future__ import annotations

import plotly.express as px
import streamlit as st
from services.binance import get_24h_tickers


def render():
    st.subheader("Market heatmap")
    tickers = get_24h_tickers().head(70)
    fig = px.treemap(
        tickers,
        path=["symbol"],
        values="quoteVolume",
        color="priceChangePercent",
        color_continuous_scale="RdYlGn",
        title="USDT market heatmap · size = volume, color = 24h %",
    )
    fig.update_layout(template="plotly_dark", height=650, margin=dict(l=5, r=5, t=45, b=5), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
