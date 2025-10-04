#!/usr/bin/env python3
"""
News Data Module

This module provides news data for tickers using LLM summarization.
Returns structured JSON format for dynamic newsletter generation.

Author: Clément Van Goethem
Date: 2025-10-04
"""
import json
from typing import List, Dict
from pathlib import Path

# TODO: remove dummy data below
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


def load_input_news_data() -> Dict[str, Dict[str, str]]:
    """
    Load news data from input_news_summary.json.

    Returns:
        Dict[str, Dict[str, str]]: Dictionary mapping ticker to news data
    """
    input_file = Path(__file__).parent / "news" / "input_news_summary.json"
    try:
        with open(input_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading input news data: {e}")
        return {}


def get_all_news(tickers: List[str], use_llm: bool = True) -> Dict[str, List[str]]:
    """
    Get news for multiple tickers.

    When use_llm=True, uses LLM summarization with real news data from input_news_summary.json.
    When use_llm=False, returns placeholder data.

    Args:
        tickers (List[str]): List of stock ticker symbols
        use_llm (bool): Whether to use LLM summarization (default: False)

    Returns:
        Dict[str, List[str]]: Dictionary mapping ticker to list of news bullet points
    """
    if not use_llm:
        # Return placeholder data
        return {ticker: get_news_placeholder(ticker) for ticker in tickers}

    # Use LLM summarization with input data
    try:
        from src.data.news.llm_summariser import NewsSummarizer

        # Load news data from input JSON
        all_news_data = load_input_news_data()

        # Filter to requested tickers
        news_data = {
            ticker: all_news_data[ticker]
            for ticker in tickers
            if ticker in all_news_data
        }

        if not news_data:
            print(f"No news data found for tickers: {tickers}")
            print("Falling back to placeholder data")
            return {ticker: get_news_placeholder(ticker) for ticker in tickers}

        summarizer = NewsSummarizer()
        return summarizer.summarize_batch(news_data)

    except Exception as e:
        print(f"Error using LLM summarization: {e}")
        print("Falling back to placeholder data")
        return {ticker: get_news_placeholder(ticker) for ticker in tickers}
