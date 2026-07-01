from __future__ import annotations

import pandas as pd
import streamlit as st

from components.layout import hero, top_nav
from components.theme import inject_css
from config import APP_ICON, APP_TITLE, DEFAULT_SYMBOL, INTERVALS
from pages_app import chart, dashboard, favorites, heatmap, portfolio, scanner, settings
from services.binance import BinanceDataError

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
inject_css()

if "favorites" not in st.session_state:
    st.session_state.favorites = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["symbol", "amount", "buy_price"])

with st.sidebar:
    st.title("⚡ Crypto Terminal")
    st.caption("Binance public market data · Streamlit Cloud ready")
    symbol = st.text_input("Пара", value=DEFAULT_SYMBOL).upper().replace("/", "").strip()
    interval = st.selectbox("Таймфрейм", INTERVALS, index=5)
    limit = st.slider("Количество свечей", 100, 1000, 500, step=50)
    show_ema = st.toggle("EMA 20/50/200", value=True)
    show_bb = st.toggle("Bollinger Bands", value=True)
    st.divider()
    if st.button("⭐ Добавить в избранное", use_container_width=True):
        if symbol and symbol not in st.session_state.favorites:
            st.session_state.favorites.append(symbol)
            st.success(f"{symbol} добавлена")

hero()
page = top_nav()

try:
    if page == "Dashboard":
        dashboard.render()
    elif page == "Chart":
        chart.render(symbol, interval, limit, show_ema, show_bb)
    elif page == "Scanner":
        scanner.render(st.session_state.favorites)
    elif page == "Heatmap":
        heatmap.render()
    elif page == "Favorites":
        favorites.render(st.session_state.favorites, interval)
    elif page == "Portfolio":
        portfolio.render()
    elif page == "Settings":
        settings.render()
except BinanceDataError as exc:
    st.error(str(exc))
    st.info("Для Streamlit Cloud используется data-api.binance.vision. Если Binance снова блокирует IP, можно подключить CoinGecko/CoinCap fallback.")
except Exception as exc:
    st.exception(exc)
