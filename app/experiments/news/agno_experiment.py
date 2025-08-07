"""
This module implements a news analysis agent using the Agno framework.
"""
# Model: openai
# https://docs.agno.com/examples/models/huggingface/ seems not working

# Tools: https://github.com/agno-agi/agno/tree/main/cookbook/tools

from datetime import datetime
import dotenv
# from agno.tools import *
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.financial_datasets import (
    FinancialDatasetsTools,
)  # FINANCIAL_DATASETS_API_KEY, https://financialdatasets.ai
# from agno.tools.newspaper import NewspaperTools # pip install newspaper3k
# from agno.tools.googlesearch import GoogleSearchTools

from app.experiments.news.custom_news_api_tool import get_top_news_headlines, search_news_everything

dotenv.load_dotenv()
today = datetime.now().strftime("%Y-%m-%d")

# main agent
agent = Agent(
    model=OpenAIChat(id="gpt-4o", temperature=0, max_tokens=4096, top_p=1),
    markdown=True,
    tools=[
        [get_top_news_headlines, search_news_everything], # own tools: API news
        ExaTools(
            start_published_date=today,
            type="keyword",
            include_domains=["cnbc.com", "reuters.com", "bloomberg.com"],
            show_results=True,
        ),
        ReasoningTools(add_instructions=True),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
    ],
    description="You are a helpful assistant that can summarize news articles and provide sentiment analysis.",
    # instructions="Use tables to display data. Don't include any other text.",
    expected_output="Use tables to display data. Don't include any other text.",
    show_tool_calls=True,
)

# ------------ Testing ------------
agent.print_response("Find the latest news about Apple.", stream=True)
