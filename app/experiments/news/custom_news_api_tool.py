"""
This module implements custom tools for news analysis using the Agno framework.
news api: https://newsapi.org/
"""
import json
import os
from datetime import date, datetime
import httpx
import dotenv

from agno.agent import Agent

dotenv.load_dotenv()

# hacker-news example in doc
def get_top_news_headlines(
    q: str | None = None,
    sources: str | None = None,
    category: str | None = None,
    language: str = "en",
    country: str | None = None,
    page_size: int = 10,
    page: int = 1,
) -> str:
    """Use this function to get top headlines from NewsAPI.

    Args:
        q: Keywords or phrase to search for
        sources: Comma-separated list of source identifiers
        category: Category of headlines (business, entertainment, general, health, science, sports, technology)
        language: Language of articles (default: 'en')
        country: 2-letter ISO 3166-1 country code (e.g., 'us')
        page_size: Number of results per page (max 100)
        page: Page number for pagination

    Returns:
        str: JSON string with NewsAPI response (status, totalResults, articles)
    """
    api_key = os.getenv("API_NEWS_KEY")
    if not api_key:
        raise ValueError("API_NEWS_KEY not set in environment")

    # Note: NewsAPI does not allow mixing `sources` with `country` or `category`.
    if sources and (country or category):
        raise ValueError(
            "Cannot combine 'sources' with 'country' or 'category'"
        )

    params: dict[str, object] = {
        "q": q,
        "sources": sources,
        "category": category,
        "language": language,
        "country": country,
        "pageSize": page_size,
        "page": page,
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    headers = {"X-Api-Key": api_key}
    resp = httpx.get(
        "https://newsapi.org/v2/top-headlines",
        params=params,
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    # Trim noisy fields to keep tool output concise
    for art in data.get("articles", []) or []:
        art.pop("content", None)
    return json.dumps(data)


def search_news_everything(
    q: str | None = None,
    sources: str | None = None,
    domains: str | None = None,
    from_param: str | date | datetime | None = None,
    to: str | date | datetime | None = None,
    language: str = "en",
    sort_by: str = "publishedAt",
    page_size: int = 10,
    page: int = 1,
) -> str:
    """Use this function to search articles using the NewsAPI 'everything' endpoint.

    Args mirror NewsAPI 'everything' parameters. Dates can be YYYY-MM-DD, date, or datetime.
    Returns a JSON string.
    """
    api_key = os.getenv("API_NEWS_KEY")
    if not api_key:
        raise ValueError("API_NEWS_KEY not set in environment")

    if isinstance(from_param, (date, datetime)):
        from_param = from_param.strftime("%Y-%m-%d")
    if isinstance(to, (date, datetime)):
        to = to.strftime("%Y-%m-%d")

    params: dict[str, object] = {
        "q": q,
        "sources": sources,
        "domains": domains,
        "from": from_param,
        "to": to,
        "language": language,
        "sortBy": sort_by,
        "pageSize": page_size,
        "page": page,
    }
    params = {k: v for k, v in params.items() if v is not None}

    headers = {"X-Api-Key": api_key}
    resp = httpx.get(
        "https://newsapi.org/v2/everything",
        params=params,
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    for art in data.get("articles", []) or []:
        art.pop("content", None)
    return json.dumps(data)


agent = Agent(
    tools=[
        get_top_news_headlines,
        search_news_everything,
    ],
    show_tool_calls=True,
    markdown=True,
)

# Example invocations
agent.print_response(
    "Summarize the top 5 US business headlines from NewsAPI.", stream=True
)
