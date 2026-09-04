"""
data_loader.py
Pulls historical stock price data and cleans it for portfolio analysis.
"""

import pandas as pd
import yfinance as yf


def load_price_data(tickers, start="2020-01-01", end=None):
    """
    Downloads historical Close prices for a list of tickers,
    cleans the data, and returns a single DataFrame (Date x Ticker).
    """
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True)

    # Pull just the Close prices (already split/dividend-adjusted)
    prices = raw["Close"]

    # --- Cleaning steps ---
    prices = prices[~prices.index.duplicated(keep="first")]  # drop duplicate dates
    prices = prices.ffill()                                   # forward-fill small gaps
    prices = prices.dropna()                                   # align all tickers to common start date

    return prices


def calculate_returns(prices):
    """Converts price data into daily percentage returns."""
    return prices.pct_change().dropna()


if __name__ == "__main__":
    # Example portfolio — swap these for your own tickers
    tickers = ["AAPL", "MSFT", "JPM"]

    prices = load_price_data(tickers)
    returns = calculate_returns(prices)

    print(prices.tail())
    print(returns.tail())