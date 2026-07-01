from __future__ import annotations

import pandas as pd
import streamlit as st


def price_fmt(value) -> str:
    if value is None or pd.isna(value):
        return "—"
    value = float(value)
    if value >= 1000:
        return f"${value:,.0f}"
    if value >= 1:
        return f"${value:,.4f}"
    if value >= .01:
        return f"${value:,.5f}"
    return f"${value:,.8f}"


def badge_html(signal: str) -> str:
    css_class = "buy" if "Buy" in signal else "sell" if "Sell" in signal else "neutral"
    return f"<span class='badge {css_class}'>{signal}</span>"


def render_topbar() -> None:
    st.markdown("<div class='topbar'><div class='brand'><span class='dot'></span>Crypto Terminal</div><div class='muted'>Stable modular</div></div>", unsafe_allow_html=True)


def render_asset_card(symbol: str, score: dict, change=None, subtitle: str | None = None) -> None:
    change_text = "—" if change is None or pd.isna(change) else f"{float(change):+.2f}%"
    subtitle = subtitle or f"24h {change_text} · RSI {score['rsi']:.1f} · ADX {score['adx']:.1f}"
    st.markdown(
        f"""
        <div class='asset'>
          <div class='asset-row'>
            <div>
              <div class='sym'>{symbol}</div>
              <div class='price'>{price_fmt(score['price'])}</div>
              <div class='muted'>{subtitle}</div>
            </div>
            <div style='text-align:right'>
              {badge_html(score['signal'])}
              <div style='font-size:2.2rem;font-weight:950;line-height:1;margin-top:.4rem;letter-spacing:-.06em'>{score['total']}</div>
              <div class='muted'>score</div>
            </div>
          </div>
          <div class='mini'>
            <div class='mini-card'><div class='ml'>Trend</div><div class='mv'>{score['trend']}</div></div>
            <div class='mini-card'><div class='ml'>Momentum</div><div class='mv'>{score['momentum']}</div></div>
            <div class='mini-card'><div class='ml'>Volume</div><div class='mv'>{score['volume']}</div></div>
            <div class='mini-card'><div class='ml'>Volatility</div><div class='mv'>{score['volatility']}</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_scan_cards(df: pd.DataFrame, name_col: str = "symbol") -> None:
    for _, row in df.iterrows():
        signal = str(row.get("signal", "Neutral"))
        score_value = int(row.get("score", 0)) if not pd.isna(row.get("score", 0)) else 0
        pills = []
        for key in ["change_%", "rsi", "adx", "trend", "momentum", "timeframes"]:
            if key in row and not pd.isna(row[key]):
                value = row[key]
                if key == "change_%":
                    pills.append(f"<span class='pill'>24h {float(value):+.2f}%</span>")
                elif key == "timeframes":
                    pills.append(f"<span class='pill'>{value}</span>")
                else:
                    pills.append(f"<span class='pill'>{key.upper()} {float(value):.1f}</span>")
        st.markdown(
            f"<div class='scan'><div class='scan-row'><div><div class='scan-symbol'>{row[name_col]}</div>{badge_html(signal)}</div><div class='scan-score'>{score_value}</div></div><div class='pills'>{''.join(pills)}</div></div>",
            unsafe_allow_html=True,
        )


def render_pills(items: list[str]) -> None:
    st.markdown(" ".join([f"<span class='pill'>{item}</span>" for item in items]), unsafe_allow_html=True)
