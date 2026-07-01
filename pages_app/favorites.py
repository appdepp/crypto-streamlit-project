from __future__ import annotations

import pandas as pd
import streamlit as st
from components.layout import chips, scan_cards, section
from services.binance import get_klines
from services.indicators import add_indicators
from services.scoring import score_market


def render(favorites: list[str], interval: str):
    section("Favorites", "Твои быстрые монеты для ежедневного контроля.")
    chips(favorites)
    remove = st.selectbox("Удалить из избранного", [""] + favorites)
    if st.button("Удалить", use_container_width=True) and remove:
        st.session_state.favorites = [x for x in favorites if x != remove]
        st.rerun()
    rows = []
    for s in favorites:
        try:
            df = add_indicators(get_klines(s, interval, 300))
            sc = score_market(df)
            rows.append({"symbol": s, "price": sc["price"], "signal": sc["signal"], "score": sc["total"], "rsi": round(sc["rsi"], 1), "adx": round(sc["adx"], 1)})
        except Exception:
            pass
    if rows:
        result = pd.DataFrame(rows).sort_values("score", ascending=False)
        scan_cards(result)
        with st.expander("Таблица"):
            st.dataframe(result, use_container_width=True, hide_index=True)
