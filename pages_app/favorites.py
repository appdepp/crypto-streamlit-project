from __future__ import annotations

import streamlit as st

from components.ui import render_pills, render_scan_cards
from services.binance import normalize_symbol
from services.scoring import run_scanner


def render(state: dict) -> None:
    a, b = st.columns(2)
    add = normalize_symbol(a.text_input("Add pair", state["symbol"], key="fav_add"))
    if b.button("Add", use_container_width=True) and add not in st.session_state.favorites:
        st.session_state.favorites.append(add)
        st.rerun()

    render_pills(st.session_state.favorites)
    remove = st.selectbox("Remove", [""] + st.session_state.favorites)
    if st.button("Remove selected") and remove:
        st.session_state.favorites = [item for item in st.session_state.favorites if item != remove]
        st.rerun()
    if st.session_state.favorites:
        result = run_scanner(st.session_state.favorites, [state["interval"]], min(int(state["limit"]), 400), False)
        render_scan_cards(result)
