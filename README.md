# Market Simulator (Streamlit)

A Python web app that downloads live prices from Yahoo Finance, calibrates drift and volatility, and simulates thousands of future price paths with **geometric Brownian motion** or the **Heston** stochastic-volatility model.

**Live app:** deploy on Streamlit Community Cloud (link added after deployment)

## Features

- Any Yahoo Finance symbol: stocks (`AAPL`, `1155.KL`), crypto (`BTC-USD`) and futures (`CL=F`)
- Calibration from 6 months to 5 years of history
- Fan chart of percentiles, sample paths, and a histogram of final prices
- Median outcome, 5th–95th percentile range, and the chance of a loss

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech

Python · Streamlit · yfinance · NumPy · pandas · Plotly

> For education only. Not financial advice.

Part of [BoonWui's portfolio](https://boonwui.github.io). A browser-only version is at [boonwui.github.io/monte-carlo](https://boonwui.github.io/monte-carlo/).

> **Disclaimer:** Data and results may be inaccurate. For education only. Use at your own risk. **Not financial advice.**
