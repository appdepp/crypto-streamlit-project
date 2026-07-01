from __future__ import annotations


def inject_css() -> None:
    import streamlit as st
    st.markdown("""
    <style>
    :root { --bg:#05070b; --panel:rgba(255,255,255,.055); --border:rgba(255,255,255,.10); --muted:#94a3b8; --green:#32d583; --yellow:#fdb022; --red:#f97066; --accent:#ff4b5c; }
    .stApp { background: radial-gradient(circle at 5% 0%, #162034 0, #070b12 34%, #05070b 100%); color:#f8fafc; }
    [data-testid="stSidebar"] { background:#0b111c; border-right:1px solid var(--border); }
    .block-container { padding-top:1rem; padding-bottom:4rem; max-width:1480px; }
    h1 { font-size:clamp(2rem, 5vw, 4rem)!important; line-height:1!important; }
    h2 { font-size:clamp(1.35rem, 3.2vw, 2.2rem)!important; }
    .hero { padding:1.25rem 1.35rem; border:1px solid var(--border); border-radius:24px; background:linear-gradient(135deg, rgba(255,75,92,.14), rgba(50,213,131,.08) 45%, rgba(96,165,250,.07)), rgba(255,255,255,.04); box-shadow:0 20px 60px rgba(0,0,0,.28); margin-bottom:1rem; }
    .hero-title { font-size:clamp(2.2rem, 6vw, 4.2rem); line-height:1.02; font-weight:900; margin:0; }
    .hero-subtitle { color:var(--muted); font-size:clamp(.92rem, 2.2vw, 1.05rem); margin-top:.75rem; max-width:850px; }
    div[data-testid="stMetric"] { background:var(--panel); padding:14px 15px; border-radius:18px; border:1px solid var(--border); box-shadow:0 12px 35px rgba(0,0,0,.20); min-height:106px; }
    div[data-testid="stMetricLabel"] { color:var(--muted); }
    div[data-testid="stMetricValue"] { font-size:clamp(1.35rem, 3.5vw, 2rem); letter-spacing:-.03em; }
    .terminal-card { border:1px solid var(--border); background:var(--panel); border-radius:20px; padding:1rem; box-shadow:0 16px 45px rgba(0,0,0,.22); }
    .coin-chip { display:inline-flex; align-items:center; gap:.45rem; padding:.42rem .7rem; border:1px solid var(--border); border-radius:999px; margin:.2rem .22rem .2rem 0; background:rgba(255,255,255,.06); color:#f8fafc; font-size:.92rem; }
    .signal-buy { color:var(--green); font-weight:900; }
    .signal-neutral { color:var(--yellow); font-weight:900; }
    .signal-sell { color:var(--red); font-weight:900; }
    div[data-testid="stDataFrame"] { border-radius:16px; overflow:hidden; border:1px solid var(--border); }
    div[data-testid="stPlotlyChart"] { border-radius:18px; overflow:hidden; }
    .stButton > button, .stDownloadButton > button { border-radius:14px!important; min-height:44px; font-weight:700; }
    @media (max-width: 760px) {
      .block-container { padding-left:.72rem!important; padding-right:.72rem!important; padding-top:.65rem!important; max-width:100%!important; }
      .hero { padding:1rem .95rem; border-radius:18px; margin-bottom:.7rem; }
      .hero-title { font-size:2.05rem; }
      .hero-subtitle { font-size:.9rem; margin-top:.55rem; }
      div[data-testid="stMetric"] { min-height:82px; padding:12px 13px; border-radius:16px; }
      div[data-testid="stMetricValue"] { font-size:1.52rem!important; }
      div[data-testid="stMetricLabel"], div[data-testid="stMetricDelta"] { font-size:.78rem!important; }
      [data-testid="column"] { width:100%!important; flex:1 1 100%!important; min-width:100%!important; }
      [data-testid="stHorizontalBlock"] { flex-wrap:wrap!important; gap:.55rem!important; }
      iframe, .js-plotly-plot, .plot-container, .svg-container { max-width:100%!important; }
    }
    </style>
    """, unsafe_allow_html=True)
