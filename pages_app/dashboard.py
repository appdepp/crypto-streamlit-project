from __future__ import annotations

import plotly.express as px
import streamlit as st
from services.binance import get_24h_tickers


def render():
    st.subheader("Market overview")
    tickers = get_24h_tickers().head(100)
    top = tickers.head(4)
    cols = st.columns(4)
    for col, (_, row) in zip(cols, top.iterrows()):
        col.metric(row["symbol"], f"${row['lastPrice']:,.4g}", f"{row['priceChangePercent']:.2f}%")
    c1, c2 = st.columns([1.25, 1])
    with c1:
        fig = px.bar(tickers.head(25), x="symbol", y="priceChangePercent", title="Top 25 by volume · 24h %", template="plotly_dark")
        fig.update_layout(height=420, margin=dict(l=8, r=8, t=45, b=8), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.dataframe(tickers[["symbol", "lastPrice", "priceChangePercent", "quoteVolume"]].head(30), use_container_width=True, hide_index=True)
