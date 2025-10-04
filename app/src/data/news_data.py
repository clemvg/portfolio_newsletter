#!/usr/bin/env python3
"""
News Placeholder Module

This module provides placeholder news data for tickers.
This will be replaced with actual news extraction in the future.

Author: Clément Van Goethem
Date: 2025-10-04
"""
from typing import List, Dict


def get_news_placeholder(ticker: str) -> List[str]:
    """
    Get placeholder news bullets for a ticker.

    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

    Returns:
        List[str]: List of placeholder news items (3-4 bullets)
    """
    news_items = [
        "shows strong market performance in recent trading sessions",
        "Analysts maintain positive outlook on fundamentals",
        "remains active in key strategic initiatives"
    ]
    return news_items


def get_all_news(tickers: List[str]) -> Dict[str, List[str]]:
    """
    Get placeholder news for multiple tickers.

    Args:
        tickers (List[str]): List of stock ticker symbols

    Returns:
        Dict[str, List[str]]: Dictionary mapping ticker to list of news items
    """
    return {ticker: get_news_placeholder(ticker) for ticker in tickers}
