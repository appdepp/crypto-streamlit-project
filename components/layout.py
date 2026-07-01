from __future__ import annotations

import streamlit as st
from config import MENU


def hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-title">📈 Crypto<br/>Terminal 3.0</div>
          <div class="hero-subtitle">Мобильный криптотерминал: market overview, chart, индикаторы, scoring, scanner, heatmap, favorites и portfolio.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def top_nav() -> str:
    return st.selectbox("Раздел", MENU, index=0, label_visibility="collapsed")


def chips(items: list[str]) -> None:
    html = "".join(f"<span class='coin-chip'>● {item}</span>" for item in items)
    st.markdown(html, unsafe_allow_html=True)


def signal_class(signal: str) -> str:
    if "Buy" in signal:
        return "signal-buy"
    if "Sell" in signal:
        return "signal-sell"
    return "signal-neutral"


def signal_badge(signal: str, score: int | float | None = None) -> str:
    suffix = "" if score is None else f" · {int(score)}/100"
    return f"<span class='{signal_class(signal)}'>{signal}{suffix}</span>"
