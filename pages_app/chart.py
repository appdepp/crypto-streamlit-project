from __future__ import annotations

import pandas as pd
import streamlit as st
from components.charts import candlestick_chart
from components.layout import asset_card, format_price, score_bars, section, timeframe_cards
from pages_app.multi_tf import analyze_symbol_timeframes
from services.binance import get_klines
from services.indicators import add_indicators
from services.scoring import score_market


def render(symbol: str, interval: str, limit: int, show_ema: bool, show_bb: bool, show_volume: bool, show_rsi: bool, show_macd: bool, timeframes: list[str]):
    df = add_indicators(get_klines(symbol, interval, limit))
    score = score_market(df)
    asset_card(symbol, score["price"], score["signal"], score["total"], score.get("rsi"), score.get("adx"), interval)
    score_bars(score)
    st.plotly_chart(
        candlestick_chart(df, symbol, show_ema=show_ema, show_bb=show_bb, show_volume=show_volume, show_rsi=show_rsi, show_macd=show_macd, compact=True),
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": True},
    )
    section("Timeframes", "Сводка по выбранным таймфреймам")
    tf_rows, _, _ = analyze_symbol_timeframes(symbol, timeframes, min(limit, 500))
    timeframe_cards(tf_rows)
    latest = df.dropna().iloc[-1]
    with st.expander("Индикаторы"):
        st.dataframe(pd.DataFrame([{
            "price": format_price(latest["close"]), "rsi": round(latest["rsi"], 2), "macd": round(latest["macd"], 4),
            "macd_signal": round(latest["macd_signal"], 4), "adx": round(latest["adx"], 2), "atr": round(latest["atr"], 4),
            "ema20": round(latest["ema20"], 4), "ema50": round(latest["ema50"], 4), "ema200": round(latest["ema200"], 4),
        }]), use_container_width=True, hide_index=True)
