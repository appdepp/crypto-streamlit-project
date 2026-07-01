from __future__ import annotations

import math
import streamlit as st
from config import MENU


def format_price(value: float | int | None) -> str:
    if value is None:
        return "—"
    try:
        v = float(value)
    except Exception:
        return "—"
    if math.isnan(v):
        return "—"
    if v >= 1000:
        return f"${v:,.0f}"
    if v >= 1:
        return f"${v:,.3f}".rstrip("0").rstrip(".")
    return f"${v:.6f}".rstrip("0").rstrip(".")


def signal_class(signal: str) -> str:
    if "Buy" in str(signal):
        return "signal-buy"
    if "Sell" in str(signal):
        return "signal-sell"
    return "signal-neutral"


def signal_color(signal: str) -> str:
    if "Buy" in str(signal):
        return "green"
    if "Sell" in str(signal):
        return "red"
    return "yellow"


def signal_badge(signal: str, score: int | float | None = None) -> str:
    suffix = "" if score is None else f" · {int(score)}/100"
    return f"<span class='{signal_class(signal)}'>{signal}{suffix}</span>"


def stars(score: int | float) -> str:
    n = max(1, min(5, round(float(score) / 20)))
    return "★" * n + "☆" * (5 - n)


def app_top(symbol: str | None = None) -> None:
    right = f"<span class='quick-dot'>{symbol}</span>" if symbol else "<span class='quick-dot'>Live market</span>"
    st.markdown(
        f"""
        <div class="app-top">
          <div class="brand">
            <div class="brand-icon">📈</div>
            <div><div>Crypto Terminal 4.0</div><div class="brand-sub">mobile trading dashboard</div></div>
          </div>
          {right}
        </div>
        """,
        unsafe_allow_html=True,
    )


def top_nav() -> str:
    return st.selectbox("Раздел", MENU, index=1, label_visibility="collapsed")


def section(title: str, subtitle: str | None = None) -> None:
    sub = "" if not subtitle else f"<div class='section-sub'>{subtitle}</div>"
    st.markdown(f"<div class='section-title'>{title}</div>{sub}", unsafe_allow_html=True)


def asset_card(symbol: str, price: float, signal: str, score: int, rsi: float | None = None, adx: float | None = None, interval: str | None = None) -> None:
    color = signal_color(signal)
    extra = []
    if interval:
        extra.append(f"<span class='pill'>{interval}</span>")
    if rsi is not None:
        extra.append(f"<span class='pill'>RSI {rsi:.1f}</span>")
    if adx is not None:
        extra.append(f"<span class='pill'>ADX {adx:.1f}</span>")
    meta = "".join(extra)
    st.markdown(
        f"""
        <div class="asset-card">
          <div class="asset-row">
            <div>
              <div class="asset-symbol">{symbol}</div>
              <div class="asset-price">{format_price(price)}</div>
              <div class="asset-meta"><span class="pill {color}">{signal}</span>{meta}</div>
            </div>
            <div>
              <div class="score-label">Score</div>
              <div class="score-big">{int(score)}</div>
              <div class="stars">{stars(score)}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_bars(score: dict) -> None:
    items = [
        ("Trend", score.get("trend", 0)),
        ("Momentum", score.get("momentum", 0)),
        ("Volume", score.get("volume", 0)),
        ("Volatility", score.get("volatility", 0)),
        ("ADX", score.get("adx_score", score.get("adx", 0))),
    ]
    rows = []
    for label, value in items:
        try:
            v = max(0, min(100, int(round(float(value)))))
        except Exception:
            v = 0
        rows.append(f"<div class='bar-row'><div class='bar-label'>{label}</div><div class='bar-track'><div class='bar-fill' style='width:{v}%'></div></div><div class='bar-value'>{v}</div></div>")
    st.markdown("<div class='terminal-card'>" + "".join(rows) + "</div>", unsafe_allow_html=True)


def mini_metrics(items: list[tuple[str, str, str | None]]) -> None:
    cards = []
    for label, value, delta in items:
        d = "" if not delta else f"<div class='mini-delta'>{delta}</div>"
        cards.append(f"<div class='mini-card'><div class='mini-label'>{label}</div><div class='mini-value'>{value}</div>{d}</div>")
    st.markdown("<div class='metric-grid'>" + "".join(cards) + "</div>", unsafe_allow_html=True)


def chips(items: list[str]) -> None:
    html = "".join(f"<span class='coin-chip'>● {item}</span>" for item in items)
    st.markdown(html, unsafe_allow_html=True)


def scan_cards(rows) -> None:
    html_parts = []
    for _, row in rows.iterrows():
        signal = str(row.get("signal", "Neutral"))
        cls = signal_class(signal)
        html_parts.append(
            f"""
            <div class="scan-card">
              <div><div class="scan-symbol">{row.get('symbol','')}</div><div class="scan-price">{format_price(row.get('price'))} · RSI {row.get('rsi','—')} · ADX {row.get('adx','—')}</div></div>
              <div><div class="scan-score">{int(row.get('score',0))}</div><div class="scan-signal {cls}">{signal}</div></div>
            </div>
            """
        )
    st.markdown("".join(html_parts), unsafe_allow_html=True)
