"""
Configuration file for Multi-Agent News Retrieval System
Easily toggle between dummy data mode and real API mode
"""

import os

# ==========================================
# MODE CONFIGURATION 
# ==========================================

# Set to True to use dummy data for testing, False to use real APIs
USE_DUMMY_DATA = True

# ==========================================
# API CONFIGURATION
# ==========================================

# Scraper Agent APIs
EXA_API_KEY = os.getenv("EXA_API_KEY", "YOUR_EXA_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "YOUR_SERPAPI_KEY")

# Cross-Checker Agent APIs  
STOCKNEWS_API_KEY = os.getenv("STOCKNEWS_API_KEY", "YOUR_STOCKNEWS_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "YOUR_POLYGON_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "CTMWD3HRJVT9PUON")

# Summarizer Agent (HuggingFace)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "YOUR_HUGGINGFACE_TOKEN")

# ==========================================
# PIPELINE CONFIGURATION
# ==========================================

# Content similarity threshold for cross-checking (0.0 to 1.0)
SIMILARITY_THRESHOLD = 0.3  # Lower for demo, higher (0.7+) for production

# Quality news sources filter
QUALITY_NEWS_SOURCES = [
    "ft.com",
    "theguardian.com", 
    "bloomberg.com",
    "wsj.com",
    "reuters.com"
]

# Default test tickers
DEFAULT_TEST_TICKERS = ["AAPL", "GOOGL", "TSLA", "MSFT", "NVDA"]

# Template directory
TEMPLATES_DIR = "templates"

# ==========================================
# INSTRUCTIONS
# ==========================================
"""
TO SWITCH MODES:

1. DUMMY DATA MODE (Testing):
   - Set USE_DUMMY_DATA = True
   - No API keys required
   - Uses sample data from dummy_data.py

2. REAL API MODE (Production):
   - Set USE_DUMMY_DATA = False
   - Set all API keys in environment variables:
     export EXA_API_KEY="your_exa_api_key"
     export SERPAPI_KEY="your_serpapi_key"  
     export STOCKNEWS_API_KEY="your_stocknews_key"
     export POLYGON_API_KEY="your_polygon_key"
     export ALPHAVANTAGE_API_KEY="your_alphavantage_key"
     export HUGGINGFACE_TOKEN="your_huggingface_token"
   - Uncomment API call lines in agent files
"""