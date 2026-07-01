from __future__ import annotations

import pandas as pd


def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Wilder RSI as a full pandas Series."""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(100)


def calculate_macd(
    close: pd.Series,
    short_period: int = 12,
    long_period: int = 26,
    signal_period: int = 9,
) -> pd.DataFrame:
    """MACD, signal line and histogram as pandas columns."""
    ema_short = close.ewm(span=short_period, adjust=False).mean()
    ema_long = close.ewm(span=long_period, adjust=False).mean()
    macd = ema_short - ema_long
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return pd.DataFrame({"macd": macd, "signal": signal, "histogram": histogram})


def rsi_signal(value: float, buy_level: float = 40, sell_level: float = 70) -> str:
    if value < buy_level:
        return "🟢 Покупка / перепроданность"
    if value > sell_level:
        return "🔴 Продажа / перекупленность"
    return "🔷 Нейтрально"


def macd_signal(macd: float, signal: float) -> str:
    if macd > signal:
        return "🟢 MACD выше сигнальной"
    if macd < signal:
        return "🔴 MACD ниже сигнальной"
    return "🔷 MACD = сигнальная"


def combined_signal(rsi_text: str, macd_text: str) -> str:
    if rsi_text.startswith("🟢") and macd_text.startswith("🟢"):
        return "🟢 Сильнее в сторону покупки"
    if rsi_text.startswith("🔴") and macd_text.startswith("🔴"):
        return "🔴 Сильнее в сторону продажи"
    if rsi_text.startswith("🔷") and macd_text.startswith("🔷"):
        return "🔷 Нейтрально"
    return "🟡 Смешанный сигнал"
