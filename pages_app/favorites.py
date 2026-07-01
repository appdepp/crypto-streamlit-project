from __future__ import annotations

import pandas as pd
import streamlit as st
from components.layout import chips
from services.binance import get_klines
from services.indicators import add_indicators
from services.scoring import score_market


def render(favorites: list[str], interval: str):
    st.subheader("Favorites")
    chips(favorites)
    remove = st.selectbox("Удалить из избранного", [""] + favorites)
    if st.button("Удалить", use_container_width=True) and remove:
        st.session_state.favorites = [x for x in favorites if x != remove]
        st.rerun()
    rows = []
    for s in favorites:
        try:
            sc = score_market(add_indicators(get_klines(s, interval, 300)))
            rows.append({"symbol": s, "price": sc["price"], "signal": sc["signal"], "score": sc["total"], "rsi": round(sc["rsi"], 1), "adx": round(sc["adx"], 1)})
        except Exception:
            pass
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
