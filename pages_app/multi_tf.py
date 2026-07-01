from __future__ import annotations

import streamlit as st

from config import INTERVALS
from components.ui import badge_html, render_scan_cards
from services.binance import normalize_symbol
from services.scoring import aggregate_signal, multi_timeframe


def render(state: dict) -> None:
    c1, c2 = st.columns([1, 1.4])
    symbol = normalize_symbol(c1.text_input("Pair", state["symbol"], key="mtf_symbol"))
    intervals = c2.multiselect("Timeframes", INTERVALS, default=["5m", "15m", "1h", "4h", "1d"])
    intervals = intervals or ["1h"]
    st.session_state.symbol = symbol

    try:
        df = multi_timeframe(symbol, intervals, min(int(state["limit"]), 500))
        valid = df[df.signal != "Error"]
        avg = int(valid.score.mean()) if not valid.empty else 0
        signal = aggregate_signal(avg)
        st.markdown(
            f"<div class='asset'><div class='asset-row'><div><div class='sym'>{symbol}</div><div class='price'>{avg}</div><div class='muted'>Multi-timeframe score</div></div><div>{badge_html(signal)}</div></div></div>",
            unsafe_allow_html=True,
        )
        render_scan_cards(df.rename(columns={"timeframe": "symbol"}), "symbol")
        with st.expander("Table", expanded=True):
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as exc:
        st.error(f"Multi TF error: {exc}")
