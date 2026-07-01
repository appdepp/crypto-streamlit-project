from __future__ import annotations

import pandas as pd


def clamp(value: float, low: int = 0, high: int = 100) -> int:
    return int(max(low, min(high, round(value))))


def score_market(df: pd.DataFrame) -> dict:
    d = df.dropna().copy()
    if d.empty:
        return {"total": 0, "signal": "No data", "trend": 0, "momentum": 0, "volume": 0, "volatility": 0, "adx": 0, "rsi": 0, "price": 0}
    last = d.iloc[-1]
    price = float(last["close"])

    trend = 50
    if price > last["ema20"]: trend += 12
    if price > last["ema50"]: trend += 16
    if price > last["ema200"]: trend += 20
    if last["ema20"] > last["ema50"] > last["ema200"]: trend += 12
    trend = clamp(trend)

    rsi = float(last.get("rsi", 50))
    macd_hist = float(last.get("macd_hist", 0))
    stoch = float(last.get("stoch", 50))
    momentum = 50
    momentum += 18 if 45 <= rsi <= 68 else (-18 if rsi > 78 or rsi < 25 else 4)
    momentum += 18 if macd_hist > 0 else -8
    momentum += 8 if 35 <= stoch <= 82 else -6
    momentum = clamp(momentum)

    recent_vol = d["volume"].tail(20).mean()
    base_vol = d["volume"].tail(120).mean()
    volume = clamp(50 + ((recent_vol / base_vol) - 1) * 55) if base_vol else 50

    atr_pct = float(last.get("atr", 0)) / price * 100 if price else 0
    volatility = clamp(78 - abs(atr_pct - 2.5) * 10)

    adx_value = float(last.get("adx", 0))
    adx_score = clamp(adx_value * 2.2)

    total = clamp(trend * .34 + momentum * .30 + volume * .16 + volatility * .08 + adx_score * .12)
    if total >= 82:
        signal = "Strong Buy"
    elif total >= 66:
        signal = "Buy"
    elif total <= 28:
        signal = "Strong Sell"
    elif total <= 42:
        signal = "Sell"
    else:
        signal = "Neutral"

    return {
        "total": total,
        "signal": signal,
        "trend": trend,
        "momentum": momentum,
        "volume": volume,
        "volatility": volatility,
        "adx_score": adx_score,
        "adx": adx_value,
        "rsi": rsi,
        "stoch": stoch,
        "price": price,
        "atr_pct": atr_pct,
    }
