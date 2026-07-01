# Crypto Terminal 3.0

Mobile-first Streamlit crypto terminal.

## Features

- Mobile-first layout
- Binance public market data via `data-api.binance.vision`
- Candlestick Plotly chart
- RSI, MACD, EMA 20/50/200, Bollinger Bands, ADX, ATR, Stochastic
- Market scoring
- Scanner
- Heatmap
- Favorites
- Virtual portfolio
- Modular architecture

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Push to GitHub. Streamlit Cloud will redeploy automatically.

```bash
git add .
git commit -m "Upgrade to Crypto Terminal 3.0"
git push
```
