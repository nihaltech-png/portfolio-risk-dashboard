"""
app.py
Streamlit dashboard for portfolio risk analysis, with benchmark comparison.
"""

import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from data_loader import load_price_data, calculate_returns
from metrics import (
    portfolio_returns,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
    beta,
)

st.set_page_config(page_title="Portfolio Risk Dashboard", layout="wide", page_icon="📊")

st.title("📊 Portfolio Risk Dashboard")
st.caption("Track returns, volatility, and risk-adjusted performance for a custom stock portfolio.")

# --- Sidebar inputs ---
st.sidebar.header("Portfolio Settings")

tickers_input = st.sidebar.text_input("Tickers (comma-separated)", "AAPL, MSFT, JPM")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

benchmark_ticker = st.sidebar.text_input("Benchmark ticker", "^GSPC")

st.sidebar.subheader("Weights (%)")
weights = {}
if tickers:
    default_weight = round(100 / len(tickers), 1)
    for ticker in tickers:
        weights[ticker] = st.sidebar.number_input(
            ticker, min_value=0.0, max_value=100.0, value=default_weight
        ) / 100

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
run_clicked = st.sidebar.button("Run Analysis", type="primary")

# --- Validation before doing any work ---
def validate_inputs(tickers, weights):
    errors = []
    if not tickers:
        errors.append("Enter at least one ticker.")
    total_weight = sum(weights.values()) if weights else 0
    if weights and abs(total_weight - 1.0) > 0.01:
        errors.append(f"Weights should add up to 100% (currently {total_weight * 100:.1f}%).")
    return errors


if run_clicked:
    validation_errors = validate_inputs(tickers, weights)

    if validation_errors:
        for err in validation_errors:
            st.error(err)
    else:
        try:
            with st.spinner("Fetching data..."):
                all_tickers = tickers + [benchmark_ticker]
                prices = load_price_data(all_tickers, start=str(start_date))

                # Separate benchmark from portfolio tickers
                missing = [t for t in all_tickers if t not in prices.columns]
                if missing:
                    st.warning(f"No data found for: {', '.join(missing)}. Check the ticker symbol(s).")

                available_tickers = [t for t in tickers if t in prices.columns]
                if not available_tickers:
                    st.error("None of your portfolio tickers returned data. Please check the symbols and try again.")
                    st.stop()

                returns = calculate_returns(prices)
                port_returns = portfolio_returns(returns, {t: weights[t] for t in available_tickers})

                has_benchmark = benchmark_ticker in returns.columns
                bench_returns = returns[benchmark_ticker] if has_benchmark else None

            # --- Metrics ---
            cols = st.columns(4 if has_benchmark else 3)
            cols[0].metric("Annualized Volatility", f"{annualized_volatility(port_returns):.2%}")
            cols[1].metric("Sharpe Ratio", f"{sharpe_ratio(port_returns):.2f}")
            cols[2].metric("Max Drawdown", f"{max_drawdown(port_returns):.2%}")
            if has_benchmark:
                port_beta = beta(port_returns, bench_returns)
                cols[3].metric("Beta vs. Benchmark", f"{port_beta:.2f}")

            st.divider()

            # --- Charts ---
            st.subheader("Cumulative Growth: Portfolio vs. Benchmark")
            cumulative = (1 + port_returns).cumprod()
            cumulative.name = "Portfolio"
            if has_benchmark:
                bench_cumulative = (1 + bench_returns).cumprod()
                bench_cumulative.name = "Benchmark"
                chart_df = pd.concat([cumulative, bench_cumulative], axis=1)
            else:
                chart_df = cumulative.to_frame()
            st.line_chart(chart_df)

            st.subheader("Individual Stock Prices")
            st.line_chart(prices[available_tickers])

            st.subheader("Correlation Matrix")
            st.dataframe(returns[available_tickers].corr().style.background_gradient(cmap="coolwarm"))

        except Exception as e:
            st.error(f"Something went wrong while fetching or processing data: {e}")

else:
    st.info("Set your portfolio in the sidebar and click **Run Analysis**.")