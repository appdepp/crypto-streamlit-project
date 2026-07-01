from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from services.binance import get_klines


def render():
    st.subheader("Virtual portfolio")
    st.caption("Демо-портфель хранится в session_state браузера.")
    c1, c2, c3 = st.columns(3)
    p_symbol = c1.text_input("Symbol", "BTCUSDT", key="p_symbol").upper().replace("/", "").strip()
    amount = c2.number_input("Amount", min_value=0.0, value=0.01, step=0.01, format="%.8f")
    buy_price = c3.number_input("Buy price", min_value=0.0, value=50000.0, step=100.0)
    if st.button("Добавить позицию", use_container_width=True):
        new = pd.DataFrame([{"symbol": p_symbol, "amount": amount, "buy_price": buy_price}])
        st.session_state.portfolio = pd.concat([st.session_state.portfolio, new], ignore_index=True)
    if st.session_state.portfolio.empty:
        st.info("Добавь первую позицию выше.")
        return
    pf = st.session_state.portfolio.copy()
    current = []
    for s in pf["symbol"]:
        try:
            current.append(float(get_klines(s, "1h", 100).iloc[-1]["close"]))
        except Exception:
            current.append(None)
    pf["current_price"] = current
    pf["cost"] = pf["amount"] * pf["buy_price"]
    pf["value"] = pf["amount"] * pf["current_price"]
    pf["pnl"] = pf["value"] - pf["cost"]
    pf["pnl_%"] = pf["pnl"] / pf["cost"] * 100
    st.metric("Portfolio value", f"${pf['value'].sum():,.2f}", f"${pf['pnl'].sum():,.2f}")
    st.dataframe(pf, use_container_width=True, hide_index=True)
    fig = px.pie(pf, values="value", names="symbol", title="Allocation", template="plotly_dark")
    fig.update_layout(height=430, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    if st.button("Очистить портфель", use_container_width=True):
        st.session_state.portfolio = st.session_state.portfolio.iloc[0:0]
        st.rerun()
