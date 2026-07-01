from __future__ import annotations

import streamlit as st
from components.layout import section


def render():
    section("Settings / README", "Crypto Terminal 4.0: mobile-first UI/UX.")
    st.markdown("""
    **Что изменено в 4.0**

    - большая hero-шапка заменена на компактную верхнюю панель;
    - карточка актива стала главным элементом экрана;
    - gauge-графики заменены горизонтальными score-барами;
    - scanner теперь показывает мобильные карточки;
    - график стал легче и не перегружает телефон;
    - старые таблицы спрятаны в expander.

    **Обновление:** измени файлы → `git add -A` → `git commit -m "..."` → `git push`.

    Сигналы являются аналитическим скорингом, а не финансовой рекомендацией.
    """)
