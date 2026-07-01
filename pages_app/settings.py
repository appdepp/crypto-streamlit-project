from __future__ import annotations

import streamlit as st
from components.layout import section


def render(timeframes: list[str] | None = None):
    section("Settings", "Управление приложением")
    st.markdown("""
    **Панель настроек** — слева. На телефоне её открывает маленькая стрелка `>` в левом верхнем углу страницы.

    **Пара** — торговая пара Binance, например `BTCUSDT`.

    **Таймфрейм графика** — основной график свечей.

    **Таймфреймы анализа** — несколько периодов одновременно для страницы `Multi TF` и multi-TF scanner.

    **Scanner** — анализирует группу top-пар Binance по объёму или твой список избранного.
    """)
    if timeframes:
        st.write("Активные таймфреймы:", ", ".join(timeframes))
    st.warning("Сигналы — аналитический скоринг, не финансовая рекомендация.")
