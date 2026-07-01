from __future__ import annotations

import numpy as np
import pandas as pd


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(close: pd.Series):
    macd_line = ema(close, 12) - ema(close, 26)
    signal = ema(macd_line, 9)
    hist = macd_line - signal
    return macd_line, signal, hist


def bollinger(close: pd.Series, period: int = 20, width: float = 2.0):
    mid = close.rolling(period).mean()
    std = close.rolling(period).std()
    return mid, mid + width * std, mid - width * std


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high = df["high"]
    low = df["low"]
    close = df["close"]
    plus_dm = high.diff()
    minus_dm = -low.diff()
    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)
    tr = pd.concat([(high-low), (high-close.shift()).abs(), (low-close.shift()).abs()], axis=1).max(axis=1)
    atr_s = tr.rolling(period).mean()
    plus_di = 100 * plus_dm.rolling(period).mean() / atr_s
    minus_di = 100 * minus_dm.rolling(period).mean() / atr_s
    dx = ((plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)) * 100
    return dx.rolling(period).mean()


def stochastic(df: pd.DataFrame, period: int = 14) -> pd.Series:
    low_min = df["low"].rolling(period).min()
    high_max = df["high"].rolling(period).max()
    return 100 * (df["close"] - low_min) / (high_max - low_min).replace(0, np.nan)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ema20"] = ema(df["close"], 20)
    df["ema50"] = ema(df["close"], 50)
    df["ema200"] = ema(df["close"], 200)
    df["rsi"] = rsi(df["close"])
    df["macd"], df["macd_signal"], df["macd_hist"] = macd(df["close"])
    df["bb_mid"], df["bb_upper"], df["bb_lower"] = bollinger(df["close"])
    df["atr"] = atr(df)
    df["adx"] = adx(df)
    df["stoch"] = stochastic(df)
    df["ret_24"] = df["close"].pct_change(24) * 100
    return df
