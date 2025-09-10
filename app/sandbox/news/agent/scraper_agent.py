"""
Scraper Agent using Agno framework
Retrieves news from Exa API and Google News API for given tickers
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from base_agent import Agent
import requests
import os
from jinja2 import Environment, FileSystemLoader
from dummy_data import USE_DUMMY_DATA, get_dummy_exa_response, get_dummy_google_news_response


class ScraperAgent(Agent):
    """Agent for scraping news from multiple sources with natural language processing"""
    
    def __init__(self):
        super().__init__(
            name="ScraperAgent",
            description="Retrieves news articles from Exa API and Google News API with intelligent query generation"
        )
        self.exa_api_key = os.getenv("EXA_API_KEY", "YOUR_EXA_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_KEY", "YOUR_SERPAPI_KEY")
        
        # Quality news sources filter
        self.quality_sources = [
            "ft.com",
            "theguardian.com", 
            "bloomberg.com",
            "wsj.com",
            "reuters.com"
        ]
        
        # Set up Jinja2 template environment
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(templates_dir))

    def load_scraper_template(self) -> str:
        """Load the scraper prompt template for query optimization"""
        try:
            template = self.jinja_env.get_template('scraper_prompt.j2')
            return template
        except Exception as e:
            print(f"Error loading scraper template: {e}")
            return None

    def generate_optimized_query(self, ticker: str) -> str:
        """Generate optimized search query using Agno natural language processing"""
        template = self.load_scraper_template()
        if template:
            # Use template to guide search strategy
            search_context = template.render(ticker=ticker)
            # For actual implementation, this would use Agno's NLP capabilities
            # to generate the most effective search query based on the template
            optimized_query = f"{ticker} stock earnings financial news"
        else:
            # Fallback query
            optimized_query = f"{ticker} stock news"
        
        return optimized_query

    def search_exa_news(self, ticker: str) -> List[Dict[str, Any]]:
        """Search news using Exa API for a specific ticker with optimized queries"""
        
        # Use dummy data if enabled
        if USE_DUMMY_DATA:
            print(f"[DUMMY MODE] Using dummy Exa data for {ticker}")
            return get_dummy_exa_response(ticker)
        
        url = "https://api.exa.ai/search"
        
        # Generate optimized query using template
        optimized_query = self.generate_optimized_query(ticker)
        
        # Filter for past 24 hours
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        
        headers = {
            "x-api-key": self.exa_api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": optimized_query,
            "num_results": 10,
            "start_published_date": yesterday,
            "include_domains": self.quality_sources,
            "contents": {
                "text": True
            }
        }
        
        # Real API call (commented for now)
        # response = requests.post(url, json=payload, headers=headers)
        # return response.json().get('results', [])
        return []  # Fallback return for real API mode

    def search_google_news(self, ticker: str) -> List[Dict[str, Any]]:
        """Search news using Google News API via SerpApi for a specific ticker with optimized queries"""
        
        # Use dummy data if enabled
        if USE_DUMMY_DATA:
            print(f"[DUMMY MODE] Using dummy Google News data for {ticker}")
            return get_dummy_google_news_response(ticker)
        
        url = "https://serpapi.com/search.json"
        
        # Use optimized query generation
        optimized_query = self.generate_optimized_query(ticker)
        
        params = {
            "engine": "google_news",
            "q": optimized_query,
            "api_key": self.serpapi_key,
            "tbm": "nws",
            "tbs": "qdr:d"  # Past 24 hours
        }
        
        # Real API call (commented for now)
        # response = requests.get(url, params=params)
        # results = response.json().get('news_results', [])
        
        # Filter for quality sources
        # filtered_results = [
        #     article for article in results
        #     if any(source in article.get('link', '') for source in self.quality_sources)
        # ]
        
        return []  # Fallback return for real API mode

    def run(self, tickers: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Main execution method for the Scraper Agent
        
        Args:
            tickers: List of stock ticker symbols
            
        Returns:
            Dictionary mapping tickers to list of news articles
        """
        results = {}
        
        for ticker in tickers:
            ticker_news = []
            
            # Search Exa API
            exa_results = self.search_exa_news(ticker)
            ticker_news.extend(exa_results)
            
            # Search Google News API
            google_results = self.search_google_news(ticker)
            ticker_news.extend(google_results)
            
            # Standardize output format
            standardized_news = []
            for article in ticker_news:
                standardized_article = {
                    'title': article.get('title', ''),
                    'snippet': article.get('snippet', article.get('text', '')),
                    'url': article.get('url', article.get('link', '')),
                    'source': self._extract_source(article.get('url', article.get('link', ''))),
                    'published_date': article.get('published_date', article.get('date', '')),
                    'ticker': ticker
                }
                standardized_news.append(standardized_article)
            
            results[ticker] = standardized_news
            
        return results
    
    def _extract_source(self, url: str) -> str:
        """Extract source name from URL"""
        if not url:
            return "Unknown"
            
        for source_domain in self.quality_sources:
            if source_domain in url:
                return source_domain.split('.')[0].title()
        
        return "Unknown"