from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from config import DEFAULT_SYMBOLS
from services.binance import get_24h_tickers, get_klines
from services.indicators import add_indicators
from services.scoring import score_market


def render(favorites: list[str]):
    st.subheader("Market scanner")
    st.caption("Сканирует USDT-пары и считает общий рейтинг.")
    scan_count = st.slider("Сколько монет сканировать", 5, 60, 20)
    scan_interval = st.selectbox("Таймфрейм сканера", ["15m", "1h", "4h", "1d"], index=2)
    source = st.radio("Источник", ["Top Binance volume", "Default list", "Favorites"], horizontal=True)
    if st.button("Запустить сканер", type="primary", use_container_width=True):
        if source == "Top Binance volume":
            symbols = get_24h_tickers().head(scan_count)["symbol"].tolist()
        elif source == "Favorites":
            symbols = favorites[:scan_count]
        else:
            symbols = DEFAULT_SYMBOLS[:scan_count]
        rows = []
        progress = st.progress(0)
        for i, s in enumerate(symbols):
            try:
                df = add_indicators(get_klines(s, scan_interval, 300))
                sc = score_market(df)
                rows.append({"symbol": s, "signal": sc["signal"], "score": sc["total"], "trend": sc["trend"], "momentum": sc["momentum"], "rsi": round(sc["rsi"], 1), "adx": round(sc["adx"], 1), "price": sc["price"]})
            except Exception:
                rows.append({"symbol": s, "signal": "Error", "score": 0, "trend": 0, "momentum": 0, "rsi": None, "adx": None, "price": None})
            progress.progress((i + 1) / max(1, len(symbols)))
        result = pd.DataFrame(rows).sort_values("score", ascending=False)
        st.dataframe(result, use_container_width=True, hide_index=True)
        fig = px.bar(result, x="symbol", y="score", color="signal", title="Scanner score", template="plotly_dark")
        fig.update_layout(height=420, margin=dict(l=8, r=8, t=45, b=8), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
