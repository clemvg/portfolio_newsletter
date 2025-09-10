"""
Summarizer Agent using Agno framework
Summarizes validated news articles and performs sentiment analysis using HuggingFace models
"""

from typing import List, Dict, Any
from base_agent import Agent
import os
import sys
from jinja2 import Environment, FileSystemLoader

# Add the parent directory to sys.path to import from hf_llm
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from sandbox.hf_llm.summarization import get_bart_summary
from sandbox.hf_llm.sentiment_analysis import get_financial_sentiment


class SummarizerAgent(Agent):
    """Agent for summarizing news articles and performing sentiment analysis"""
    
    def __init__(self, templates_path: str = None):
        super().__init__(
            name="SummarizerAgent",
            description="Summarizes validated news articles and performs sentiment analysis"
        )
        
        # Set up Jinja2 template environment - templates now in news/templates
        templates_dir = templates_path or os.path.join(
            os.path.dirname(__file__), 'templates'
        )
        self.jinja_env = Environment(loader=FileSystemLoader(templates_dir))

    def load_summarizer_template(self) -> str:
        """Load the summarization prompt template"""
        try:
            template = self.jinja_env.get_template('summarizer_prompt.j2')
            return template
        except Exception as e:
            print(f"Error loading template: {e}")
            # Fallback template
            return """
            Please provide a concise summary of the following news articles about {{ ticker }}:
            
            {% for article in articles %}
            Title: {{ article.title }}
            Source: {{ article.source }}
            Content: {{ article.snippet }}
            ---
            {% endfor %}
            
            Summary should be 1-2 sentences focusing on the key developments and their potential impact.
            """

    def summarize_ticker_news(self, ticker: str, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize all news articles for a specific ticker"""
        if not articles:
            return {
                "ticker": ticker,
                "summary": "No validated news found for this ticker.",
                "sources": [],
                "sentiment": "neutral"
            }
        
        # Load and render template
        template = self.load_summarizer_template()
        if isinstance(template, str):
            # Fallback string template
            prompt = template.replace("{{ ticker }}", ticker)
            articles_text = "\n".join([
                f"Title: {article['title']}\nSource: {article['source']}\nContent: {article['snippet']}"
                for article in articles
            ])
            prompt = prompt.replace("{% for article in articles %}...{% endfor %}", articles_text)
        else:
            # Jinja2 template
            prompt = template.render(ticker=ticker, articles=articles)
        
        # Combine all article content for summarization
        combined_content = f"News about {ticker}:\n"
        for article in articles:
            combined_content += f"{article['title']} - {article['snippet']}\n"
        
        # Generate summary using BART
        summary_result = get_bart_summary(combined_content)
        
        if summary_result and hasattr(summary_result, 'summary_text'):
            summary = summary_result.summary_text
        elif isinstance(summary_result, dict) and 'summary_text' in summary_result:
            summary = summary_result['summary_text']
        else:
            # Fallback summary
            summary = f"Multiple news sources report developments regarding {ticker}."
        
        # Perform sentiment analysis
        sentiment_result = get_financial_sentiment(summary)
        sentiment = "neutral"
        
        if sentiment_result and len(sentiment_result) > 0:
            top_sentiment = sentiment_result[0]
            if hasattr(top_sentiment, 'label'):
                sentiment_label = top_sentiment.label.lower()
                # Map financial sentiment labels to standard format
                if 'positive' in sentiment_label or 'bullish' in sentiment_label:
                    sentiment = "positive"
                elif 'negative' in sentiment_label or 'bearish' in sentiment_label:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
        
        # Extract unique sources
        sources = list(set([article['source'] for article in articles if article.get('source')]))
        
        return {
            "ticker": ticker,
            "summary": summary,
            "sources": sources,
            "sentiment": sentiment
        }

    def run(self, validated_results: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Main execution method for the Summarizer Agent
        
        Args:
            validated_results: Dictionary of ticker -> list of validated articles
            
        Returns:
            List of ticker summaries with sentiment analysis
        """
        summaries = []
        
        for ticker, articles in validated_results.items():
            ticker_summary = self.summarize_ticker_news(ticker, articles)
            summaries.append(ticker_summary)
        
        return summaries