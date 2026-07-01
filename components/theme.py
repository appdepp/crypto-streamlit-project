from __future__ import annotations


def inject_css() -> None:
    import streamlit as st
    st.markdown(
        """
        <style>
        :root {
          --bg:#05070b; --bg2:#08101d; --card:#101722; --card2:#121c2a;
          --line:rgba(255,255,255,.10); --line2:rgba(255,255,255,.16);
          --txt:#f8fafc; --muted:#8b96a8; --muted2:#64748b;
          --green:#00D26A; --yellow:#F5B301; --red:#FF4D4F; --blue:#4EA1FF; --accent:#ff4655;
        }
        html, body { background: #05070b !important; }
        .stApp{background:radial-gradient(circle at 10% -5%,#142033 0,#07101e 28%,#05070b 70%);color:var(--txt)}
        [data-testid="stHeader"], header, header[data-testid="stHeader"] {display:none!important; height:0!important; min-height:0!important; visibility:hidden!important;}
        [data-testid="stDecoration"]{display:none!important;}
        [data-testid="stToolbar"]{display:none!important;}
        [data-testid="stSidebar"]{background:#080e18;border-right:1px solid var(--line)}
        .block-container{max-width:1320px;padding-top:calc(env(safe-area-inset-top,0px) + 1.05rem)!important;padding-bottom:5.4rem}
        #MainMenu, footer{visibility:hidden}
        h1,h2,h3{letter-spacing:-.03em} h1{font-size:clamp(1.9rem,5vw,3.2rem)!important;line-height:1!important} h2{font-size:clamp(1.45rem,4vw,2.2rem)!important}
        .app-top{display:flex;align-items:center;justify-content:space-between;gap:.8rem;margin:0 0 .7rem;padding:.15rem 0 .1rem}
        .brand{display:flex;align-items:center;gap:.62rem;font-weight:900;font-size:1.08rem;letter-spacing:-.02em}
        .brand-icon{width:30px;height:30px;border-radius:11px;display:grid;place-items:center;background:linear-gradient(135deg,#ff4655,#4EA1FF);box-shadow:0 8px 22px rgba(255,70,85,.22)}
        .brand-sub{color:var(--muted);font-size:.72rem;font-weight:700;margin-top:-.12rem;text-transform:lowercase}
        .quick-dot{border:1px solid var(--line);border-radius:999px;padding:.34rem .55rem;background:rgba(255,255,255,.05);color:var(--muted);font-size:.78rem;white-space:nowrap;max-width:120px;overflow:hidden;text-overflow:ellipsis}
        .asset-card{border:1px solid var(--line2);border-radius:24px;padding:1.05rem;background:linear-gradient(135deg,rgba(255,70,85,.12),rgba(78,161,255,.08)),rgba(16,23,34,.92);box-shadow:0 18px 55px rgba(0,0,0,.30);margin:.25rem 0 1rem}
        .asset-row{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem}.asset-symbol{font-size:1.05rem;color:var(--muted);font-weight:800}.asset-price{font-size:clamp(2.1rem,8vw,4rem);font-weight:950;letter-spacing:-.075em;line-height:1.02;margin:.18rem 0}.asset-meta{display:flex;gap:.45rem;flex-wrap:wrap;margin-top:.55rem}.pill{border-radius:999px;padding:.38rem .62rem;border:1px solid var(--line);background:rgba(255,255,255,.06);font-size:.82rem;font-weight:800}.pill.green{color:var(--green);background:rgba(0,210,106,.11);border-color:rgba(0,210,106,.24)}.pill.yellow{color:var(--yellow);background:rgba(245,179,1,.11);border-color:rgba(245,179,1,.24)}.pill.red{color:var(--red);background:rgba(255,77,79,.11);border-color:rgba(255,77,79,.24)}
        .score-big{font-size:2rem;font-weight:950;letter-spacing:-.06em;text-align:right}.score-label{color:var(--muted);font-size:.78rem;text-align:right;font-weight:700}.stars{color:var(--yellow);font-size:.95rem;letter-spacing:.02em;text-align:right;margin-top:.2rem}
        .section-title{font-size:1.45rem;font-weight:950;letter-spacing:-.045em;margin:1.05rem 0 .25rem}.section-sub{color:var(--muted);font-size:.92rem;margin-bottom:.78rem;line-height:1.55}
        .terminal-card{border:1px solid var(--line);background:rgba(16,23,34,.82);border-radius:20px;padding:1rem;box-shadow:0 14px 42px rgba(0,0,0,.24)}
        .metric-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem}.mini-card{border:1px solid var(--line);background:rgba(16,23,34,.72);border-radius:18px;padding:.9rem}.mini-label{color:var(--muted);font-size:.76rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em}.mini-value{font-size:1.35rem;font-weight:900;letter-spacing:-.05em;margin-top:.2rem}.mini-delta{font-size:.82rem;margin-top:.28rem;font-weight:850}
        .bar-row{display:grid;grid-template-columns:88px 1fr 42px;align-items:center;gap:.7rem;margin:.62rem 0}.bar-label{color:var(--muted);font-weight:800;font-size:.86rem}.bar-track{height:10px;border-radius:999px;background:rgba(255,255,255,.08);overflow:hidden}.bar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--red),var(--yellow),var(--green));}.bar-value{text-align:right;font-weight:900;font-size:.88rem}
        .scan-card{display:grid;grid-template-columns:1fr auto;gap:.45rem;border:1px solid var(--line);background:linear-gradient(135deg,rgba(78,161,255,.06),rgba(255,255,255,.025)),rgba(16,23,34,.86);border-radius:18px;padding:.9rem 1rem;margin:.55rem 0;box-shadow:0 12px 30px rgba(0,0,0,.18)}.scan-symbol{font-size:1.05rem;font-weight:950;letter-spacing:.02em}.scan-price{color:var(--muted);font-size:.84rem;margin-top:.18rem}.scan-score{font-size:1.65rem;font-weight:950;letter-spacing:-.05em;text-align:right;line-height:1}.scan-signal{text-align:right;font-weight:950;font-size:.78rem;border-radius:999px;padding:.26rem .48rem;margin-top:.25rem;background:rgba(255,255,255,.06);border:1px solid var(--line);display:inline-block;white-space:nowrap}.signal-buy{color:var(--green);font-weight:900}.signal-neutral{color:var(--yellow);font-weight:900}.signal-sell{color:var(--red);font-weight:900}
        .coin-chip{display:inline-flex;align-items:center;gap:.45rem;padding:.46rem .72rem;border:1px solid var(--line);border-radius:999px;margin:.2rem .22rem .2rem 0;background:rgba(255,255,255,.06);color:var(--txt);font-size:.9rem;font-weight:750}

        .stSlider [data-baseweb="slider"] { padding-top: .25rem; }
        .stRadio label { color: var(--muted)!important; font-weight:800; }
        .stProgress > div > div > div > div { background: linear-gradient(90deg, var(--blue), var(--accent))!important; }
        .stExpander { border: 1px solid var(--line)!important; border-radius: 18px!important; overflow:hidden; background: rgba(16,23,34,.45)!important; }
        .desktop-grid-note{color:var(--muted);font-size:.8rem}
        div[data-testid="stMetric"]{background:rgba(16,23,34,.78);padding:14px;border-radius:18px;border:1px solid var(--line);box-shadow:0 12px 34px rgba(0,0,0,.18);min-height:96px}div[data-testid="stMetricValue"]{font-size:clamp(1.3rem,3vw,1.9rem);letter-spacing:-.04em}div[data-testid="stMetricLabel"]{color:var(--muted)}
        div[data-testid="stDataFrame"]{border-radius:16px;overflow:hidden;border:1px solid var(--line)}div[data-testid="stPlotlyChart"]{border-radius:18px;overflow:hidden}.stButton>button,.stDownloadButton>button{border-radius:16px!important;min-height:46px;font-weight:850}.stSelectbox div[data-baseweb="select"]>div,.stTextInput input,.stNumberInput input{border-radius:16px!important}
        @media(max-width:760px){.block-container{padding-left:.72rem!important;padding-right:.72rem!important;padding-top:calc(env(safe-area-inset-top,0px) + .95rem)!important;max-width:100%!important}.app-top{margin-top:0;margin-bottom:.55rem}.brand-icon{width:28px;height:28px;border-radius:10px}.brand{font-size:.9rem;line-height:1.05}.brand-sub{display:none}.quick-dot{font-size:.72rem;padding:.28rem .44rem;max-width:96px}.asset-card{padding:.85rem;border-radius:20px;margin:.1rem 0 .75rem}.asset-row{gap:.6rem}.asset-price{font-size:2.35rem}.score-big{font-size:1.55rem}.score-label,.stars{text-align:right}.asset-symbol{font-size:.92rem}.pill{font-size:.76rem;padding:.33rem .52rem}.metric-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem}.mini-card{padding:.75rem;border-radius:16px}.mini-value{font-size:1.15rem}.section-title{font-size:1.45rem;margin-top:1rem}.section-sub{font-size:.88rem}.bar-row{grid-template-columns:78px 1fr 34px;gap:.52rem;margin:.55rem 0}.bar-label{font-size:.8rem}.bar-track{height:9px}.scan-card{border-radius:16px;padding:.8rem;margin:.5rem 0}.scan-score{font-size:1.42rem}[data-testid="column"]{width:100%!important;flex:1 1 100%!important;min-width:100%!important}[data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:.55rem!important}iframe,.js-plotly-plot,.plot-container,.svg-container{max-width:100%!important}.stRadio [role="radiogroup"]{gap:.8rem!important;flex-wrap:wrap!important}}
        </style>
        """,
        unsafe_allow_html=True,
    )
