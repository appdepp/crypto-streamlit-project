from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from services.binance import get_klines, normalize_symbol


def render(state: dict) -> None:
    c1, c2, c3 = st.columns(3)
    symbol = normalize_symbol(c1.text_input("Pair", "BTCUSDT", key="p_symbol"))
    amount = c2.number_input("Amount", min_value=0.0, value=0.01, step=0.01, format="%.8f")
    buy_price = c3.number_input("Buy price", min_value=0.000001, value=50000.0, step=100.0, format="%.8f")

    if st.button("Add position", use_container_width=True):
        new = pd.DataFrame([{"symbol": symbol, "amount": amount, "buy_price": buy_price}])
        st.session_state.portfolio = pd.concat([st.session_state.portfolio, new], ignore_index=True)

    portfolio = st.session_state.portfolio.copy()
    if portfolio.empty:
        st.info("Portfolio is empty")
        return

    prices = []
    for item in portfolio.symbol:
        try:
            prices.append(float(get_klines(item, "1h", 2).iloc[-1].close))
        except Exception:
            prices.append(np.nan)
    portfolio["current_price"] = prices
    portfolio["cost"] = portfolio.amount * portfolio.buy_price
    portfolio["value"] = portfolio.amount * portfolio.current_price
    portfolio["pnl"] = portfolio.value - portfolio.cost
    portfolio["pnl_%"] = np.where(portfolio.cost > 0, portfolio.pnl / portfolio.cost * 100, np.nan)

    st.metric("Portfolio value", f"${portfolio['value'].sum():,.2f}", f"${portfolio['pnl'].sum():,.2f}")
    st.dataframe(portfolio, use_container_width=True, hide_index=True)
    fig = px.pie(portfolio.dropna(subset=["value"]), values="value", names="symbol", template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    if st.button("Clear portfolio"):
        st.session_state.portfolio = st.session_state.portfolio.iloc[0:0]
        st.rerun()
