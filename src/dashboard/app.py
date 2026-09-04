"""
app.py
Streamlit dashboard for portfolio risk analysis.
"""

import sys
import os
import streamlit as st
import pandas as pd

# Allow importing from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from data_loader import load_price_data, calculate_returns
from metrics import (
    portfolio_returns,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
)

st.set_page_config(page_title="Portfolio Risk Dashboard", layout="wide")
st.title("📊 Portfolio Risk Dashboard")

# --- Sidebar inputs ---
st.sidebar.header("Portfolio Settings")
tickers_input = st.sidebar.text_input("Tickers (comma-separated)", "AAPL, MSFT, JPM")
tickers = [t.strip().upper() for t in tickers_input.split(",")]

st.sidebar.subheader("Weights (%)")
weights = {}
default_weight = round(100 / len(tickers), 1)
for ticker in tickers:
    weights[ticker] = st.sidebar.number_input(ticker, min_value=0.0, max_value=100.0, value=default_weight) / 100

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))

# --- Load and process data ---
if st.sidebar.button("Run Analysis"):
    with st.spinner("Fetching data..."):
        prices = load_price_data(tickers, start=str(start_date))
        returns = calculate_returns(prices)
        port_returns = portfolio_returns(returns, weights)

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Annualized Volatility", f"{annualized_volatility(port_returns):.2%}")
    col2.metric("Sharpe Ratio", f"{sharpe_ratio(port_returns):.2f}")
    col3.metric("Max Drawdown", f"{max_drawdown(port_returns):.2%}")

    # --- Charts ---
    st.subheader("Cumulative Portfolio Growth")
    cumulative = (1 + port_returns).cumprod()
    st.line_chart(cumulative)

    st.subheader("Individual Stock Prices")
    st.line_chart(prices)

    st.subheader("Correlation Matrix")
    st.dataframe(returns.corr().style.background_gradient(cmap="coolwarm"))

else:
    st.info("Set your portfolio in the sidebar and click **Run Analysis**.")