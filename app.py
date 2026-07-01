from __future__ import annotations

import pandas as pd
import streamlit as st

from components.layout import app_top, top_nav
from components.theme import inject_css
from config import APP_ICON, APP_TITLE, CORE_TIMEFRAMES, DEFAULT_SYMBOL, INTERVALS
from pages_app import chart, dashboard, favorites, heatmap, multi_tf, portfolio, scanner, settings
from services.binance import BinanceDataError

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide", initial_sidebar_state="expanded")
inject_css()

if "favorites" not in st.session_state:
    st.session_state.favorites = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["symbol", "amount", "buy_price"])
if "selected_timeframes" not in st.session_state:
    st.session_state.selected_timeframes = CORE_TIMEFRAMES.copy()

with st.sidebar:
    st.title("⚡ Terminal")
    symbol = st.text_input("Пара", value=DEFAULT_SYMBOL).upper().replace("/", "").strip()
    interval = st.selectbox("Таймфрейм графика", INTERVALS, index=5)
    selected_timeframes = st.multiselect("Таймфреймы анализа", INTERVALS, default=st.session_state.selected_timeframes)
    if selected_timeframes:
        st.session_state.selected_timeframes = selected_timeframes
    limit = st.slider("Свечи", 100, 1000, 420, step=40)
    show_ema = st.toggle("EMA", value=True)
    show_bb = st.toggle("Bollinger", value=False)
    show_volume = st.toggle("Volume", value=True)
    show_rsi = st.toggle("RSI", value=True)
    show_macd = st.toggle("MACD", value=False)
    if st.button("⭐ В избранное", use_container_width=True):
        if symbol and symbol not in st.session_state.favorites:
            st.session_state.favorites.append(symbol)
            st.success(f"{symbol} добавлена")

app_top(symbol)
page = top_nav()

tfs = st.session_state.selected_timeframes or CORE_TIMEFRAMES

try:
    if page == "Dashboard":
        dashboard.render()
    elif page == "Chart":
        chart.render(symbol, interval, limit, show_ema, show_bb, show_volume, show_rsi, show_macd, tfs)
    elif page == "Multi TF":
        multi_tf.render(symbol, tfs, limit)
    elif page == "Scanner":
        scanner.render(st.session_state.favorites, tfs)
    elif page == "Heatmap":
        heatmap.render()
    elif page == "Favorites":
        favorites.render(st.session_state.favorites, interval)
    elif page == "Portfolio":
        portfolio.render()
    elif page == "Settings":
        settings.render(tfs)
except BinanceDataError as exc:
    st.error(str(exc))
except Exception as exc:
    st.exception(exc)
