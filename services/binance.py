from __future__ import annotations

import requests
import pandas as pd
import streamlit as st
from config import BINANCE_BASE_URL


class BinanceDataError(RuntimeError):
    pass


@st.cache_data(ttl=45, show_spinner=False)
def _get_json(path: str, params: tuple[tuple[str, str | int], ...] = ()):
    url = BINANCE_BASE_URL + path
    try:
        response = requests.get(url, params=dict(params), timeout=15)
    except requests.RequestException as exc:
        raise BinanceDataError(f"Binance API недоступен: {exc}") from exc
    if response.status_code != 200:
        raise BinanceDataError(f"Binance API error {response.status_code}: {response.text[:180]}")
    return response.json()


@st.cache_data(ttl=45, show_spinner=False)
def get_klines(symbol: str, interval: str = "1h", limit: int = 500) -> pd.DataFrame:
    symbol = symbol.upper().replace("/", "").strip()
    data = _get_json("/api/v3/klines", (("symbol", symbol), ("interval", interval), ("limit", int(limit))))
    if not isinstance(data, list) or len(data) == 0:
        raise BinanceDataError(f"Пара {symbol} не найдена или Binance не вернул свечи.")
    columns = [
        "open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
        "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ]
    df = pd.DataFrame(data, columns=columns)
    numeric = ["open", "high", "low", "close", "volume", "quote_asset_volume", "taker_buy_base", "taker_buy_quote"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df.dropna(subset=["close"])


@st.cache_data(ttl=60, show_spinner=False)
def get_24h_tickers() -> pd.DataFrame:
    data = _get_json("/api/v3/ticker/24hr")
    df = pd.DataFrame(data)
    if df.empty:
        return df
    keep = ["symbol", "lastPrice", "priceChangePercent", "quoteVolume", "volume", "count"]
    df = df[[c for c in keep if c in df.columns]].copy()
    for col in ["lastPrice", "priceChangePercent", "quoteVolume", "volume", "count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[df["symbol"].str.endswith("USDT")]
    df = df[~df["symbol"].str.contains("UPUSDT|DOWNUSDT|BULLUSDT|BEARUSDT", regex=True)]
    return df.sort_values("quoteVolume", ascending=False).reset_index(drop=True)


@st.cache_data(ttl=300, show_spinner=False)
def get_server_time() -> str:
    try:
        data = _get_json("/api/v3/time")
        return pd.to_datetime(data["serverTime"], unit="ms").strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "n/a"
