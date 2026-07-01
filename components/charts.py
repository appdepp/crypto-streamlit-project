from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def candlestick_chart(df, symbol: str, show_ema=True, show_bb=True, compact: bool = False):
    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        vertical_spacing=0.025 if compact else 0.03,
        row_heights=[0.58, 0.14, 0.14, 0.14],
    )
    fig.add_trace(go.Candlestick(x=df["open_time"], open=df["open"], high=df["high"], low=df["low"], close=df["close"], name="Price"), row=1, col=1)
    if show_ema:
        for col, name in [("ema20", "EMA20"), ("ema50", "EMA50"), ("ema200", "EMA200")]:
            fig.add_trace(go.Scatter(x=df["open_time"], y=df[col], name=name, mode="lines", line=dict(width=1.15)), row=1, col=1)
    if show_bb:
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["bb_upper"], name="BB upper", mode="lines", line=dict(width=0.8, dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["bb_lower"], name="BB lower", mode="lines", line=dict(width=0.8, dash="dot")), row=1, col=1)
    fig.add_trace(go.Bar(x=df["open_time"], y=df["volume"], name="Volume"), row=2, col=1)
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["rsi"], name="RSI", mode="lines"), row=3, col=1)
    fig.add_hline(y=70, line_dash="dot", row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", row=3, col=1)
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["macd"], name="MACD", mode="lines"), row=4, col=1)
    fig.add_trace(go.Scatter(x=df["open_time"], y=df["macd_signal"], name="Signal", mode="lines"), row=4, col=1)
    fig.add_trace(go.Bar(x=df["open_time"], y=df["macd_hist"], name="Hist"), row=4, col=1)
    fig.update_layout(
        title=None if compact else f"{symbol} · Candles / Volume / RSI / MACD",
        template="plotly_dark",
        height=620 if compact else 840,
        xaxis_rangeslider_visible=False,
        margin=dict(l=4 if compact else 18, r=4 if compact else 18, t=18 if compact else 48, b=8),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, font=dict(size=10 if compact else 12)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def gauge(score: int, title: str, compact: bool = False):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        title={"text": title, "font": {"size": 14 if compact else 16}},
        gauge={"axis": {"range": [0, 100]}, "bar": {"thickness": 0.28}},
    ))
    fig.update_layout(template="plotly_dark", height=155 if compact else 230, margin=dict(l=6, r=6, t=30, b=6), paper_bgcolor="rgba(0,0,0,0)")
    return fig
