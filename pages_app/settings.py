from __future__ import annotations

import streamlit as st
from services.binance import get_server_time


def render():
    st.subheader("Settings / README")
    st.info(f"Binance server time: {get_server_time()}")
    st.markdown("""
    **Как обновлять приложение:** измени файлы → `git add .` → `git commit -m "..."` → `git push`.

    **Важно:** сигналы — это аналитический скоринг, а не финансовая рекомендация. Для реальной торговли нужны риск-менеджмент, бэктесты и проверка стратегии.
    """)
