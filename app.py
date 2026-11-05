"""Market Simulator: Monte Carlo price paths from live Yahoo Finance data (Streamlit)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Market Simulator", page_icon="📈", layout="wide")
st.title("Market Simulator")
st.warning("**Disclaimer:** Data may be delayed, incomplete or inaccurate. For education and research only; use at your own risk. **Not financial advice.**")
st.caption("Monte Carlo price paths calibrated to live Yahoo Finance data · by [BoonWui](https://boonwui.github.io)")

with st.sidebar:
    st.header("Inputs")
    ticker = st.text_input("Ticker", "AAPL", help="Any Yahoo Finance symbol, e.g. AAPL, 1155.KL, BTC-USD, CL=F").strip().upper()
    lookback = st.select_slider("History used for calibration", ["6mo", "1y", "2y", "5y"], value="2y")
    model = st.radio("Model", ["GBM", "Heston"], horizontal=True)
    days = st.slider("Days to simulate", 20, 504, 252)
    paths = st.slider("Paths", 500, 10000, 3000, step=500)
    seed = st.number_input("Random seed", 1, 10**6, 42)
    if model == "Heston":
        kappa = st.slider("Reversion speed κ", 0.1, 10.0, 2.0)
        xi = st.slider("Vol of vol ξ", 0.05, 1.5, 0.5)
        rho = st.slider("Correlation ρ", -0.95, 0.95, -0.6)


@st.cache_data(ttl=3600, show_spinner="Downloading prices…")
def load(sym: str, period: str) -> pd.Series:
    df = yf.download(sym, period=period, auto_adjust=True, progress=False)
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close.dropna()


try:
    px = load(ticker, lookback)
except Exception as exc:  # network or symbol errors
    st.error(f"Could not download {ticker}: {exc}")
    st.stop()
if len(px) < 30:
    st.error(f"Not enough price history for {ticker}. Check the symbol.")
    st.stop()

ret = np.log(px / px.shift(1)).dropna()
mu, sigma, s0 = float(ret.mean() * 252), float(ret.std() * np.sqrt(252)), float(px.iloc[-1])
rng = np.random.default_rng(int(seed))
dt = 1 / 252

S = np.full(paths, s0)
v = np.full(paths, sigma**2)
out = np.empty((days + 1, paths))
out[0] = s0
for t in range(1, days + 1):
    z1 = rng.standard_normal(paths)
    if model == "Heston":
        z2 = rho * z1 + np.sqrt(1 - rho**2) * rng.standard_normal(paths)
        vp = np.maximum(v, 0)
        S = S * np.exp((mu - 0.5 * vp) * dt + np.sqrt(vp * dt) * z1)
        v = v + kappa * (sigma**2 - vp) * dt + xi * np.sqrt(vp * dt) * z2  # full-truncation Euler
    else:
        S = S * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z1)
    out[t] = S

final = out[-1]
pct = np.percentile(out, [5, 25, 50, 75, 95], axis=1)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Last price", f"{s0:,.2f}")
c2.metric("Median at end", f"{np.median(final):,.2f}", f"{(np.median(final) / s0 - 1) * 100:+.1f}%")
c3.metric("5th–95th percentile", f"{pct[0, -1]:,.0f} – {pct[4, -1]:,.0f}")
c4.metric("Chance of a loss", f"{(final < s0).mean() * 100:.1f}%")
c5.metric("Calibrated vol / drift", f"{sigma * 100:.1f}% / {mu * 100:+.1f}%")

x = np.arange(days + 1)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=pct[4], line=dict(width=0), showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=x, y=pct[0], fill="tonexty", fillcolor="rgba(31,111,74,0.15)", line=dict(width=0), name="5th–95th"))
fig.add_trace(go.Scatter(x=x, y=pct[3], line=dict(width=0), showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=x, y=pct[1], fill="tonexty", fillcolor="rgba(31,111,74,0.30)", line=dict(width=0), name="25th–75th"))
for i in range(min(15, paths)):
    fig.add_trace(go.Scatter(x=x, y=out[:, i], line=dict(width=0.7, color="rgba(45,100,168,0.45)"), showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=x, y=pct[2], line=dict(width=3, color="#1f6f4a"), name="Median"))
fig.update_layout(title=f"{ticker}: {paths:,} simulated paths ({model})", xaxis_title="Trading days ahead", yaxis_title="Price", height=480, margin=dict(t=50, b=40))
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Where prices end up")
    st.plotly_chart(go.Figure(go.Histogram(x=final, nbinsx=60, marker_color="#1f6f4a")).update_layout(height=320, margin=dict(t=10, b=30), xaxis_title="Final price"), use_container_width=True)
with right:
    st.subheader("History used")
    st.line_chart(px, height=320)

st.caption("A model of uncertainty, not a forecast. Calibrated drift from past returns is a weak guide to the future. Not financial advice.")
