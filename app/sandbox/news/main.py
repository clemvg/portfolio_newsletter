"""
Main orchestration pipeline for Multi-Agent News Retrieval System
Coordinates Scraper (Agno), Cross-Checker (regular class), and Summarizer (Agno) agents
"""

from typing import List, Dict, Any
from agno import Pipeline

# Import the agents
from .scraper_agent import ScraperAgent
from .crosschecker_agent import CrossCheckerAgent
from .summarizer_agent import SummarizerAgent


class NewsRetrievalPipeline:
    """Main pipeline orchestrating the multi-agent news retrieval system"""
    
    def __init__(self):
        """Initialize the pipeline with all agents"""
        self.scraper_agent = ScraperAgent()  # Agno Agent for NLP
        self.crosschecker_agent = CrossCheckerAgent()  # Regular class for data processing
        self.summarizer_agent = SummarizerAgent()  # Agno Agent for NLP
        
        # Create Agno pipeline with only Agno agents
        self.agno_pipeline = Pipeline(
            name="NewsRetrievalPipeline",
            description="Multi-agent system for retrieving, validating, and summarizing financial news",
            agents=[
                self.scraper_agent,
                self.summarizer_agent  # Only include Agno agents in pipeline
            ]
        )

    def execute(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """
        Execute the complete news retrieval pipeline
        
        Args:
            tickers: List of stock ticker symbols to analyze
            
        Returns:
            List of dictionaries with ticker summaries, sources, and sentiment
        """
        print(f"Starting news retrieval pipeline for tickers: {tickers}")
        
        # Step 1: Scrape news articles
        print("Step 1: Scraping news from multiple sources...")
        scraper_results = self.scraper_agent.run(tickers)
        print(f"Scraper found articles for {len(scraper_results)} tickers")
        
        # Step 2: Cross-check and validate articles
        print("Step 2: Cross-checking articles with validation sources...")
        validated_results = self.crosschecker_agent.run(scraper_results)
        validated_count = sum(len(articles) for articles in validated_results.values())
        print(f"Cross-checker validated {validated_count} articles")
        
        # Step 3: Summarize and analyze sentiment
        print("Step 3: Generating summaries and sentiment analysis...")
        final_summaries = self.summarizer_agent.run(validated_results)
        print(f"Generated {len(final_summaries)} ticker summaries")
        
        return final_summaries

    def run_single_ticker(self, ticker: str) -> Dict[str, Any]:
        """
        Run the pipeline for a single ticker
        
        Args:
            ticker: Single stock ticker symbol
            
        Returns:
            Dictionary with ticker summary, sources, and sentiment
        """
        results = self.execute([ticker])
        return results[0] if results else {
            "ticker": ticker,
            "summary": "No news found or validation failed",
            "sources": [],
            "sentiment": "neutral"
        }

    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get status information about the pipeline and its agents"""
        return {
            "pipeline_name": self.agno_pipeline.name,
            "agno_agents": [
                {
                    "name": agent.name,
                    "description": agent.description,
                    "status": "ready",
                    "type": "Agno Agent"
                }
                for agent in self.agno_pipeline.agents
            ],
            "utility_agents": [
                {
                    "name": self.crosschecker_agent.name,
                    "description": self.crosschecker_agent.description,
                    "status": "ready",
                    "type": "Utility Class"
                }
            ],
            "status": "ready"
        }


def main():
    """Example usage of the news retrieval pipeline"""
    # Example tickers
    example_tickers = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    
    # Initialize pipeline
    pipeline = NewsRetrievalPipeline()
    
    # Show pipeline status
    status = pipeline.get_pipeline_status()
    print(f"Pipeline Status: {status}")
    
    # Execute pipeline
    results = pipeline.execute(example_tickers)
    
    # Print results
    print("\n" + "="*50)
    print("NEWS RETRIEVAL RESULTS")
    print("="*50)
    
    for result in results:
        print(f"\nTicker: {result['ticker']}")
        print(f"Summary: {result['summary']}")
        print(f"Sources: {', '.join(result['sources'])}")
        print(f"Sentiment: {result['sentiment']}")
        print("-" * 30)


if __name__ == "__main__":
    main()