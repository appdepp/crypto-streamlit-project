from __future__ import annotations

import numpy as np
import pandas as pd

from config import DEFAULT_SYMBOLS
from services.binance import get_24h_tickers, get_klines
from services.indicators import add_indicators


def clamp(value) -> int:
    if pd.isna(value):
        return 50
    return int(max(0, min(100, round(value))))


def load_symbol(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    return add_indicators(get_klines(symbol, interval, limit))


def score_market(df: pd.DataFrame) -> dict:
    clean = df.dropna()
    clean = clean if not clean.empty else df
    latest = clean.iloc[-1]

    price = float(latest["close"])
    rsi = float(latest["rsi"]) if not pd.isna(latest["rsi"]) else 50.0
    adx = float(latest["adx"]) if not pd.isna(latest["adx"]) else 20.0

    trend = 50
    trend += 17 if price > latest["ema20"] else -12
    trend += 17 if latest["ema20"] > latest["ema50"] else -12
    trend += 16 if latest["ema50"] > latest["ema200"] else -10
    trend = clamp(trend)

    momentum = 50
    momentum += 16 if 45 <= rsi <= 65 else 5 if 35 <= rsi <= 75 else -12
    momentum += 18 if latest["macd"] > latest["macd_signal"] else -10
    momentum = clamp(momentum)

    volume_average = clean["volume"].tail(30).mean()
    volume = clamp(50 + min(28, ((latest["volume"] / volume_average) - 1) * 28) if volume_average > 0 else 50)

    volatility = clamp(100 - abs((latest["atr"] / price * 100 if price else 2) - 2) * 12) if not pd.isna(latest["atr"]) else 50
    total = clamp(trend * .32 + momentum * .32 + volume * .16 + volatility * .10 + clamp(adx * 2.1) * .10)

    signal = "Strong Buy" if total >= 82 else "Buy" if total >= 64 else "Strong Sell" if total <= 24 else "Sell" if total <= 42 else "Neutral"
    return {
        "price": price, "rsi": rsi, "adx": adx, "trend": trend, "momentum": momentum,
        "volume": volume, "volatility": volatility, "total": total, "signal": signal,
    }


def top_symbols(count: int) -> list[str]:
    try:
        return get_24h_tickers().head(count)["symbol"].tolist()
    except Exception:
        return DEFAULT_SYMBOLS[:count]


def multi_timeframe(symbol: str, intervals: list[str], limit: int) -> pd.DataFrame:
    rows = []
    for interval in intervals:
        try:
            df = load_symbol(symbol, interval, limit)
            score = score_market(df)
            rows.append({
                "timeframe": interval,
                "signal": score["signal"],
                "score": score["total"],
                "price": score["price"],
                "rsi": round(score["rsi"], 1),
                "adx": round(score["adx"], 1),
                "trend": score["trend"],
                "momentum": score["momentum"],
            })
        except Exception:
            rows.append({"timeframe": interval, "signal": "Error", "score": 0, "price": np.nan, "rsi": np.nan, "adx": np.nan, "trend": 0, "momentum": 0})
    return pd.DataFrame(rows)


def aggregate_signal(avg: int) -> str:
    return "Strong Buy" if avg >= 82 else "Buy" if avg >= 64 else "Strong Sell" if avg <= 24 and avg > 0 else "Sell" if avg <= 42 and avg > 0 else "Neutral"


def run_scanner(symbols: list[str], intervals: list[str], limit: int, multi: bool, progress=None) -> pd.DataFrame:
    rows = []
    for index, symbol in enumerate(symbols):
        try:
            if multi:
                mtf = multi_timeframe(symbol, intervals, limit)
                valid = mtf[mtf["signal"] != "Error"]
                avg = int(valid["score"].mean()) if not valid.empty else 0
                rows.append({
                    "symbol": symbol, "signal": aggregate_signal(avg), "score": avg,
                    "price": valid["price"].iloc[-1] if not valid.empty else np.nan,
                    "rsi": valid["rsi"].mean() if not valid.empty else np.nan,
                    "adx": valid["adx"].mean() if not valid.empty else np.nan,
                    "trend": valid["trend"].mean() if not valid.empty else np.nan,
                    "momentum": valid["momentum"].mean() if not valid.empty else np.nan,
                    "timeframes": ", ".join(intervals),
                })
            else:
                df = load_symbol(symbol, intervals[0], limit)
                score = score_market(df)
                rows.append({
                    "symbol": symbol, "signal": score["signal"], "score": score["total"],
                    "price": score["price"], "rsi": score["rsi"], "adx": score["adx"],
                    "trend": score["trend"], "momentum": score["momentum"], "timeframes": intervals[0],
                })
        except Exception:
            rows.append({"symbol": symbol, "signal": "Error", "score": 0, "price": np.nan, "rsi": np.nan, "adx": np.nan, "trend": np.nan, "momentum": np.nan, "timeframes": ""})
        if progress is not None:
            progress.progress((index + 1) / max(1, len(symbols)))
    return pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
