from __future__ import annotations

import pandas as pd
import streamlit as st

from config import APP_TITLE, INTERVALS
from components.theme import inject_css
from components.ui import render_topbar
from services.binance import clear_market_cache, normalize_symbol
from pages_app import chart, dashboard, favorites, heatmap, multi_tf, portfolio, scanner, settings

st.set_page_config(page_title=APP_TITLE, page_icon="📈", layout="wide", initial_sidebar_state="expanded")
inject_css()

if "favorites" not in st.session_state:
    st.session_state.favorites = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["symbol", "amount", "buy_price"])
if "symbol" not in st.session_state:
    st.session_state.symbol = "BTCUSDT"
if "interval" not in st.session_state:
    st.session_state.interval = "1h"
if "limit" not in st.session_state:
    st.session_state.limit = 500

render_topbar()

with st.sidebar:
    st.subheader("Controls")
    st.session_state.symbol = normalize_symbol(st.text_input("Pair", st.session_state.symbol))
    st.session_state.interval = st.selectbox("Timeframe", INTERVALS, index=INTERVALS.index(st.session_state.interval))
    st.session_state.limit = st.slider("Candles", 120, 1000, int(st.session_state.limit), step=40)
    if st.button("Refresh data", use_container_width=True):
        clear_market_cache()
        st.success("Refreshed")
    st.caption("Sidebar is optional. Main controls are duplicated inside pages.")

page = st.radio(
    "Navigation",
    ["Dashboard", "Chart", "Multi TF", "Scanner", "Heatmap", "Favorites", "Portfolio", "Settings"],
    horizontal=True,
    label_visibility="collapsed",
)

state = {
    "symbol": st.session_state.symbol,
    "interval": st.session_state.interval,
    "limit": int(st.session_state.limit),
}

if page == "Dashboard":
    dashboard.render(state)
elif page == "Chart":
    chart.render(state)
elif page == "Multi TF":
    multi_tf.render(state)
elif page == "Scanner":
    scanner.render(state)
elif page == "Heatmap":
    heatmap.render(state)
elif page == "Favorites":
    favorites.render(state)
elif page == "Portfolio":
    portfolio.render(state)
else:
    settings.render(state)
