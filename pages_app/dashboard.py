from __future__ import annotations

import plotly.express as px
import streamlit as st
from components.layout import format_price, mini_metrics, section
from services.binance import get_24h_tickers


def render():
    section("Market overview", "Самые ликвидные USDT-пары Binance за 24 часа.")
    tickers = get_24h_tickers().head(100)
    top = tickers.head(4)
    items = []
    for _, row in top.iterrows():
        delta = f"{row['priceChangePercent']:.2f}%"
        items.append((row["symbol"], format_price(row["lastPrice"]), delta))
    mini_metrics(items)
    section("24h movers")
    fig = px.bar(tickers.head(25), x="symbol", y="priceChangePercent", title=None, template="plotly_dark")
    fig.update_layout(height=360, margin=dict(l=4, r=4, t=10, b=4), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with st.expander("Таблица рынка"):
        st.dataframe(tickers[["symbol", "lastPrice", "priceChangePercent", "quoteVolume"]].head(40), use_container_width=True, hide_index=True)
