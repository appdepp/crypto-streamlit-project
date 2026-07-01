from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def inject_css() -> None:
    import streamlit as st
    st.markdown(
        """
        <style>
        :root {
            --bg: #05070b;
            --panel: rgba(255,255,255,.055);
            --panel-2: rgba(255,255,255,.085);
            --border: rgba(255,255,255,.10);
            --text: #f8fafc;
            --muted: #94a3b8;
            --green: #32d583;
            --yellow: #fdb022;
            --red: #f97066;
            --accent: #ff4b5c;
        }
        .stApp {
            background: radial-gradient(circle at 5% 0%, #162034 0, #070b12 34%, #05070b 100%);
            color: var(--text);
        }
        [data-testid="stSidebar"] {
            background: #0b111c;
            border-right: 1px solid var(--border);
        }
        .block-container {
            padding-top: 1.1rem;
            padding-bottom: 4rem;
            max-width: 1480px;
        }
        h1, h2, h3 { letter-spacing: .01em; }
        h1 { font-size: clamp(2rem, 5vw, 4rem) !important; line-height: .98 !important; }
        h2 { font-size: clamp(1.45rem, 3.2vw, 2.3rem) !important; }
        h3 { font-size: clamp(1.15rem, 2.5vw, 1.55rem) !important; }
        p, label, span { -webkit-font-smoothing: antialiased; }
        .hero {
            padding: 1.35rem 1.4rem 1.15rem;
            border: 1px solid var(--border);
            border-radius: 24px;
            background:
              linear-gradient(135deg, rgba(255,75,92,.14), rgba(50,213,131,.08) 45%, rgba(96,165,250,.07)),
              rgba(255,255,255,.04);
            box-shadow: 0 20px 60px rgba(0,0,0,.28);
            margin-bottom: 1rem;
        }
        .hero-title { font-size: clamp(2.25rem, 6vw, 4.25rem); line-height: .98; font-weight: 900; margin: 0; }
        .hero-subtitle { color: var(--muted); font-size: clamp(.95rem, 2.2vw, 1.05rem); margin-top: .8rem; max-width: 850px; }
        .mobile-menu-note { display: none; }
        div[data-testid="stMetric"] {
            background: var(--panel);
            padding: 15px 16px;
            border-radius: 18px;
            border: 1px solid var(--border);
            box-shadow: 0 12px 35px rgba(0,0,0,.20);
            min-height: 112px;
        }
        div[data-testid="stMetricLabel"] { color: var(--muted); }
        div[data-testid="stMetricValue"] { font-size: clamp(1.45rem, 3.6vw, 2.1rem); letter-spacing: -.03em; }
        div[data-testid="stMetricDelta"] { font-size: .95rem; }
        .terminal-card {
            border: 1px solid var(--border);
            background: var(--panel);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 16px 45px rgba(0,0,0,.22);
        }
        .coin-chip {
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            padding: .42rem .7rem;
            border: 1px solid var(--border);
            border-radius: 999px;
            margin: .2rem .22rem .2rem 0;
            background: rgba(255,255,255,.06);
            color: var(--text);
            font-size: .92rem;
        }
        .signal-buy { color: var(--green); font-weight: 900; }
        .signal-neutral { color: var(--yellow); font-weight: 900; }
        .signal-sell { color: var(--red); font-weight: 900; }
        .score-pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: .45rem .75rem;
            background: rgba(50,213,131,.12);
            border: 1px solid rgba(50,213,131,.22);
            font-weight: 800;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        div[data-testid="stPlotlyChart"] {
            border-radius: 18px;
            overflow: hidden;
        }
        .stButton > button, .stDownloadButton > button {
            border-radius: 14px !important;
            min-height: 44px;
            font-weight: 700;
        }
        .stSelectbox, .stTextInput, .stNumberInput { border-radius: 14px; }
        /* On phones: one-column, compact header, no horizontal overflow */
        @media (max-width: 760px) {
            .block-container {
                padding-left: .72rem !important;
                padding-right: .72rem !important;
                padding-top: .65rem !important;
                max-width: 100% !important;
            }
            .hero {
                padding: 1rem .95rem .95rem;
                border-radius: 18px;
                margin-bottom: .7rem;
            }
            .hero-title { font-size: 2.05rem; line-height: 1.02; }
            .hero-subtitle { font-size: .92rem; margin-top: .55rem; }
            .mobile-menu-note { display: block; color: var(--muted); font-size: .82rem; margin-top: -.3rem; margin-bottom: .55rem; }
            div[data-testid="stMetric"] {
                min-height: 82px;
                padding: 12px 13px;
                border-radius: 16px;
            }
            div[data-testid="stMetricValue"] { font-size: 1.55rem !important; }
            div[data-testid="stMetricLabel"] { font-size: .78rem !important; }
            div[data-testid="stMetricDelta"] { font-size: .78rem !important; }
            [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
            [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: .55rem !important; }
            iframe { max-width: 100% !important; }
            .js-plotly-plot, .plot-container, .svg-container { max-width: 100% !important; }
            .st-emotion-cache-1y4p8pa, .st-emotion-cache-1jicfl2 { padding-left: .75rem !important; padding-right: .75rem !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero() -> None:
    import streamlit as st
    st.markdown(
        """
        <div class="hero">
          <div class="hero-title">📈 Crypto<br/>Terminal 2.1</div>
          <div class="hero-subtitle">Адаптивный терминал для крипторынка: мобильный интерфейс, свечи, индикаторы, скоринг, scanner, heatmap и портфель.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chips(items: list[str]) -> None:
    import streamlit as st
    html = "".join(f"<span class='coin-chip'>● {item}</span>" for item in items)
    st.markdown(html, unsafe_allow_html=True)


def signal_class(signal: str) -> str:
    if "Buy" in signal:
        return "signal-buy"
    if "Sell" in signal:
        return "signal-sell"
    return "signal-neutral"


def signal_badge(signal: str, score: int | float | None = None) -> str:
    cls = signal_class(signal)
    suffix = "" if score is None else f" · {int(score)}/100"
    return f"<span class='{cls}'>{signal}{suffix}</span>"


def candlestick_chart(df, symbol: str, show_ema=True, show_bb=True, compact: bool = False):
    rows = 4
    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.025 if compact else 0.03,
        row_heights=[0.58, 0.14, 0.14, 0.14],
        specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]],
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(fixedrange=False)
    return fig


def gauge(score: int, title: str, compact: bool = False):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": title, "font": {"size": 14 if compact else 16}},
        gauge={"axis": {"range": [0, 100]}, "bar": {"thickness": 0.28}},
    ))
    fig.update_layout(
        template="plotly_dark",
        height=155 if compact else 230,
        margin=dict(l=6, r=6, t=30, b=6),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
