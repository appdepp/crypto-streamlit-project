from __future__ import annotations

import plotly.express as px
import streamlit as st

from services.binance import get_24h_tickers


def render(state: dict) -> None:
    try:
        count = st.slider("Pairs", 20, 100, 60, 10)
        tickers = get_24h_tickers().head(count)
        fig = px.treemap(tickers, path=["symbol"], values="quoteVolume", color="priceChangePercent", color_continuous_scale="RdYlGn")
        fig.update_layout(template="plotly_dark", height=720, margin=dict(l=4, r=4, t=8, b=4), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as exc:
        st.error(f"Heatmap error: {exc}")
