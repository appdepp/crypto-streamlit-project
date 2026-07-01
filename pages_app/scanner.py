from __future__ import annotations

import streamlit as st

from config import DEFAULT_SYMBOLS, INTERVALS
from components.ui import render_scan_cards
from services.binance import normalize_symbol
from services.scoring import run_scanner, top_symbols


def render(state: dict) -> None:
    s1, s2, s3 = st.columns(3)
    source = s1.selectbox("Universe", ["Top Binance volume", "Default list", "Favorites", "Custom"])
    count = s2.slider("Pairs", 5, 50, 20, 5)
    mode = s3.selectbox("Mode", ["Single TF", "Multi TF"])

    if source == "Top Binance volume":
        symbols = top_symbols(count)
    elif source == "Favorites":
        symbols = st.session_state.favorites[:count]
    elif source == "Custom":
        raw = st.text_area("Pairs", "BTCUSDT, ETHUSDT, SOLUSDT")
        symbols = [normalize_symbol(item) for item in raw.replace("\n", ",").split(",") if normalize_symbol(item)][:count]
    else:
        symbols = DEFAULT_SYMBOLS[:count]

    if mode == "Single TF":
        intervals = [st.selectbox("Scan timeframe", INTERVALS, index=INTERVALS.index(state["interval"]))]
        multi = False
    else:
        intervals = st.multiselect("Scan timeframes", INTERVALS, default=["15m", "1h", "4h", "1d"])
        intervals = intervals or ["1h"]
        multi = True

    if st.button("Run scanner", type="primary", use_container_width=True):
        progress = st.progress(0)
        st.session_state.scan_result = run_scanner(symbols, intervals, min(int(state["limit"]), 500), multi, progress)
        progress.empty()

    if "scan_result" in st.session_state:
        render_scan_cards(st.session_state.scan_result.head(40))
        with st.expander("Table", expanded=False):
            st.dataframe(st.session_state.scan_result, use_container_width=True, hide_index=True)
