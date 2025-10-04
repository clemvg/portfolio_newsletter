#!/usr/bin/env python3
"""
LLM-based News Summarizer

This module uses HuggingFace LLMs with structured output to summarize
raw news data into bullet points for the portfolio newsletter.

Author: Clément Van Goethem
Date: 2025-10-04
"""
import os
import json
from typing import Dict, List
from pathlib import Path
from jinja2 import Template
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class NewsSummarizer:
    """Summarizes raw news data using HuggingFace LLMs with structured output."""

    def __init__(self, model: str = "meta-llama/Llama-3.2-3B-Instruct"):
        """
        Initialize the news summarizer.

        Args:
            model (str): HuggingFace model to use for summarization
        """
        self.client = InferenceClient(
            model=model,
            token=os.environ.get("HUGGINGFACE_TOKEN"),
        )

        # Load Jinja2 template
        template_path = Path(__file__).parent / "summarisation_prompt.jinja2"
        with open(template_path, "r") as f:
            self.template = Template(f.read())

    def summarize_batch(self, news_data: Dict[str, Dict[str, str]]) -> Dict[str, List[str]]:
        """
        Summarize news for multiple tickers.

        Args:
            news_data: Dictionary mapping ticker to dict with keys:
                - company_name: Full company name
                - raw_info: Raw news text to summarize

        Returns:
            Dict[str, List[str]]: Dictionary mapping ticker to list of bullet points
        """
        results = {}

        for ticker, data in news_data.items():
            company_name = data.get("company_name", ticker)
            raw_info = data.get("raw_info", "")

            if not raw_info:
                results[ticker] = []
                continue

            # Generate prompt from template
            prompt = self.template.render(company_name=company_name, raw_info=raw_info)

            try:
                # Call LLM
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.3,
                )

                # Parse JSON response
                summary_text = response.choices[0].message.content.strip()
                summary_json = json.loads(summary_text)

                # Handle both dict and list responses
                if isinstance(summary_json, dict):
                    results[ticker] = summary_json.get("bullets", [])
                elif isinstance(summary_json, list):
                    results[ticker] = summary_json
                else:
                    results[ticker] = []

            except Exception as e:
                print(f"Error summarizing {ticker}: {e}")
                results[ticker] = []

        return results


# Example usage
if __name__ == "__main__":
    # Load sample_data from input_news_summary.json
    input_file = Path(__file__).parent / "input_news_summary.json"
    with open(input_file, "r") as f:
        sample_data = json.load(f)

    # Run summarization
    summarizer = NewsSummarizer()
    results = summarizer.summarize_batch(sample_data)

    print("=== Summarized News ===")
    for ticker, bullets in results.items():
        print(f"\n{ticker}:")
        for bullet in bullets:
            print(f"  - {bullet}")

    # Save as JSON
    output_file = "src/data/news/output_news_summary.json" # run from root app folder
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n=== Saved to {output_file} ===")
