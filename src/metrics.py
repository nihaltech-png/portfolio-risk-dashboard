"""
metrics.py
Calculates portfolio risk and performance metrics from daily returns.
"""

import numpy as np
import pandas as pd


def portfolio_returns(returns, weights):
    """
    Combines individual stock returns into a single weighted portfolio return series.
    'weights' should be a dict like {"AAPL": 0.4, "MSFT": 0.3, "JPM": 0.3}
    """
    weights_series = pd.Series(weights)
    return returns[weights_series.index].dot(weights_series)


def annualized_volatility(returns, trading_days=252):
    """Annualized standard deviation of returns."""
    return returns.std() * np.sqrt(trading_days)


def sharpe_ratio(returns, risk_free_rate=0.02, trading_days=252):
    """
    Annualized Sharpe Ratio: excess return over risk-free rate, divided by volatility.
    risk_free_rate is annual (e.g. 0.02 = 2%).
    """
    excess_daily_return = returns.mean() * trading_days - risk_free_rate
    vol = annualized_volatility(returns, trading_days)
    return excess_daily_return / vol


def max_drawdown(returns):
    """
    Largest peak-to-trough decline in cumulative portfolio value.
    Returns a negative number (e.g. -0.23 = a 23% drawdown).
    """
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min()


def beta(portfolio_returns, benchmark_returns):
    """Portfolio's sensitivity to benchmark (e.g. S&P 500) movements."""
    covariance = np.cov(portfolio_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    return covariance / benchmark_variance


if __name__ == "__main__":
    from data_loader import load_price_data, calculate_returns

    tickers = ["AAPL", "MSFT", "JPM"]
    weights = {"AAPL": 0.4, "MSFT": 0.3, "JPM": 0.3}

    prices = load_price_data(tickers)
    returns = calculate_returns(prices)
    port_returns = portfolio_returns(returns, weights)

    print("Annualized Volatility:", round(annualized_volatility(port_returns), 4))
    print("Sharpe Ratio:", round(sharpe_ratio(port_returns), 4))
    print("Max Drawdown:", round(max_drawdown(port_returns), 4))