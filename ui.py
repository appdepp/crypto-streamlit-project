from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def inject_css() -> None:
    import streamlit as st
    st.markdown(
        """
        <style>
        .stApp { background: radial-gradient(circle at top left, #162034 0, #070b12 35%, #05070b 100%); color: #f4f7fb; }
        [data-testid="stSidebar"] { background: #0b111c; border-right: 1px solid rgba(255,255,255,.08); }
        .block-container { padding-top: 1.4rem; max-width: 1500px; }
        h1, h2, h3 { letter-spacing: .02em; }
        .metric-card { padding: 18px 18px; border-radius: 18px; background: rgba(255,255,255,.055); border: 1px solid rgba(255,255,255,.09); box-shadow: 0 12px 35px rgba(0,0,0,.25); }
        .small-muted { color: #9ca3af; font-size: .9rem; }
        .signal-buy { color: #32d583; font-weight: 800; }
        .signal-neutral { color: #fdb022; font-weight: 800; }
        .signal-sell { color: #f97066; font-weight: 800; }
        div[data-testid="stMetric"] { background: rgba(255,255,255,.045); padding: 14px; border-radius: 16px; border: 1px solid rgba(255,255,255,.08); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def signal_class(signal: str) -> str:
    if "Buy" in signal:
        return "signal-buy"
    if "Sell" in signal:
        return "signal-sell"
    return "signal-neutral"


def candlestick_chart(df, symbol: str, show_ema=True, show_bb=True):
    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.55, 0.15, 0.15, 0.15],
        specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]],
    )
    fig.add_trace(go.Candlestick(x=df["open_time"], open=df["open"], high=df["high"], low=df["low"], close=df["close"], name="Price"), row=1, col=1)
    if show_ema:
        for col, name in [("ema20", "EMA 20"), ("ema50", "EMA 50"), ("ema200", "EMA 200")]:
            fig.add_trace(go.Scatter(x=df["open_time"], y=df[col], name=name, mode="lines", line=dict(width=1.2)), row=1, col=1)
    if show_bb:
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["bb_upper"], name="BB Upper", mode="lines", line=dict(width=0.8, dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["bb_lower"], name="BB Lower", mode="lines", line=dict(width=0.8, dash="dot")), row=1, col=1)

    fig.add_trace(go.Bar(x=df["open_time"], y=df["volume"], name="Volume"), row=2, col=1)
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["rsi"], name="RSI", mode="lines"), row=3, col=1)
    fig.add_hline(y=70, line_dash="dot", row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", row=3, col=1)
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["macd"], name="MACD", mode="lines"), row=4, col=1)
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["macd_signal"], name="Signal", mode="lines"), row=4, col=1)
    fig.add_trace(go.Bar(x=df["open_time"], y=df["macd_hist"], name="Histogram"), row=4, col=1)

    fig.update_layout(
        title=f"{symbol} · Candles / Volume / RSI / MACD",
        template="plotly_dark",
        height=880,
        xaxis_rangeslider_visible=False,
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def gauge(score: int, title: str):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": title},
        gauge={"axis": {"range": [0, 100]}, "bar": {"thickness": 0.25}},
    ))
    fig.update_layout(template="plotly_dark", height=250, margin=dict(l=10, r=10, t=40, b=10))
    return fig
