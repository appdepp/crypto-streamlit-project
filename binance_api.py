from __future__ import annotations

import time
from typing import Any

import pandas as pd
import requests
import streamlit as st

from config import BASE_URLS


class BinanceDataError(RuntimeError):
    pass


def _request(path: str, params: dict[str, Any] | None = None) -> Any:
    last_error = None
    for base_url in BASE_URLS:
        try:
            response = requests.get(f"{base_url}{path}", params=params, timeout=12)
            if response.status_code == 451:
                last_error = "Binance заблокировал регион/IP этого сервера."
                continue
            response.raise_for_status()
            return response.json()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise BinanceDataError(f"Не удалось получить данные Binance: {last_error}")


@st.cache_data(ttl=60, show_spinner=False)
def get_klines(symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
    symbol = symbol.upper().strip().replace("/", "")
    data = _request("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": limit})
    if not isinstance(data, list) or not data:
        raise BinanceDataError(f"Пара {symbol} не найдена или Binance не вернул свечи.")

    columns = [
        "open_time", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base_volume",
        "taker_buy_quote_volume", "ignore",
    ]
    df = pd.DataFrame(data, columns=columns)
    numeric_cols = ["open", "high", "low", "close", "volume", "quote_asset_volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df


@st.cache_data(ttl=60, show_spinner=False)
def get_24h_tickers() -> pd.DataFrame:
    data = _request("/api/v3/ticker/24hr")
    df = pd.DataFrame(data)
    if df.empty:
        return df
    numeric = ["lastPrice", "priceChangePercent", "quoteVolume", "volume", "highPrice", "lowPrice"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[df["symbol"].str.endswith("USDT")]
    df = df[~df["symbol"].str.contains("UPUSDT|DOWNUSDT|BULLUSDT|BEARUSDT", regex=True)]
    return df.sort_values("quoteVolume", ascending=False).reset_index(drop=True)


def validate_symbol(symbol: str) -> bool:
    try:
        get_klines(symbol, "1d", 2)
        return True
    except Exception:
        return False


def get_server_time() -> str:
    try:
        data = _request("/api/v3/time")
        ts = pd.to_datetime(data["serverTime"], unit="ms")
        return ts.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
