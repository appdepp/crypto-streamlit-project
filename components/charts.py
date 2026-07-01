from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def candlestick_chart(df, symbol: str, show_ema=True, show_bb=False, show_volume=True, show_rsi=True, show_macd=False, compact: bool = True):
    lower_rows = int(show_volume) + int(show_rsi) + int(show_macd)
    rows = 1 + lower_rows
    heights = [0.68] + ([0.12] if show_volume else []) + ([0.10] if show_rsi else []) + ([0.10] if show_macd else [])
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.025, row_heights=heights)
    fig.add_trace(go.Candlestick(x=df["open_time"], open=df["open"], high=df["high"], low=df["low"], close=df["close"], name="Price"), row=1, col=1)
    if show_ema:
        for col, name in [("ema20", "EMA20"), ("ema50", "EMA50"), ("ema200", "EMA200")]:
            fig.add_trace(go.Scatter(x=df["open_time"], y=df[col], name=name, mode="lines", line=dict(width=1.05)), row=1, col=1)
    if show_bb:
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["bb_upper"], name="BB upper", mode="lines", line=dict(width=.75, dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["bb_lower"], name="BB lower", mode="lines", line=dict(width=.75, dash="dot")), row=1, col=1)
    r = 2
    if show_volume:
        fig.add_trace(go.Bar(x=df["open_time"], y=df["volume"], name="Volume"), row=r, col=1)
        r += 1
    if show_rsi:
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["rsi"], name="RSI", mode="lines", line=dict(width=1.1)), row=r, col=1)
        fig.add_hline(y=70, line_dash="dot", row=r, col=1)
        fig.add_hline(y=30, line_dash="dot", row=r, col=1)
        r += 1
    if show_macd:
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["macd"], name="MACD", mode="lines", line=dict(width=1)), row=r, col=1)
        fig.add_trace(go.Scatter(x=df["open_time"], y=df["macd_signal"], name="Signal", mode="lines", line=dict(width=1)), row=r, col=1)
        fig.add_trace(go.Bar(x=df["open_time"], y=df["macd_hist"], name="Hist"), row=r, col=1)
    fig.update_layout(
        template="plotly_dark",
        height=520 if compact else 740,
        xaxis_rangeslider_visible=False,
        margin=dict(l=2, r=2, t=12, b=4),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,.055)", zeroline=False)
    fig.update_xaxes(showgrid=False, rangeslider_visible=False)
    return fig
