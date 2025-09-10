"""
Cross-Checker Agent - Regular class for output structure alignment
Validates news articles using StockNewsAPI, Polygon, and Alpha Vantage
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests
import os
from difflib import SequenceMatcher
from dummy_data import USE_DUMMY_DATA, get_dummy_stocknews_response, get_dummy_polygon_response, get_dummy_alphavantage_response


class CrossCheckerAgent:
    """Agent for cross-checking and validating news articles - simple class for data processing"""
    
    def __init__(self):
        self.name = "CrossCheckerAgent"
        self.description = "Validates news articles through multiple financial APIs using content similarity"
        
        self.stocknews_api_key = os.getenv("STOCKNEWS_API_KEY", "YOUR_STOCKNEWS_API_KEY")
        self.polygon_api_key = os.getenv("POLYGON_API_KEY", "YOUR_POLYGON_API_KEY") 
        self.alphavantage_api_key = os.getenv("ALPHAVANTAGE_API_KEY", "YOUR_ALPHAVANTAGE_API_KEY")
        
        self.similarity_threshold = 0.3  # Lowered threshold for demo purposes

    def fetch_stocknews_articles(self, ticker: str) -> List[Dict[str, Any]]:
        """Fetch articles from StockNewsAPI for a specific ticker"""
        
        # Use dummy data if enabled
        if USE_DUMMY_DATA:
            print(f"[DUMMY MODE] Using dummy StockNewsAPI data for {ticker}")
            return get_dummy_stocknews_response(ticker)
            
        url = "https://stocknewsapi.com/api/v1"
        
        params = {
            "tickers": ticker,
            "items": 10,
            "token": self.stocknews_api_key,
            "date": "last24hours"
        }
        
        # Real API call (commented for now)
        # response = requests.get(url, params=params)
        # return response.json().get('data', [])
        return []  # Fallback return for real API mode

    def fetch_polygon_news(self, ticker: str) -> List[Dict[str, Any]]:
        """Fetch news from Polygon API for a specific ticker"""
        
        # Use dummy data if enabled
        if USE_DUMMY_DATA:
            print(f"[DUMMY MODE] Using dummy Polygon data for {ticker}")
            return get_dummy_polygon_response(ticker)
            
        url = "https://api.polygon.io/v2/reference/news"
        
        # Past 24 hours
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            "ticker": ticker,
            "published_utc.gte": yesterday,
            "published_utc.lte": today,
            "limit": 10,
            "apikey": self.polygon_api_key
        }
        
        # Real API call (commented for now) 
        # response = requests.get(url, params=params)
        # return response.json().get('results', [])
        return []  # Fallback return for real API mode

    def fetch_alphavantage_news(self, ticker: str) -> List[Dict[str, Any]]:
        """Fetch news from Alpha Vantage API for a specific ticker"""
        
        # Use dummy data if enabled
        if USE_DUMMY_DATA:
            print(f"[DUMMY MODE] Using dummy Alpha Vantage data for {ticker}")
            return get_dummy_alphavantage_response(ticker)
            
        url = "https://www.alphavantage.co/query"
        
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "apikey": self.alphavantage_api_key,
            "limit": 10,
            "time_from": (datetime.now() - timedelta(days=1)).strftime('%Y%m%dT%H%M')
        }
        
        # Real API call (commented for now)
        # response = requests.get(url, params=params)  
        # return response.json().get('feed', [])
        return []  # Fallback return for real API mode

    def calculate_content_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two text snippets"""
        if not text1 or not text2:
            return 0.0
            
        # Simple string similarity as fallback
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        # For production, use sentence transformers:
        # embeddings = self.similarity_model.encode([text1, text2])
        # similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        # return similarity

    def cross_check_articles(self, scraper_articles: List[Dict[str, Any]], ticker: str) -> List[Dict[str, Any]]:
        """Cross-check scraper articles against multiple validation sources"""
        validation_sources = []
        
        # Fetch from all validation APIs
        stocknews_articles = self.fetch_stocknews_articles(ticker)
        polygon_articles = self.fetch_polygon_news(ticker)
        alphavantage_articles = self.fetch_alphavantage_news(ticker)
        
        validation_sources.extend([
            {'source': 'StockNewsAPI', 'articles': stocknews_articles},
            {'source': 'Polygon', 'articles': polygon_articles}, 
            {'source': 'AlphaVantage', 'articles': alphavantage_articles}
        ])
        
        validated_articles = []
        
        for scraper_article in scraper_articles:
            scraper_content = f"{scraper_article.get('title', '')} {scraper_article.get('snippet', '')}"
            
            confirmation_sources = []
            
            # Check against each validation source
            for validation_source in validation_sources:
                for validation_article in validation_source['articles']:
                    validation_content = f"{validation_article.get('title', '')} {validation_article.get('summary', validation_article.get('description', ''))}"
                    
                    similarity = self.calculate_content_similarity(scraper_content, validation_content)
                    
                    if similarity >= self.similarity_threshold:
                        confirmation_sources.append(validation_source['source'])
                        break
            
            # Keep articles confirmed by at least one validation source
            if confirmation_sources:
                scraper_article['confirmation_sources'] = list(set(confirmation_sources))
                validated_articles.append(scraper_article)
        
        return validated_articles

    def run(self, scraper_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Main execution method for the Cross-Checker Agent
        
        Args:
            scraper_results: Dictionary of ticker -> list of articles from scraper
            
        Returns:
            Dictionary of validated articles per ticker
        """
        validated_results = {}
        
        for ticker, articles in scraper_results.items():
            validated_articles = self.cross_check_articles(articles, ticker)
            validated_results[ticker] = validated_articles
            
        return validated_results