from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root{--panel:rgba(17,24,39,.84);--border:rgba(255,255,255,.10);--muted:#94a3b8;--green:#00d26a;--yellow:#f5b301;--red:#ff4d4f;}
        .stApp{background:radial-gradient(circle at top left,#151e31 0,#070b14 34%,#05070b 100%);color:#f8fafc}
        [data-testid="stHeader"]{background:rgba(5,7,11,.02);height:2.3rem}
        [data-testid="stSidebar"]{background:#090f1a;border-right:1px solid var(--border)}
        .block-container{padding-top:.25rem;padding-bottom:4rem;max-width:1480px}
        .topbar{display:flex;align-items:center;justify-content:space-between;margin:.1rem 0 .8rem}
        .brand{font-weight:950;font-size:clamp(1.15rem,3.5vw,1.55rem);letter-spacing:-.04em}
        .dot{display:inline-block;width:.55rem;height:.55rem;border-radius:99px;background:var(--green);box-shadow:0 0 16px rgba(0,210,106,.8);margin-right:.4rem}
        .muted{color:var(--muted);font-size:.88rem}
        .asset{border:1px solid var(--border);border-radius:22px;padding:1rem;background:linear-gradient(135deg,rgba(96,165,250,.13),rgba(0,210,106,.06)),var(--panel);box-shadow:0 18px 50px rgba(0,0,0,.28);margin-bottom:.85rem}
        .asset-row{display:flex;justify-content:space-between;gap:.8rem}.sym{font-size:1.05rem;font-weight:900;color:#dbeafe}.price{font-size:clamp(2.05rem,8vw,3.7rem);font-weight:950;letter-spacing:-.06em;line-height:1;margin:.4rem 0 .25rem}
        .badge{display:inline-flex;border-radius:999px;padding:.34rem .62rem;font-size:.78rem;font-weight:900;text-transform:uppercase;letter-spacing:.04em;border:1px solid}.buy{color:var(--green);background:rgba(0,210,106,.12);border-color:rgba(0,210,106,.28)}.neutral{color:var(--yellow);background:rgba(245,179,1,.12);border-color:rgba(245,179,1,.28)}.sell{color:var(--red);background:rgba(255,77,79,.12);border-color:rgba(255,77,79,.28)}
        .mini{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem;margin-top:.75rem}.mini-card{border:1px solid var(--border);background:rgba(255,255,255,.055);border-radius:16px;padding:.72rem;min-height:72px}.ml{color:var(--muted);font-size:.75rem}.mv{font-weight:900;font-size:1.15rem;margin-top:.15rem}
        .scan{border:1px solid var(--border);border-radius:18px;background:var(--panel);padding:.85rem;margin:.45rem 0;box-shadow:0 12px 30px rgba(0,0,0,.18)}.scan-row{display:flex;align-items:center;justify-content:space-between;gap:.7rem}.scan-symbol{font-weight:950;font-size:1.02rem}.scan-score{font-weight:950;font-size:1.7rem;letter-spacing:-.06em}.pills{display:flex;gap:.35rem;flex-wrap:wrap;margin-top:.5rem}.pill{border:1px solid var(--border);background:rgba(255,255,255,.06);color:#cbd5e1;border-radius:999px;padding:.22rem .48rem;font-size:.76rem}
        div[data-testid="stMetric"]{background:rgba(255,255,255,.055);border:1px solid var(--border);border-radius:16px;padding:12px 14px;min-height:86px}div[data-testid="stPlotlyChart"],div[data-testid="stDataFrame"]{border-radius:16px;overflow:hidden}.stButton>button{border-radius:14px!important;min-height:42px;font-weight:800}
        @media(max-width:760px){[data-testid="stHeader"]{height:2.2rem}.block-container{padding-left:.65rem!important;padding-right:.65rem!important;padding-top:.15rem!important}.mini{grid-template-columns:repeat(2,1fr)}.asset{border-radius:18px;padding:.9rem}.asset-row{flex-direction:column}[data-testid="column"]{width:100%!important;flex:1 1 100%!important;min-width:100%!important}[data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:.55rem!important}.stTabs [data-baseweb="tab-list"]{gap:.2rem;overflow-x:auto}.stTabs [data-baseweb="tab"]{padding:.45rem .55rem;font-size:.86rem}}
        </style>
        """,
        unsafe_allow_html=True,
    )
