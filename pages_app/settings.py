from __future__ import annotations

import streamlit as st

from services.binance import clear_market_cache


def render(state: dict) -> None:
    st.subheader("Settings")
    if st.button("Refresh market data", use_container_width=True):
        clear_market_cache()
        st.success("Market data cache cleared")
    st.markdown("""
    **Navigation** is always visible at the top. Sidebar is optional and only duplicates main controls.

    **Signals** are analytical scores, not financial advice.
    """)
