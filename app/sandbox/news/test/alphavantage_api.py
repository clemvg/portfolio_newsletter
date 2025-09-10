from base_api import BaseApi
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# TODO: think if I pass one ticker or multiple in my logic for one AlphaVantageApi instance
# TODO: ticker relevance score is a good one, but source does not work (Benzinga and others) less trustable sources

class AlphaVantageApi(BaseApi):
    """
    AlphaVantage API client for fetching market news and sentiment data.

    This class provides access to AlphaVantage's NEWS_SENTIMENT API endpoint,
    which returns live and historical market news & sentiment data from premier
    news outlets covering stocks, cryptocurrencies, forex, and various topics.

    API Documentation: https://www.alphavantage.co/documentation/#news-sentiment
    """

    # AlphaVantage API specific configuration
    BASE_URL = "https://www.alphavantage.co/query"
    FUNCTION = "NEWS_SENTIMENT"  # currenty only one function
    # Supported topics see doc
    SORT_OPTION = "RELEVANCE"  # also LATEST and EARLIEST

    # limit param is ignored, set at 50
    LIMIT = 50

    # time from and to are in YYYYMMDDTHHMM format, last 24 hours
    TIME_FROM = (datetime.now() - timedelta(days=1)).strftime("%Y%m%dT%H%M")
    TIME_TO = datetime.now().strftime("%Y%m%dT%H%M")
    
    # Filtering configuration
    TICKER_SENTIMENT_THRESHOLD = 0.7  # TODO: change bcs rather low 
    TRUSTABLE_SOURCES = [
        "Reuters", "Bloomberg", "Associated Press", "Wall Street Journal",
        "Financial Times", "MarketWatch", "Yahoo Finance", "CNBC",
        "Seeking Alpha", "Benzinga" # add Benzinga sources in there to test
    ]

    def __init__(self, api_key):
        self.api_key = api_key

    def call_api(
        self,
        tickers: list[str],
        # time to and from, limit, sort, topics params are kept constant
    ):
        """
        Call the AlphaVantage NEWS_SENTIMENT API.

        The API response follows the structure outlined in the documentation:
        {
          "feed": [
            {
              "title": "Article title",
              "url": "https://...",
              "time_published": "20241201T120000",
              "authors": ["Author 1", "Author 2"],
              "summary": "Article summary...",
              "banner_image": "https://...",
              "source": "Source Name",
              "category_within_source": "Category",
              "source_domain": "domain.com",
              "overall_sentiment_score": 0.5,
              "overall_sentiment_label": "Bullish",
              "ticker_sentiment": [
                {
                  "ticker": "AAPL",
                  "relevance_score": "0.8",
                  "ticker_sentiment_score": "0.2",
                  "ticker_sentiment_label": "Somewhat-Bullish"
                }
              ]
            }
          ],
          "items": "Number of items returned",
          "sentiment_score_definition": "...",
          "relevance_score_definition": "..."
        }
        
        Interesting fields:
        - title
        - url
        - summary
        - source
        - overall_sentiment_label
        - ticker_sentiment
        """
        # Build the API request parameters
        params = {
            "function": self.FUNCTION,
            "tickers": ",".join(tickers),
            "apikey": self.api_key,
            "sort": self.SORT_OPTION,
            "time_from": self.TIME_FROM,
            "time_to": self.TIME_TO,
            "limit": self.LIMIT
        }
        
        # Make the API call
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract articles from the feed
        articles = data.get("feed", [])
        
        # Print the first 3 articles and metadata
        print(f"Total articles retrieved: {data.get('items', 0)}")
        print(f"Sentiment score definition: {data.get('sentiment_score_definition', 'N/A')}")
        print(f"Relevance score definition: {data.get('relevance_score_definition', 'N/A')}")
        print("\nFirst 3 articles:")
        
        for i, article in enumerate(articles[:3]):
            print(f"\nArticle {i+1}:")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  URL: {article.get('url', 'N/A')}")
            print(f"  Summary: {article.get('summary', 'N/A')}")
            print(f"  Source: {article.get('source', 'N/A')}")
            print(f"  Overall Sentiment: {article.get('overall_sentiment_label', 'N/A')}")
            print(f"  Ticker Sentiment: {article.get('ticker_sentiment', 'N/A')}")
        
        # Return the list of articles
        return articles

    def filter_articles(self, search_ticker: list[str], articles: list[dict]):
        """
        Filter articles based on source trustworthiness and ticker sentiment score.
        
        Filtering criteria:
        - Source: Only articles from trustable news sources
        - Ticker sentiment: Only articles with ticker sentiment score above threshold
        
        Args:
            articles (list): List of articles to filter
            
        Returns:
            list: Filtered list of articles in the same format
        """
        if not articles:
            print("No articles to filter.")
            return []
        
        original_count = len(articles)
        filtered_articles = []
        
        for article in articles:
            # 1) Check if source is trustable
            source = article.get('source', '')
            if source not in self.TRUSTABLE_SOURCES: # could also check URL
                continue
            
            # 2) Check if ticker sentiment is relevant
            ticker_sentiment = article.get('ticker_sentiment') # error raising if not present
            for ticker_data in ticker_sentiment:
                ticker = ticker_data.get('ticker')
                ticker_score = float(ticker_data.get('relevance_score', 0)) # not ticker_sentiment_score
                if ticker and abs(ticker_score) >= self.TICKER_SENTIMENT_THRESHOLD and ticker == search_ticker:
                    filtered_articles.append(article) 
                    break
        
        filtered_count = len(filtered_articles)
        print(f"Articles filtered: {original_count - filtered_count} removed, {filtered_count} remaining")
        
        return filtered_articles


if __name__ == "__main__":
    # Test the AlphaVantage API with AAPL ticker
    api_key = os.getenv("ALPHAVANTAGE_API_KEY") 
    if not api_key:
        raise ValueError("API key not found. Please set ALPHAVANTAGE_API_KEY in your .env file.")
    
    # Create API instance
    alpha_api = AlphaVantageApi(api_key)
    
    # Test with AAPL ticker
    tickers = ["AAPL"]
    
    try:
        print(f"Fetching articles for tickers: {tickers}")
        print("-" * 50)
        
        articles = alpha_api.call_api(tickers) # prints are inside call_api
        filtered_articles = alpha_api.filter_articles(tickers[0], articles)
        print(f"Filtered articles: {filtered_articles}")
        
    except Exception as e:
        print(f"Error occurred: {e}")