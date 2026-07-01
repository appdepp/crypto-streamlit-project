# Crypto RSI/MACD Analyzer — Streamlit версия

Это адаптация Telegram-бота `18.py` под Streamlit.

## Что умеет

- выбор криптовалютной пары из списка;
- ручной ввод пары Binance, например `BTCUSDT`;
- анализ RSI и MACD по нескольким таймфреймам;
- итоговый сигнал по RSI + MACD;
- текущая цена и статистика за 24 часа;
- интерактивный свечной график с SMA 20 / SMA 50;
- работает через публичный Binance REST API, ключи не нужны.

## Установка

```bash
cd crypto_streamlit_project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Для Windows:

```bash
cd crypto_streamlit_project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
streamlit run app.py
```

После запуска Streamlit покажет локальную ссылку, обычно:

```text
http://localhost:8501
```

## Важно

Это аналитический инструмент, а не торговый советник. Сигналы RSI/MACD не гарантируют прибыль.
