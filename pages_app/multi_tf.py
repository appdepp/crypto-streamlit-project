from __future__ import annotations

import pandas as pd
import streamlit as st
from components.layout import aggregate_card, section, timeframe_cards
from services.binance import get_klines
from services.indicators import add_indicators
from services.scoring import score_market


def _bias(avg: int) -> str:
    if avg >= 82:
        return "Strong Buy"
    if avg >= 66:
        return "Buy"
    if avg <= 28:
        return "Strong Sell"
    if avg <= 42:
        return "Sell"
    return "Neutral"


def analyze_symbol_timeframes(symbol: str, timeframes: list[str], limit: int = 420) -> tuple[list[dict], int, str]:
    rows = []
    for tf in timeframes:
        df = add_indicators(get_klines(symbol, tf, min(limit, 700)))
        sc = score_market(df)
        rows.append({
            "symbol": symbol,
            "timeframe": tf,
            "score": sc["total"],
            "signal": sc["signal"],
            "price": sc["price"],
            "rsi": round(sc["rsi"], 1),
            "adx": round(sc["adx"], 1),
            "trend": sc["trend"],
            "momentum": sc["momentum"],
            "volume": sc["volume"],
        })
    avg = int(round(sum(r["score"] for r in rows) / max(1, len(rows))))
    return rows, avg, _bias(avg)


def render(symbol: str, timeframes: list[str], limit: int):
    section("Multi-timeframe", "Один актив на нескольких таймфреймах")
    rows, avg, bias = analyze_symbol_timeframes(symbol, timeframes, limit)
    aggregate_card(symbol, avg, bias, rows)
    timeframe_cards(rows)
    with st.expander("Таблица таймфреймов"):
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
