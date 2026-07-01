from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def candlestick_chart(df, show_ema=True, show_bb=False, show_volume=True, show_rsi=True, show_macd=True):
    rows = 1 + int(show_volume) + int(show_rsi) + int(show_macd)
    heights = [0.58] + [0.14] * (rows - 1)
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=.025, row_heights=heights)
    row = 1
    fig.add_trace(go.Candlestick(x=df.open_time, open=df.open, high=df.high, low=df.low, close=df.close, name="Price"), row=row, col=1)
    if show_ema:
        for col, name in [("ema20", "EMA20"), ("ema50", "EMA50"), ("ema200", "EMA200")]:
            fig.add_trace(go.Scatter(x=df.open_time, y=df[col], name=name, mode="lines", line=dict(width=1)), row=1, col=1)
    if show_bb:
        fig.add_trace(go.Scatter(x=df.open_time, y=df.bb_upper, name="BB upper", mode="lines", line=dict(width=.8, dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.open_time, y=df.bb_lower, name="BB lower", mode="lines", line=dict(width=.8, dash="dot")), row=1, col=1)
    if show_volume:
        row += 1
        fig.add_trace(go.Bar(x=df.open_time, y=df.volume, name="Volume", opacity=.45), row=row, col=1)
    if show_rsi:
        row += 1
        fig.add_trace(go.Scatter(x=df.open_time, y=df.rsi, name="RSI", mode="lines"), row=row, col=1)
        fig.add_hline(y=70, line_dash="dot", row=row, col=1)
        fig.add_hline(y=30, line_dash="dot", row=row, col=1)
    if show_macd:
        row += 1
        fig.add_trace(go.Scatter(x=df.open_time, y=df.macd, name="MACD", mode="lines"), row=row, col=1)
        fig.add_trace(go.Scatter(x=df.open_time, y=df.macd_signal, name="Signal", mode="lines"), row=row, col=1)
        fig.add_trace(go.Bar(x=df.open_time, y=df.macd_hist, name="Hist", opacity=.45), row=row, col=1)
    fig.update_layout(
        template="plotly_dark", height=720 if rows > 2 else 540,
        margin=dict(l=4, r=4, t=18, b=8), xaxis_rangeslider_visible=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.01, x=0, font=dict(size=10)),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,.04)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,.04)")
    return fig
