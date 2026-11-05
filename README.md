# Market Simulator (Streamlit)

A Python web app that calibrates drift and volatility to real price history and simulates thousands of future price paths with **geometric Brownian motion** or the **Heston** stochastic-volatility model.

**Live app:** [boonwui.github.io/market-simulator](https://boonwui.github.io/market-simulator/). It runs this same `app.py` entirely in your browser with [stlite](https://github.com/whitphx/stlite) (Streamlit on Pyodide/WebAssembly), so there is no server to sleep or pay for. The first load downloads the Python runtime and takes 20–60 seconds.

## Two ways to run

| | In the browser (stlite) | On a server (`streamlit run`) |
|---|---|---|
| Symbols | About 110 Bursa Malaysia and US stocks plus both indices, from the portfolio's [self-updating data](https://github.com/BoonWui/BoonWui.github.io) | Any Yahoo Finance symbol: `AAPL`, `1155.KL`, `BTC-USD`, `CL=F` |
| Prices | Refreshed hourly in market hours by GitHub Actions | Downloaded live with yfinance |

The app detects where it runs (`sys.platform == "emscripten"` in the browser) and picks the data source.

## Features

- Calibration from 6 months to 5 years of history
- Fan chart of percentiles, sample paths, and a histogram of final prices
- Median outcome, 5th–95th percentile range, and the chance of a loss

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech

Python · Streamlit · stlite / Pyodide · NumPy · pandas · Altair · yfinance

Part of [BoonWui's portfolio](https://boonwui.github.io). A JavaScript version is at [boonwui.github.io/monte-carlo](https://boonwui.github.io/monte-carlo/).

> **Disclaimer:** Data and results may be inaccurate. For education only. Use at your own risk. **Not financial advice.**
