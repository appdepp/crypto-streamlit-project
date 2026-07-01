# Crypto Terminal 2.1

Профессиональная Streamlit-версия крипто-бота: Binance market data, свечные графики, RSI, MACD, EMA, Bollinger Bands, ADX, ATR, Stochastic, скоринг монет, сканер, heatmap, избранное и демо-портфель.

## Запуск локально

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

## Деплой Streamlit Cloud

- Repository: `appdepp/crypto-streamlit-project`
- Branch: `main`
- Main file path: `app.py`

## Обновление GitHub

```bash
git add .
git commit -m "Upgrade to Crypto Terminal 2.1"
git push
```

## Важно

Это аналитический инструмент, а не финансовая рекомендация. Для торговли нужны бэктесты, риск-менеджмент и проверка стратегии.


## v2.1 Mobile-first update

- Mobile-safe navigation via top selectbox instead of overflowing tabs.
- Compact responsive Plotly charts.
- One-column layout on phones.
- Better metric cards and hero block for small screens.
