#!/usr/bin/env python3
"""
Test script for the Multi-Agent News Retrieval System with dummy data
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper_agent import ScraperAgent
from crosschecker_agent import CrossCheckerAgent
from summarizer_agent import SummarizerAgent


def test_pipeline():
    """Test the complete pipeline with dummy data"""
    print("="*60)
    print("TESTING MULTI-AGENT NEWS RETRIEVAL SYSTEM")
    print("="*60)
    
    # Test tickers
    test_tickers = ["AAPL", "GOOGL", "TSLA"]
    
    # Initialize agents
    print("\n1. Initializing agents...")
    try:
        scraper = ScraperAgent()
        crosschecker = CrossCheckerAgent()
        summarizer = SummarizerAgent()
        print("✅ All agents initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing agents: {e}")
        return
    
    # Step 1: Scraper Agent
    print(f"\n2. Running Scraper Agent for tickers: {test_tickers}")
    try:
        scraper_results = scraper.run(test_tickers)
        print(f"✅ Scraper found articles for {len(scraper_results)} tickers")
        for ticker, articles in scraper_results.items():
            print(f"   - {ticker}: {len(articles)} articles")
    except Exception as e:
        print(f"❌ Error in Scraper Agent: {e}")
        return
    
    # Step 2: Cross-Checker Agent
    print(f"\n3. Running Cross-Checker Agent...")
    try:
        validated_results = crosschecker.run(scraper_results)
        validated_count = sum(len(articles) for articles in validated_results.values())
        print(f"✅ Cross-checker validated {validated_count} articles")
        for ticker, articles in validated_results.items():
            if articles:
                print(f"   - {ticker}: {len(articles)} validated articles")
                for article in articles:
                    if article.get('confirmation_sources'):
                        print(f"     • {article['title'][:50]}... (confirmed by: {', '.join(article['confirmation_sources'])})")
    except Exception as e:
        print(f"❌ Error in Cross-Checker Agent: {e}")
        return
    
    # Step 3: Summarizer Agent
    print(f"\n4. Running Summarizer Agent...")
    try:
        final_summaries = summarizer.run(validated_results)
        print(f"✅ Generated {len(final_summaries)} ticker summaries")
        
        print("\n" + "="*60)
        print("FINAL RESULTS")
        print("="*60)
        
        for summary in final_summaries:
            print(f"\n📈 Ticker: {summary['ticker']}")
            print(f"📰 Summary: {summary['summary']}")
            print(f"🔍 Sources: {', '.join(summary['sources']) if summary['sources'] else 'None'}")
            print(f"💭 Sentiment: {summary['sentiment']}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error in Summarizer Agent: {e}")
        return
    
    print(f"\n✅ Pipeline completed successfully!")
    print("="*60)


if __name__ == "__main__":
    test_pipeline()