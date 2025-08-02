"""
Price change detection module for experimentation. Test with test_price_detection.py
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(ticker: str, days: int) -> pd.DataFrame:
    """Get stock data from Yahoo Finance"""
    try:
        end_date = datetime.now()
        # Add extra days to account for weekends and holidays
        # For every 5 business days, we need about 7 calendar days
        extra_days = max(5, int(days * 1.4))  # Add 40% more days to ensure we get enough data
        start_date = end_date - timedelta(days=days + extra_days)
        
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
            
        return data
    except Exception as e:
        raise Exception(f"Error fetching data for {ticker}: {str(e)}")


def collect_data_over_n_days(tickers: List[str], days: int) -> Dict[str, pd.DataFrame]:
    """Collect stock data over N days for multiple tickers"""
    data = {}
    for ticker in tickers:
        try:
            ticker_data = get_stock_data(ticker, days)
            data[ticker] = ticker_data
        except Exception as e:
            print(f"Warning: Could not fetch data for {ticker}: {e}")
            continue
    return data


def calculate_percentage_change_over_n_days(data: pd.DataFrame, days: int) -> float:
    """Calculate the percentage change over N days"""
    if len(data) < days:
        raise ValueError(f"Not enough data points. Need at least {days} days, got {len(data)}")
    
    # Get the first and last available prices
    first_price = data['Close'].iloc[0] # FIXED TO YFINANCE API 
    last_price = data['Close'].iloc[-1]
    
    percentage_change = ((last_price - first_price) / first_price) * 100
    return percentage_change


def calculate_volatility_over_n_days(data: pd.DataFrame, days: int) -> float:
    """Calculate the volatility (standard deviation of returns) over N days"""
    if len(data) < 2:
        raise ValueError("Need at least 2 data points to calculate volatility")
    
    # Calculate daily returns
    returns = data['Close'].pct_change().dropna()
    
    # Calculate volatility (standard deviation of returns)
    volatility = returns.std() * np.sqrt(252)  # Annualized volatility
    return volatility


def detect_stock_price_changes(tickers: List[str], days: int = 10) -> Dict[str, Dict]:
    """Main function to detect stock price changes and volatility"""
    results = {}
    
    # Collect data for all tickers
    print(f"Collecting data for {len(tickers)} tickers over {days} days...")
    data = collect_data_over_n_days(tickers, days)
    
    for ticker, ticker_data in data.items():
        try:
            # Calculate percentage change
            percentage_change = calculate_percentage_change_over_n_days(ticker_data, days)
            
            # Calculate volatility
            volatility = calculate_volatility_over_n_days(ticker_data, days)
            
            # Get current price
            current_price = ticker_data['Close'].iloc[-1]
            
            results[ticker] = {
                'current_price': current_price,
                'percentage_change': percentage_change,
                'volatility': volatility,
                'days_analyzed': len(ticker_data), # not very informative 
                'data_points': len(ticker_data)
            }
            
            print(f"{ticker}: {percentage_change:.2f}% change, {volatility:.2f} volatility")
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            results[ticker] = {
                'error': str(e)
            }
    
    return results


def analyze_stock_prices(tickers: str, days: int = 10) -> Dict[str, Dict]:
    """
    Main convenience function to detect stock price changes
    
    Args:
        tickers: Comma-separated string of ticker symbols
        days: Number of days to analyze (default: 10)
    
    Returns:
        Dictionary with analysis results for each ticker
    """
    if not tickers:
        print("No tickers provided")
        return {}
    
    # Parse tickers string into list
    ticker_list = [ticker.strip().upper() for ticker in tickers.split(',') if ticker.strip()]
    
    if not ticker_list:
        print("No valid tickers found")
        return {}
    
    # Run the analysis
    results = detect_stock_price_changes(ticker_list, days)
    
    return results
