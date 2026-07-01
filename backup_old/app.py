from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import streamlit as st

APP_TITLE = "Crypto Terminal"
BASE_URLS = ["https://data-api.binance.vision", "https://api.binance.com"]
INTERVALS = ["5m", "15m", "30m", "1h", "4h", "6h", "12h", "1d", "3d", "1w", "1M"]
DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "TRXUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT", "UNIUSDT", "ATOMUSDT", "XLMUSDT", "ETCUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "NEARUSDT"]
STABLE_EXCLUDE = {"USDCUSDT", "BUSDUSDT", "FDUSDUSDT", "TUSDUSDT", "DAIUSDT", "EURUSDT"}

st.set_page_config(page_title=APP_TITLE, page_icon="📈", layout="wide", initial_sidebar_state="expanded")


def css():
    st.markdown("""
    <style>
    :root{--panel:rgba(17,24,39,.84);--border:rgba(255,255,255,.10);--muted:#94a3b8;--green:#00d26a;--yellow:#f5b301;--red:#ff4d4f;}
    .stApp{background:radial-gradient(circle at top left,#151e31 0,#070b14 34%,#05070b 100%);color:#f8fafc}
    [data-testid="stHeader"]{background:rgba(5,7,11,.02);height:2.3rem}[data-testid="stSidebar"]{background:#090f1a;border-right:1px solid var(--border)}
    .block-container{padding-top:.25rem;padding-bottom:4rem;max-width:1480px}.topbar{display:flex;align-items:center;justify-content:space-between;margin:.1rem 0 .8rem}.brand{font-weight:950;font-size:clamp(1.15rem,3.5vw,1.55rem);letter-spacing:-.04em}.dot{display:inline-block;width:.55rem;height:.55rem;border-radius:99px;background:var(--green);box-shadow:0 0 16px rgba(0,210,106,.8);margin-right:.4rem}.muted{color:var(--muted);font-size:.88rem}
    .asset{border:1px solid var(--border);border-radius:22px;padding:1rem;background:linear-gradient(135deg,rgba(96,165,250,.13),rgba(0,210,106,.06)),var(--panel);box-shadow:0 18px 50px rgba(0,0,0,.28);margin-bottom:.85rem}.asset-row{display:flex;justify-content:space-between;gap:.8rem}.sym{font-size:1.05rem;font-weight:900;color:#dbeafe}.price{font-size:clamp(2.05rem,8vw,3.7rem);font-weight:950;letter-spacing:-.06em;line-height:1;margin:.4rem 0 .25rem}.badge{display:inline-flex;border-radius:999px;padding:.34rem .62rem;font-size:.78rem;font-weight:900;text-transform:uppercase;letter-spacing:.04em;border:1px solid}.buy{color:var(--green);background:rgba(0,210,106,.12);border-color:rgba(0,210,106,.28)}.neutral{color:var(--yellow);background:rgba(245,179,1,.12);border-color:rgba(245,179,1,.28)}.sell{color:var(--red);background:rgba(255,77,79,.12);border-color:rgba(255,77,79,.28)}
    .mini{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem;margin-top:.75rem}.mini-card{border:1px solid var(--border);background:rgba(255,255,255,.055);border-radius:16px;padding:.72rem;min-height:72px}.ml{color:var(--muted);font-size:.75rem}.mv{font-weight:900;font-size:1.15rem;margin-top:.15rem}.section{font-size:1.05rem;font-weight:900;margin:.9rem 0 .5rem}.scan{border:1px solid var(--border);border-radius:18px;background:var(--panel);padding:.85rem;margin:.45rem 0;box-shadow:0 12px 30px rgba(0,0,0,.18)}.scan-row{display:flex;align-items:center;justify-content:space-between;gap:.7rem}.scan-symbol{font-weight:950;font-size:1.02rem}.scan-score{font-weight:950;font-size:1.7rem;letter-spacing:-.06em}.pills{display:flex;gap:.35rem;flex-wrap:wrap;margin-top:.5rem}.pill{border:1px solid var(--border);background:rgba(255,255,255,.06);color:#cbd5e1;border-radius:999px;padding:.22rem .48rem;font-size:.76rem}
    div[data-testid="stMetric"]{background:rgba(255,255,255,.055);border:1px solid var(--border);border-radius:16px;padding:12px 14px;min-height:86px}div[data-testid="stPlotlyChart"],div[data-testid="stDataFrame"]{border-radius:16px;overflow:hidden}.stButton>button{border-radius:14px!important;min-height:42px;font-weight:800}
    @media(max-width:760px){[data-testid="stHeader"]{height:2.2rem}.block-container{padding-left:.65rem!important;padding-right:.65rem!important;padding-top:.15rem!important}.mini{grid-template-columns:repeat(2,1fr)}.asset{border-radius:18px;padding:.9rem}.asset-row{flex-direction:column}[data-testid="column"]{width:100%!important;flex:1 1 100%!important;min-width:100%!important}[data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:.55rem!important}.stTabs [data-baseweb="tab-list"]{gap:.2rem;overflow-x:auto}.stTabs [data-baseweb="tab"]{padding:.45rem .55rem;font-size:.86rem}}
    </style>
    """, unsafe_allow_html=True)


def norm(s: str) -> str:
    return s.upper().replace("/", "").replace("-", "").strip()


def price_fmt(x) -> str:
    if x is None or pd.isna(x): return "—"
    x = float(x)
    if x >= 1000: return f"${x:,.0f}"
    if x >= 1: return f"${x:,.4f}"
    if x >= .01: return f"${x:,.5f}"
    return f"${x:,.8f}"


def badge_html(signal: str) -> str:
    cls = "buy" if "Buy" in signal else "sell" if "Sell" in signal else "neutral"
    return f"<span class='badge {cls}'>{signal}</span>"


def get_json(path, params=None):
    err = None
    for base in BASE_URLS:
        try:
            r = requests.get(base + path, params=params, timeout=15)
            r.raise_for_status(); return r.json()
        except Exception as e: err = e
    raise RuntimeError(f"Market data unavailable: {err}")


@st.cache_data(ttl=60, show_spinner=False)
def tickers24() -> pd.DataFrame:
    df = pd.DataFrame(get_json("/api/v3/ticker/24hr"))
    for c in ["lastPrice", "priceChangePercent", "quoteVolume", "volume", "highPrice", "lowPrice"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[df.symbol.str.endswith("USDT")]
    df = df[~df.symbol.isin(STABLE_EXCLUDE)]
    df = df[~df.symbol.str.contains("UPUSDT|DOWNUSDT|BULLUSDT|BEARUSDT", regex=True)]
    return df.sort_values("quoteVolume", ascending=False).reset_index(drop=True)


@st.cache_data(ttl=60, show_spinner=False)
def klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    data = get_json("/api/v3/klines", {"symbol": norm(symbol), "interval": interval, "limit": int(limit)})
    cols = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore"]
    df = pd.DataFrame(data, columns=cols)
    if df.empty: raise ValueError(f"Pair not found: {symbol}")
    df["open_time"] = pd.to_datetime(df.open_time, unit="ms")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]: df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[["open_time", "open", "high", "low", "close", "volume", "quote_volume"]]


def indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy(); close = df.close; high = df.high; low = df.low
    for span in (20, 50, 200): df[f"ema{span}"] = close.ewm(span=span, adjust=False).mean()
    delta = close.diff(); gain = delta.clip(lower=0).rolling(14).mean(); loss = (-delta.clip(upper=0)).rolling(14).mean()
    df["rsi"] = 100 - (100 / (1 + gain / loss.replace(0, np.nan)))
    ema12 = close.ewm(span=12, adjust=False).mean(); ema26 = close.ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26; df["macd_signal"] = df.macd.ewm(span=9, adjust=False).mean(); df["macd_hist"] = df.macd - df.macd_signal
    mid = close.rolling(20).mean(); std = close.rolling(20).std(); df["bb_upper"] = mid + 2*std; df["bb_lower"] = mid - 2*std
    prev = close.shift(1); tr = pd.concat([(high-low), (high-prev).abs(), (low-prev).abs()], axis=1).max(axis=1); df["atr"] = tr.rolling(14).mean()
    plus_dm = high.diff().where((high.diff() > -low.diff()) & (high.diff() > 0), 0.0); minus_dm = (-low.diff()).where((-low.diff() > high.diff()) & (-low.diff() > 0), 0.0)
    atr = df.atr.replace(0, np.nan); plus_di = 100 * plus_dm.rolling(14).mean() / atr; minus_di = 100 * minus_dm.rolling(14).mean() / atr
    df["adx"] = (((plus_di-minus_di).abs() / (plus_di+minus_di).replace(0, np.nan)) * 100).rolling(14).mean()
    return df


def clamp(v):
    if pd.isna(v): return 50
    return int(max(0, min(100, round(v))))


def score(df: pd.DataFrame) -> dict:
    d = df.dropna(); d = d if not d.empty else df; x = d.iloc[-1]
    price = float(x.close); rsi = float(x.rsi) if not pd.isna(x.rsi) else 50; adx = float(x.adx) if not pd.isna(x.adx) else 20
    trend = 50 + (17 if price > x.ema20 else -12) + (17 if x.ema20 > x.ema50 else -12) + (16 if x.ema50 > x.ema200 else -10); trend = clamp(trend)
    momentum = 50 + (16 if 45 <= rsi <= 65 else 5 if 35 <= rsi <= 75 else -12) + (18 if x.macd > x.macd_signal else -10); momentum = clamp(momentum)
    vol_avg = d.volume.tail(30).mean(); volume = clamp(50 + min(28, ((x.volume / vol_avg) - 1) * 28) if vol_avg > 0 else 50)
    volatility = clamp(100 - abs((x.atr / price * 100 if price else 2) - 2) * 12) if not pd.isna(x.atr) else 50
    total = clamp(trend*.32 + momentum*.32 + volume*.16 + volatility*.10 + clamp(adx*2.1)*.10)
    signal = "Strong Buy" if total >= 82 else "Buy" if total >= 64 else "Strong Sell" if total <= 24 else "Sell" if total <= 42 else "Neutral"
    return {"price":price, "rsi":rsi, "adx":adx, "trend":trend, "momentum":momentum, "volume":volume, "volatility":volatility, "total":total, "signal":signal}


def load(symbol, interval, limit): return indicators(klines(symbol, interval, limit))

def asset_card(symbol, sc, change=None):
    ch = "—" if change is None or pd.isna(change) else f"{float(change):+.2f}%"
    st.markdown(f"""<div class='asset'><div class='asset-row'><div><div class='sym'>{symbol}</div><div class='price'>{price_fmt(sc['price'])}</div><div class='muted'>24h {ch} · RSI {sc['rsi']:.1f} · ADX {sc['adx']:.1f}</div></div><div style='text-align:right'>{badge_html(sc['signal'])}<div style='font-size:2.2rem;font-weight:950;line-height:1;margin-top:.4rem;letter-spacing:-.06em'>{sc['total']}</div><div class='muted'>score</div></div></div><div class='mini'><div class='mini-card'><div class='ml'>Trend</div><div class='mv'>{sc['trend']}</div></div><div class='mini-card'><div class='ml'>Momentum</div><div class='mv'>{sc['momentum']}</div></div><div class='mini-card'><div class='ml'>Volume</div><div class='mv'>{sc['volume']}</div></div><div class='mini-card'><div class='ml'>Volatility</div><div class='mv'>{sc['volatility']}</div></div></div></div>""", unsafe_allow_html=True)


def fig_chart(df, show_ema=True, show_bb=False, show_volume=True, show_rsi=True, show_macd=True):
    rows = 1 + int(show_volume) + int(show_rsi) + int(show_macd); heights = [0.58] + [0.14]*(rows-1)
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=.025, row_heights=heights); row=1
    fig.add_trace(go.Candlestick(x=df.open_time, open=df.open, high=df.high, low=df.low, close=df.close, name="Price"), row=row, col=1)
    if show_ema:
        for c,n in [("ema20","EMA20"),("ema50","EMA50"),("ema200","EMA200")]: fig.add_trace(go.Scatter(x=df.open_time, y=df[c], name=n, mode="lines", line=dict(width=1)), row=1, col=1)
    if show_bb:
        fig.add_trace(go.Scatter(x=df.open_time, y=df.bb_upper, name="BB upper", mode="lines", line=dict(width=.8, dash="dot")), row=1, col=1); fig.add_trace(go.Scatter(x=df.open_time, y=df.bb_lower, name="BB lower", mode="lines", line=dict(width=.8, dash="dot")), row=1, col=1)
    if show_volume: row+=1; fig.add_trace(go.Bar(x=df.open_time, y=df.volume, name="Volume", opacity=.45), row=row, col=1)
    if show_rsi: row+=1; fig.add_trace(go.Scatter(x=df.open_time, y=df.rsi, name="RSI", mode="lines"), row=row, col=1); fig.add_hline(y=70, line_dash="dot", row=row, col=1); fig.add_hline(y=30, line_dash="dot", row=row, col=1)
    if show_macd: row+=1; fig.add_trace(go.Scatter(x=df.open_time, y=df.macd, name="MACD", mode="lines"), row=row, col=1); fig.add_trace(go.Scatter(x=df.open_time, y=df.macd_signal, name="Signal", mode="lines"), row=row, col=1); fig.add_trace(go.Bar(x=df.open_time, y=df.macd_hist, name="Hist", opacity=.45), row=row, col=1)
    fig.update_layout(template="plotly_dark", height=720 if rows>2 else 540, margin=dict(l=4,r=4,t=18,b=8), xaxis_rangeslider_visible=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.01, x=0, font=dict(size=10)))
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,.04)"); fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,.04)")
    return fig


def top_symbols(n):
    try: return tickers24().head(n).symbol.tolist()
    except Exception: return DEFAULT_SYMBOLS[:n]


def mtf(symbol, intervals, limit):
    rows=[]
    for itv in intervals:
        try:
            d=load(symbol,itv,limit); sc=score(d); rows.append({"timeframe":itv,"signal":sc["signal"],"score":sc["total"],"price":sc["price"],"rsi":round(sc["rsi"],1),"adx":round(sc["adx"],1),"trend":sc["trend"],"momentum":sc["momentum"]})
        except Exception: rows.append({"timeframe":itv,"signal":"Error","score":0,"price":np.nan,"rsi":np.nan,"adx":np.nan,"trend":0,"momentum":0})
    return pd.DataFrame(rows)


def scan_cards(df, name_col="symbol"):
    for _, r in df.iterrows():
        signal=str(r.get("signal","Neutral")); score_val=int(r.get("score",0)) if not pd.isna(r.get("score",0)) else 0
        pills=[]
        for k in ["change_%","rsi","adx","trend","momentum","timeframes"]:
            if k in r and not pd.isna(r[k]):
                val=r[k]
                if k=="change_%": pills.append(f"<span class='pill'>24h {float(val):+.2f}%</span>")
                elif k=="timeframes": pills.append(f"<span class='pill'>{val}</span>")
                else: pills.append(f"<span class='pill'>{k.upper()} {float(val):.1f}</span>")
        st.markdown(f"<div class='scan'><div class='scan-row'><div><div class='scan-symbol'>{r[name_col]}</div>{badge_html(signal)}</div><div class='scan-score'>{score_val}</div></div><div class='pills'>{''.join(pills)}</div></div>", unsafe_allow_html=True)


def run_scanner(symbols, intervals, limit, multi):
    rows=[]; prog=st.progress(0)
    for i,s in enumerate(symbols):
        try:
            if multi:
                t=mtf(s,intervals,limit); ok=t[t.signal!="Error"]; avg=int(ok.score.mean()) if not ok.empty else 0; signal="Strong Buy" if avg>=82 else "Buy" if avg>=64 else "Strong Sell" if avg<=24 and avg>0 else "Sell" if avg<=42 and avg>0 else "Neutral"; rows.append({"symbol":s,"signal":signal,"score":avg,"price":ok.price.iloc[-1] if not ok.empty else np.nan,"rsi":ok.rsi.mean() if not ok.empty else np.nan,"adx":ok.adx.mean() if not ok.empty else np.nan,"trend":ok.trend.mean() if not ok.empty else np.nan,"momentum":ok.momentum.mean() if not ok.empty else np.nan,"timeframes":", ".join(intervals)})
            else:
                d=load(s,intervals[0],limit); sc=score(d); rows.append({"symbol":s,"signal":sc["signal"],"score":sc["total"],"price":sc["price"],"rsi":sc["rsi"],"adx":sc["adx"],"trend":sc["trend"],"momentum":sc["momentum"],"timeframes":intervals[0]})
        except Exception: rows.append({"symbol":s,"signal":"Error","score":0,"price":np.nan,"rsi":np.nan,"adx":np.nan,"trend":np.nan,"momentum":np.nan,"timeframes":""})
        prog.progress((i+1)/max(1,len(symbols)))
    prog.empty(); return pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)

css()
if "favorites" not in st.session_state: st.session_state.favorites=["BTCUSDT","ETHUSDT","SOLUSDT"]
if "portfolio" not in st.session_state: st.session_state.portfolio=pd.DataFrame(columns=["symbol","amount","buy_price"])
if "symbol" not in st.session_state: st.session_state.symbol="BTCUSDT"
if "interval" not in st.session_state: st.session_state.interval="1h"
if "limit" not in st.session_state: st.session_state.limit=500

st.markdown("<div class='topbar'><div class='brand'><span class='dot'></span>Crypto Terminal</div><div class='muted'>Final stable</div></div>", unsafe_allow_html=True)
with st.sidebar:
    st.subheader("Controls")
    st.session_state.symbol = norm(st.text_input("Pair", st.session_state.symbol))
    st.session_state.interval = st.selectbox("Timeframe", INTERVALS, index=INTERVALS.index(st.session_state.interval))
    st.session_state.limit = st.slider("Candles", 120, 1000, int(st.session_state.limit), step=40)
    st.caption("Sidebar is optional. Main controls are duplicated inside pages.")

page = st.radio("Navigation", ["Dashboard","Chart","Multi TF","Scanner","Heatmap","Favorites","Portfolio","Settings"], horizontal=True, label_visibility="collapsed")
symbol=st.session_state.symbol; interval=st.session_state.interval; limit=int(st.session_state.limit)

if page=="Dashboard":
    c1,c2,c3=st.columns([1.2,1,1]); symbol=norm(c1.text_input("Pair", symbol, key="dash_symbol")); interval=c2.selectbox("Timeframe", INTERVALS, index=INTERVALS.index(interval), key="dash_interval"); st.session_state.symbol=symbol; st.session_state.interval=interval
    if c3.button("Add favorite", use_container_width=True) and symbol not in st.session_state.favorites: st.session_state.favorites.append(symbol)
    try:
        df=load(symbol,interval,limit); sc=score(df); t=tickers24(); row=t[t.symbol==symbol]; asset_card(symbol, sc, None if row.empty else row.iloc[0].priceChangePercent)
        cols=st.columns(6)
        for col,(_,r) in zip(cols,t.head(6).iterrows()): col.metric(r.symbol.replace("USDT",""), price_fmt(r.lastPrice), f"{r.priceChangePercent:+.2f}%")
        fig=px.bar(t.head(20).sort_values("priceChangePercent"), x="priceChangePercent", y="symbol", orientation="h", template="plotly_dark")
        fig.update_layout(height=520, margin=dict(l=4,r=4,t=10,b=4), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"); st.plotly_chart(fig, use_container_width=True)
    except Exception as e: st.error(f"Dashboard error: {e}")
elif page=="Chart":
    a,b,c=st.columns([1.2,.8,.8]); symbol=norm(a.text_input("Pair",symbol,key="chart_symbol")); interval=b.selectbox("Timeframe",INTERVALS,index=INTERVALS.index(interval),key="chart_interval"); limit=c.slider("Candles",120,1000,limit,40,key="chart_limit"); st.session_state.symbol=symbol; st.session_state.interval=interval; st.session_state.limit=limit
    with st.expander("Indicators", expanded=False):
        x=st.columns(5); show_ema=x[0].toggle("EMA",True); show_bb=x[1].toggle("Bollinger",False); show_vol=x[2].toggle("Volume",True); show_rsi=x[3].toggle("RSI",True); show_macd=x[4].toggle("MACD",True)
    try:
        df=load(symbol,interval,limit); sc=score(df); asset_card(symbol,sc); st.plotly_chart(fig_chart(df,show_ema,show_bb,show_vol,show_rsi,show_macd),use_container_width=True)
        with st.expander("Indicator values", expanded=False): st.dataframe(df.dropna().tail(1)[["close","rsi","macd","macd_signal","adx","atr","ema20","ema50","ema200"]],use_container_width=True,hide_index=True)
    except Exception as e: st.error(f"Chart error: {e}")
elif page=="Multi TF":
    c1,c2=st.columns([1,1.4]); symbol=norm(c1.text_input("Pair",symbol,key="mtf_symbol")); intervals=c2.multiselect("Timeframes",INTERVALS,default=["5m","15m","1h","4h","1d"]); intervals=intervals or ["1h"]; st.session_state.symbol=symbol
    df=mtf(symbol,intervals,min(limit,500)); avg=int(df[df.signal!="Error"].score.mean()) if (df.signal!="Error").any() else 0; sig="Strong Buy" if avg>=82 else "Buy" if avg>=64 else "Strong Sell" if avg<=24 and avg>0 else "Sell" if avg<=42 and avg>0 else "Neutral"
    st.markdown(f"<div class='asset'><div class='asset-row'><div><div class='sym'>{symbol}</div><div class='price'>{avg}</div><div class='muted'>Multi-timeframe score</div></div><div>{badge_html(sig)}</div></div></div>", unsafe_allow_html=True)
    scan_cards(df.rename(columns={"timeframe":"symbol"}), "symbol")
    with st.expander("Table", expanded=True): st.dataframe(df,use_container_width=True,hide_index=True)
elif page=="Scanner":
    s1,s2,s3=st.columns(3); source=s1.selectbox("Universe",["Top Binance volume","Default list","Favorites","Custom"]); count=s2.slider("Pairs",5,80,20,5); mode=s3.selectbox("Mode",["Single TF","Multi TF"])
    if source=="Top Binance volume": symbols=top_symbols(count)
    elif source=="Favorites": symbols=st.session_state.favorites[:count]
    elif source=="Custom": symbols=[norm(x) for x in st.text_area("Pairs","BTCUSDT, ETHUSDT, SOLUSDT").replace("\n",",").split(",") if norm(x)][:count]
    else: symbols=DEFAULT_SYMBOLS[:count]
    if mode=="Single TF": intervals=[st.selectbox("Scan timeframe",INTERVALS,index=INTERVALS.index(interval))]; multi=False
    else: intervals=st.multiselect("Scan timeframes",INTERVALS,default=["15m","1h","4h","1d"]); intervals=intervals or ["1h"]; multi=True
    if st.button("Run scanner",type="primary",use_container_width=True): st.session_state.scan_result=run_scanner(symbols,intervals,min(limit,500),multi)
    if "scan_result" in st.session_state: scan_cards(st.session_state.scan_result.head(40));
    if "scan_result" in st.session_state:
        with st.expander("Table", expanded=False): st.dataframe(st.session_state.scan_result,use_container_width=True,hide_index=True)
elif page=="Heatmap":
    try:
        n=st.slider("Pairs",20,100,60,10); t=tickers24().head(n); fig=px.treemap(t,path=["symbol"],values="quoteVolume",color="priceChangePercent",color_continuous_scale="RdYlGn"); fig.update_layout(template="plotly_dark",height=720,margin=dict(l=4,r=4,t=8,b=4),paper_bgcolor="rgba(0,0,0,0)"); st.plotly_chart(fig,use_container_width=True)
    except Exception as e: st.error(f"Heatmap error: {e}")
elif page=="Favorites":
    a,b=st.columns(2); add=norm(a.text_input("Add pair",symbol,key="fav_add"));
    if b.button("Add",use_container_width=True) and add not in st.session_state.favorites: st.session_state.favorites.append(add); st.rerun()
    st.markdown(" ".join([f"<span class='pill'>{x}</span>" for x in st.session_state.favorites]), unsafe_allow_html=True)
    rem=st.selectbox("Remove",[""]+st.session_state.favorites)
    if st.button("Remove selected") and rem: st.session_state.favorites=[x for x in st.session_state.favorites if x!=rem]; st.rerun()
    if st.session_state.favorites: scan_cards(run_scanner(st.session_state.favorites,[interval],min(limit,400),False))
elif page=="Portfolio":
    c1,c2,c3=st.columns(3); ps=norm(c1.text_input("Pair","BTCUSDT",key="p_symbol")); amount=c2.number_input("Amount",min_value=0.0,value=0.01,step=0.01,format="%.8f"); buy=c3.number_input("Buy price",min_value=0.0,value=50000.0,step=100.0)
    if st.button("Add position",use_container_width=True): st.session_state.portfolio=pd.concat([st.session_state.portfolio,pd.DataFrame([{"symbol":ps,"amount":amount,"buy_price":buy}])],ignore_index=True)
    pf=st.session_state.portfolio.copy()
    if pf.empty: st.info("Portfolio is empty")
    else:
        prices=[]
        for s in pf.symbol:
            try: prices.append(float(klines(s,"1h",2).iloc[-1].close))
            except Exception: prices.append(np.nan)
        pf["current_price"]=prices; pf["cost"]=pf.amount*pf.buy_price; pf["value"]=pf.amount*pf.current_price; pf["pnl"]=pf.value-pf.cost; pf["pnl_%"]=pf.pnl/pf.cost.replace(0,np.nan)*100
        st.metric("Portfolio value",price_fmt(pf.value.sum()),f"{pf.pnl.sum():+.2f}"); st.dataframe(pf,use_container_width=True,hide_index=True)
        if st.button("Clear portfolio"): st.session_state.portfolio=st.session_state.portfolio.iloc[0:0]; st.rerun()
else:
    st.subheader("Settings"); st.write("Market data: Binance public API"); st.write("Navigation: main page tabs"); st.write("Sidebar: optional controls"); st.write("Signals: analytical score, not financial advice")
