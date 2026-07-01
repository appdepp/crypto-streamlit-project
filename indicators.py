from __future__ import annotations

import numpy as np
import pandas as pd


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def bollinger(close: pd.Series, period: int = 20, std_mult: float = 2.0):
    mid = close.rolling(period).mean()
    std = close.rolling(period).std()
    upper = mid + std_mult * std
    lower = mid - std_mult * std
    return upper, mid, lower


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    tr = pd.concat([(high - low), (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    plus_dm = high.diff()
    minus_dm = -low.diff()
    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)
    trur = atr(df, period)
    plus_di = 100 * plus_dm.ewm(alpha=1 / period, adjust=False).mean() / trur
    minus_di = 100 * minus_dm.ewm(alpha=1 / period, adjust=False).mean() / trur
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1 / period, adjust=False).mean()


def stochastic(df: pd.DataFrame, period: int = 14, smooth: int = 3):
    low_min = df["low"].rolling(period).min()
    high_max = df["high"].rolling(period).max()
    k = 100 * (df["close"] - low_min) / (high_max - low_min)
    d = k.rolling(smooth).mean()
    return k, d


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema20"] = ema(out["close"], 20)
    out["ema50"] = ema(out["close"], 50)
    out["ema200"] = ema(out["close"], 200)
    out["rsi"] = rsi(out["close"])
    out["macd"], out["macd_signal"], out["macd_hist"] = macd(out["close"])
    out["bb_upper"], out["bb_mid"], out["bb_lower"] = bollinger(out["close"])
    out["adx"] = adx(out)
    out["atr"] = atr(out)
    out["stoch_k"], out["stoch_d"] = stochastic(out)
    out["volume_ma20"] = out["volume"].rolling(20).mean()
    return out


def score_market(df: pd.DataFrame) -> dict:
    row = df.dropna().iloc[-1]
    prev = df.dropna().iloc[-2]
    close = float(row["close"])

    trend = 50
    if close > row["ema20"]: trend += 12
    if close > row["ema50"]: trend += 15
    if close > row["ema200"]: trend += 18
    if row["ema20"] > row["ema50"] > row["ema200"]: trend += 5

    momentum = 50
    if row["rsi"] > 55: momentum += 18
    elif row["rsi"] < 45: momentum -= 18
    if row["macd"] > row["macd_signal"]: momentum += 18
    else: momentum -= 12
    if row["macd_hist"] > prev["macd_hist"]: momentum += 8

    volume = 50
    if row["volume"] > row["volume_ma20"]: volume += 20
    if row["volume"] > row["volume_ma20"] * 1.5: volume += 15

    volatility = 70
    if row["adx"] > 25: volatility += 15
    if row["adx"] < 15: volatility -= 15
    if close > row["bb_upper"]: volatility -= 8
    if close < row["bb_lower"]: volatility += 5

    parts = {"trend": trend, "momentum": momentum, "volume": volume, "volatility": volatility}
    parts = {k: int(max(0, min(100, v))) for k, v in parts.items()}
    total = int(round(parts["trend"] * 0.35 + parts["momentum"] * 0.35 + parts["volume"] * 0.15 + parts["volatility"] * 0.15))

    if total >= 85:
        signal = "Strong Buy"
    elif total >= 70:
        signal = "Buy"
    elif total >= 45:
        signal = "Neutral"
    elif total >= 30:
        signal = "Sell"
    else:
        signal = "Strong Sell"

    return {
        **parts,
        "total": total,
        "signal": signal,
        "price": close,
        "rsi": float(row["rsi"]),
        "macd_hist": float(row["macd_hist"]),
        "adx": float(row["adx"]),
        "atr": float(row["atr"]),
    }
