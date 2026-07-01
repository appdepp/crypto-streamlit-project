from __future__ import annotations

import streamlit as st
from components.layout import section


def render():
    section("Settings / README", "Crypto Terminal 4.1: polish update.")
    st.markdown("""
    **Что изменено в 4.1**

    - убрана/спрятана верхняя чёрная полоса Streamlit header;
    - добавлен безопасный верхний отступ для iPhone/Safari;
    - график стал чище: убрана перегруженная легенда;
    - Dashboard-график заменён на горизонтальный bar chart;
    - карточки scanner стали визуально дороже;
    - Dashboard теперь показывает до 6 карточек вместо 4.

    **Обновление:** измени файлы → `git add -A` → `git commit -m "..."` → `git push`.

    Сигналы являются аналитическим скорингом, а не финансовой рекомендацией.
    """)
