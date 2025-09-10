"""
Dummy data for testing the news retrieval pipeline
Contains sample responses from all APIs to test the complete workflow
"""

from datetime import datetime
from typing import Dict, List, Any

# Import configuration
from config import USE_DUMMY_DATA

# Sample Exa API responses
EXA_DUMMY_RESPONSES = {
    "AAPL": [
        {
            "title": "Apple Reports Strong Q4 Earnings Beat Expectations",
            "url": "https://www.ft.com/content/apple-earnings-q4-2024",
            "text": "Apple Inc. reported fourth-quarter earnings that exceeded Wall Street expectations, driven by strong iPhone sales and services revenue growth.",
            "published_date": "2024-11-01T10:30:00Z"
        },
        {
            "title": "Apple Announces New AI Integration Plans",
            "url": "https://www.reuters.com/technology/apple-ai-integration-2024",
            "text": "Apple unveiled comprehensive AI integration plans across its ecosystem, including enhanced Siri capabilities and machine learning features.",
            "published_date": "2024-11-01T14:15:00Z"
        }
    ],
    "GOOGL": [
        {
            "title": "Alphabet Sees Cloud Revenue Surge in Latest Quarter",
            "url": "https://www.bloomberg.com/news/alphabet-cloud-growth",
            "text": "Alphabet's Google Cloud division posted significant revenue growth, competing strongly with AWS and Microsoft Azure.",
            "published_date": "2024-11-01T09:45:00Z"
        }
    ],
    "TSLA": [
        {
            "title": "Tesla Delivers Record Vehicle Numbers Despite Market Challenges",
            "url": "https://www.wsj.com/articles/tesla-delivery-record-2024",
            "text": "Tesla achieved record quarterly vehicle deliveries, surpassing analyst expectations despite ongoing supply chain challenges.",
            "published_date": "2024-11-01T16:20:00Z"
        }
    ]
}

# Sample Google News API responses
GOOGLE_NEWS_DUMMY_RESPONSES = {
    "AAPL": [
        {
            "title": "Apple Stock Rises on Earnings Beat",
            "link": "https://www.theguardian.com/technology/apple-stock-earnings",
            "snippet": "Apple shares climbed in after-hours trading following better-than-expected quarterly results and optimistic guidance.",
            "date": "2024-11-01"
        }
    ],
    "GOOGL": [
        {
            "title": "Google Parent Alphabet Beats Revenue Estimates",
            "link": "https://www.reuters.com/business/alphabet-earnings-beat",
            "snippet": "Alphabet Inc reported quarterly revenue that beat Wall Street estimates, powered by robust advertising and cloud growth.",
            "date": "2024-11-01"
        }
    ],
    "TSLA": [
        {
            "title": "Tesla Production Ramp Continues",
            "link": "https://www.bloomberg.com/news/tesla-production-ramp",
            "snippet": "Tesla continues to ramp production across its global facilities, with new manufacturing milestones achieved.",
            "date": "2024-11-01"
        }
    ]
}

# Sample StockNewsAPI responses
STOCKNEWS_DUMMY_RESPONSES = {
    "AAPL": [
        {
            "title": "Apple Earnings Exceed Expectations",
            "summary": "Apple delivered strong quarterly earnings with revenue growth across all product categories.",
            "url": "https://stocknews.com/apple-earnings-beat",
            "date": "2024-11-01T10:00:00Z"
        }
    ],
    "GOOGL": [
        {
            "title": "Alphabet Reports Cloud Revenue Growth",
            "summary": "Google's parent company showed impressive cloud division performance in latest financial results.",
            "url": "https://stocknews.com/alphabet-cloud-revenue",
            "date": "2024-11-01T11:30:00Z"
        }
    ],
    "TSLA": [
        {
            "title": "Tesla Achieves Delivery Milestone",
            "summary": "Electric vehicle manufacturer Tesla reached new quarterly delivery records despite market headwinds.",
            "url": "https://stocknews.com/tesla-delivery-milestone",
            "date": "2024-11-01T15:45:00Z"
        }
    ]
}

# Sample Polygon API responses
POLYGON_DUMMY_RESPONSES = {
    "AAPL": [
        {
            "title": "Apple Inc. Q4 Financial Results Announced",
            "description": "Apple reported quarterly earnings with strong performance in iPhone and services segments.",
            "published_utc": "2024-11-01T10:30:00Z",
            "article_url": "https://polygon.io/news/apple-q4-results"
        }
    ],
    "GOOGL": [
        {
            "title": "Google Cloud Drives Alphabet Revenue Growth",
            "description": "Alphabet's cloud computing division showed significant revenue increases in the latest quarter.",
            "published_utc": "2024-11-01T09:15:00Z",
            "article_url": "https://polygon.io/news/alphabet-cloud-growth"
        }
    ],
    "TSLA": [
        {
            "title": "Tesla Sets New Quarterly Delivery Record",
            "description": "Tesla delivered a record number of vehicles in Q4, exceeding Wall Street projections.",
            "published_utc": "2024-11-01T16:00:00Z",
            "article_url": "https://polygon.io/news/tesla-delivery-record"
        }
    ]
}

# Sample Alpha Vantage API responses
ALPHAVANTAGE_DUMMY_RESPONSES = {
    "AAPL": [
        {
            "title": "Apple Earnings Beat Drives Stock Higher",
            "summary": "Strong iPhone sales and services growth contributed to Apple's earnings beat.",
            "url": "https://alphavantage.co/news/apple-earnings-beat",
            "time_published": "20241101T103000",
            "overall_sentiment_score": 0.3,
            "overall_sentiment_label": "Somewhat-Bullish"
        }
    ],
    "GOOGL": [
        {
            "title": "Alphabet Cloud Business Shows Strong Performance",
            "summary": "Google's cloud division revenue growth exceeded analyst expectations in latest quarter.",
            "url": "https://alphavantage.co/news/alphabet-cloud-performance",
            "time_published": "20241101T094500",
            "overall_sentiment_score": 0.2,
            "overall_sentiment_label": "Somewhat-Bullish"
        }
    ],
    "TSLA": [
        {
            "title": "Tesla Delivery Numbers Impress Markets",
            "summary": "Tesla's record quarterly deliveries demonstrate strong demand for electric vehicles.",
            "url": "https://alphavantage.co/news/tesla-delivery-numbers",
            "time_published": "20241101T162000",
            "overall_sentiment_score": 0.4,
            "overall_sentiment_label": "Bullish"
        }
    ]
}


def get_dummy_exa_response(ticker: str) -> List[Dict[str, Any]]:
    """Get dummy Exa API response for a ticker"""
    return EXA_DUMMY_RESPONSES.get(ticker, [])


def get_dummy_google_news_response(ticker: str) -> List[Dict[str, Any]]:
    """Get dummy Google News API response for a ticker"""
    return GOOGLE_NEWS_DUMMY_RESPONSES.get(ticker, [])


def get_dummy_stocknews_response(ticker: str) -> List[Dict[str, Any]]:
    """Get dummy StockNewsAPI response for a ticker"""
    return STOCKNEWS_DUMMY_RESPONSES.get(ticker, [])


def get_dummy_polygon_response(ticker: str) -> List[Dict[str, Any]]:
    """Get dummy Polygon API response for a ticker"""
    return POLYGON_DUMMY_RESPONSES.get(ticker, [])


def get_dummy_alphavantage_response(ticker: str) -> List[Dict[str, Any]]:
    """Get dummy Alpha Vantage API response for a ticker"""
    return ALPHAVANTAGE_DUMMY_RESPONSES.get(ticker, [])