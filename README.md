# 📊 Portfolio Risk Dashboard

An interactive dashboard for analyzing stock portfolio performance and risk — built with Python, pandas, and Streamlit. Tracks returns, volatility, Sharpe ratio, max drawdown, and beta against a benchmark, with live data pulled from Yahoo Finance.

## Features
- Live historical price data via `yfinance` (no manual data downloads needed)
- Automated data cleaning: gap-filling, duplicate removal, and split/dividend adjustment
- Weighted portfolio construction from user-defined tickers and allocations
- Key risk metrics:
  - Annualized Volatility
  - Sharpe Ratio
  - Max Drawdown
  - Beta vs. a benchmark index (default: S&P 500)
- Interactive charts: cumulative portfolio growth vs. benchmark, individual stock prices, and a correlation matrix
- Input validation and error handling for invalid tickers or misconfigured weights

## Tech Stack
- Python
- pandas / NumPy
- yfinance
- Streamlit

## Project Structure
```
portfolio-risk-dashboard/
├── dashboard/
│   └── app.py             # Streamlit dashboard (UI layer)
├── src/
│   ├── data_loader.py     # Fetches and cleans historical price data
│   └── metrics.py         # Calculates portfolio risk/performance metrics
├── requirements.txt
└── README.md
```
