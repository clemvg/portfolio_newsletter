#!/usr/bin/env python3
"""
Yahoo Finance Metrics Extraction Module

This module provides functionality to extract key stock market metrics from Yahoo Finance
for multiple tickers and format the results for use in reports and analysis.

Key Metrics Extracted:
- Volatility: 10-day price range as a percentage, calculated as ((high - low) / low) * 100
- Average Price Movement: 50-day Simple Moving Average (SMA) of closing prices
- Momentum: 10-day price change percentage, showing recent trend direction
- Volume: Current volume relative to 10-day average volume (ratio)

The module supports:
- Batch processing of multiple tickers
- DataFrame output for easy manipulation
- Markdown table formatting for documentation and reports
- Error handling for individual ticker failures

Usage:
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    df = extract_metrics(tickers)
    markdown_output = metrics_to_markdown(df)

Author: Clément Van Goethem
Date: 2025-10-04
"""
import yfinance as yf
import pandas as pd
from typing import List, Dict

def calculate_volatility(ticker: str, days: int = 10) -> float:
    """
    Calculate volatility as 10-day price range in percentage
    Formula: ((high - low) / low) * 100 over the period

    Yahoo Finance API Parameters:
        - period: String format "{days}d" (e.g., "10d" for 10 days)
          Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

    Yahoo Finance Response Structure:
        stock.history() returns a pandas DataFrame with columns:
        - 'Open': Opening price for the period
        - 'High': Highest price for the period
        - 'Low': Lowest price for the period
        - 'Close': Closing price for the period
        - 'Volume': Trading volume
        - 'Dividends': Dividend payments (if any)
        - 'Stock Splits': Stock split information (if any)
        Index: DatetimeIndex with trading dates

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        days (int): Number of days for volatility calculation (default: 10)

    Returns:
        float: Volatility percentage rounded to 2 decimals, or None if error/no data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=f"{days}d")

        if hist.empty:
            return None

        high = hist['High'].max()
        low = hist['Low'].min()

        volatility = ((high - low) / low) * 100
        return round(volatility, 2)
    except Exception as e:
        print(f"Error calculating volatility for {ticker}: {e}")
        return None


def calculate_sma_50(ticker: str) -> float:
    """
    Calculate 50-day simple moving average

    Yahoo Finance API Parameters:
        - period: "60d" (fetches 60 days to ensure we have at least 50 trading days)

    Yahoo Finance Response Structure:
        stock.history() returns a pandas DataFrame with columns:
        - 'Close': Closing prices used for SMA calculation
        - Other columns: Open, High, Low, Volume, Dividends, Stock Splits
        Index: DatetimeIndex with trading dates (excludes weekends/holidays)

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        float: 50-day SMA price rounded to 2 decimals, or None if insufficient data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="60d")  # Get a bit more to ensure 50 days

        if len(hist) < 50:
            return None

        sma_50 = hist['Close'].tail(50).mean()
        return round(sma_50, 2)
    except Exception as e:
        print(f"Error calculating SMA for {ticker}: {e}")
        return None


def calculate_momentum(ticker: str, days: int = 10) -> float:
    """
    Calculate momentum as 10-day price change percentage
    Formula: ((current_price - price_10_days_ago) / price_10_days_ago) * 100

    Yahoo Finance API Parameters:
        - period: "{days + 5}d" (e.g., "15d" for 10-day momentum)
          Extra days fetched to account for weekends/holidays

    Yahoo Finance Response Structure:
        stock.history() returns a pandas DataFrame with:
        - 'Close': Closing prices for momentum calculation
        - Index: DatetimeIndex (only trading days, no weekends/holidays)
        - iloc[-1]: Most recent closing price
        - iloc[-(days+1)]: Closing price from 'days' trading days ago

    Args:
        ticker (str): Stock ticker symbol (e.g., 'TSLA', 'AMZN')
        days (int): Number of trading days for momentum calculation (default: 10)

    Returns:
        float: Momentum percentage rounded to 2 decimals, or None if insufficient data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=f"{days + 5}d")  # Get extra days for safety

        if len(hist) < days:
            return None

        current_price = hist['Close'].iloc[-1]
        past_price = hist['Close'].iloc[-(days + 1)]

        momentum = ((current_price - past_price) / past_price) * 100
        return round(momentum, 2)
    except Exception as e:
        print(f"Error calculating momentum for {ticker}: {e}")
        return None


def calculate_volume_ratio(ticker: str, days: int = 10) -> float:
    """
    Calculate volume ratio: current volume vs 10-day average volume
    Formula: current_volume / avg_10_day_volume

    Yahoo Finance API Parameters:
        - period: "{days + 5}d" (e.g., "15d" for 10-day average)
          Extra days to ensure sufficient trading day data

    Yahoo Finance Response Structure:
        stock.history() returns a pandas DataFrame with:
        - 'Volume': Number of shares traded per day (integer)
        - Index: DatetimeIndex with trading dates
        - .tail(days): Last 'days' rows for average calculation
        - .iloc[-1]: Most recent day's volume

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        days (int): Number of days for average volume calculation (default: 10)

    Returns:
        float: Volume ratio (current/average) rounded to 2 decimals, or None if error
        - Ratio > 1.0: Above average volume (higher trading activity)
        - Ratio < 1.0: Below average volume (lower trading activity)
        - Ratio = 1.0: Equal to average volume
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=f"{days + 5}d")

        if len(hist) < days:
            return None

        current_volume = hist['Volume'].iloc[-1]
        avg_volume = hist['Volume'].tail(days).mean()

        volume_ratio = current_volume / avg_volume
        return round(volume_ratio, 2)
    except Exception as e:
        print(f"Error calculating volume ratio for {ticker}: {e}")
        return None


def extract_metrics(tickers: List[str]) -> pd.DataFrame:
    """
    Extract all four metrics for a list of tickers

    This is the main function that orchestrates the extraction of all metrics
    by calling individual calculation functions for each ticker in the list.

    Args:
        tickers (List[str]): List of stock ticker symbols (e.g., ['AAPL', 'GOOGL', 'MSFT'])

    Returns:
        pd.DataFrame: DataFrame with columns:
            - 'Ticker': Stock ticker symbol (str)
            - 'Volatility (10d %)': 10-day price range percentage (float or None)
            - 'SMA 50d': 50-day simple moving average (float or None)
            - 'Momentum (10d %)': 10-day price change percentage (float or None)
            - 'Volume Ratio (10d)': Current vs 10-day average volume ratio (float or None)

        Note: None values indicate data unavailability or errors for that metric/ticker
    """
    results = []

    for ticker in tickers:
        print(f"Processing {ticker}...")

        metrics = {
            'Ticker': ticker,
            'Volatility (10d %)': calculate_volatility(ticker),
            'SMA 50d': calculate_sma_50(ticker),
            'Momentum (10d %)': calculate_momentum(ticker),
            'Volume Ratio (10d)': calculate_volume_ratio(ticker)
        }

        results.append(metrics)

    df = pd.DataFrame(results)
    return df


def metrics_to_markdown(df: pd.DataFrame) -> str:
    """
    Convert DataFrame to markdown table format

    Args:
        df (pd.DataFrame): DataFrame with metrics data (output from extract_metrics)

    Returns:
        str: Markdown-formatted table string ready for documentation/reports

    Example output:
        | Ticker   |   Volatility (10d %) |   SMA 50d |   Momentum (10d %) |   Volume Ratio (10d) |
        |:---------|---------------------:|----------:|-------------------:|---------------------:|
        | AAPL     |                 4.48 |    232.67 |               5.1  |                 0.93 |
    """
    return df.to_markdown(index=False)


def main():
    """
    Example usage
    """
    # Define list of tickers
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']

    print("Extracting metrics from Yahoo Finance...")
    print(f"Tickers: {', '.join(tickers)}\n")

    # Extract metrics
    df = extract_metrics(tickers)

    # Display as table
    print("\nResults:")
    print(df)

    # Display as markdown
    print("\n\nMarkdown format:")
    print(metrics_to_markdown(df))


if __name__ == "__main__":
    main()
