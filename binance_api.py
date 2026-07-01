from __future__ import annotations

import requests
import pandas as pd

BASE_URL = "https://api.binance.com"


def _get(path: str, params: dict | None = None) -> dict | list:
    response = requests.get(f"{BASE_URL}{path}", params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def validate_symbol(symbol: str) -> bool:
    symbol = symbol.upper().strip()
    try:
        _get("/api/v3/ticker/price", {"symbol": symbol})
        return True
    except requests.HTTPError:
        return False


def get_symbol_price(symbol: str) -> float:
    data = _get("/api/v3/ticker/price", {"symbol": symbol.upper().strip()})
    return float(data["price"])


def get_24h_ticker(symbol: str) -> dict:
    data = _get("/api/v3/ticker/24hr", {"symbol": symbol.upper().strip()})
    return {
        "price_change_percent": float(data["priceChangePercent"]),
        "volume": float(data["volume"]),
        "quote_volume": float(data["quoteVolume"]),
        "high_price": float(data["highPrice"]),
        "low_price": float(data["lowPrice"]),
    }


def get_klines(symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
    raw = _get(
        "/api/v3/klines",
        {"symbol": symbol.upper().strip(), "interval": interval, "limit": int(limit)},
    )
    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore",
    ]
    df = pd.DataFrame(raw, columns=columns)
    numeric_cols = ["open", "high", "low", "close", "volume", "quote_asset_volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df
