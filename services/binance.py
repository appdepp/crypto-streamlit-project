from __future__ import annotations

import requests
import pandas as pd
import streamlit as st

from config import BASE_URLS, STABLE_EXCLUDE


def normalize_symbol(symbol: str) -> str:
    return symbol.upper().replace("/", "").replace("-", "").strip()


def _get_json(path: str, params: dict | None = None):
    last_error: Exception | None = None
    for base in BASE_URLS:
        try:
            response = requests.get(base + path, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Market data unavailable: {last_error}")


@st.cache_data(ttl=60, show_spinner=False)
def get_24h_tickers() -> pd.DataFrame:
    df = pd.DataFrame(_get_json("/api/v3/ticker/24hr"))
    if df.empty or "symbol" not in df.columns:
        raise RuntimeError("Ticker list is empty")
    for col in ["lastPrice", "priceChangePercent", "quoteVolume", "volume", "highPrice", "lowPrice"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[df["symbol"].str.endswith("USDT")]
    df = df[~df["symbol"].isin(STABLE_EXCLUDE)]
    df = df[~df["symbol"].str.contains("UPUSDT|DOWNUSDT|BULLUSDT|BEARUSDT", regex=True)]
    return df.sort_values("quoteVolume", ascending=False).reset_index(drop=True)


@st.cache_data(ttl=60, show_spinner=False)
def get_klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    symbol = normalize_symbol(symbol)
    data = _get_json("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": int(limit)})
    cols = [
        "open_time", "open", "high", "low", "close", "volume", "close_time",
        "quote_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore",
    ]
    df = pd.DataFrame(data, columns=cols)
    if df.empty:
        raise ValueError(f"Pair not found: {symbol}")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    for col in ["open", "high", "low", "close", "volume", "quote_volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[["open_time", "open", "high", "low", "close", "volume", "quote_volume"]]


def clear_market_cache() -> None:
    get_24h_tickers.clear()
    get_klines.clear()
