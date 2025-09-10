# Multi-Agent News Retrieval System

A modular news retrieval and analysis system using Agno framework for financial news processing.

## 🏗️ Architecture

### Agents
- **ScraperAgent** (Agno): Intelligent news scraping with NLP query optimization
- **CrossCheckerAgent** (Regular Class): Content similarity validation across multiple APIs
- **SummarizerAgent** (Agno): Natural language summarization with sentiment analysis

### Data Flow
1. **Scraper** → Retrieves news from Exa + Google News APIs
2. **Cross-Checker** → Validates against StockNewsAPI, Polygon, Alpha Vantage  
3. **Summarizer** → Generates summaries using HuggingFace models

## 📁 Project Structure

```
app/sandbox/news/
├── scraper_agent.py          # Agno agent with Jinja2 templates
├── crosschecker_agent.py     # Regular validation class
├── summarizer_agent.py       # Agno agent with HF models
├── main.py                   # Pipeline orchestration
├── base_agent.py            # Base agent class
├── dummy_data.py            # Sample API responses
├── config.py                # Configuration & mode switching  
├── test_workflow.py         # Complete pipeline test
├── templates/
│   ├── scraper_prompt.j2    # Search optimization template
│   └── summarizer_prompt.j2 # Summary generation template
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Test with Dummy Data

```bash
cd app/sandbox/news
python test_workflow.py
```

### 2. Switch to Real APIs

Edit `config.py`:
```python
USE_DUMMY_DATA = False
```

Set environment variables:
```bash
export EXA_API_KEY="your_exa_api_key"
export SERPAPI_KEY="your_serpapi_key"  
export STOCKNEWS_API_KEY="your_stocknews_key"
export POLYGON_API_KEY="your_polygon_key"
export ALPHAVANTAGE_API_KEY="your_alphavantage_key"
export HUGGINGFACE_TOKEN="your_huggingface_token"
```

Uncomment API calls in agent files.

## 🎯 Output Format

```json
{
  "ticker": "AAPL",
  "summary": "Apple beat earnings expectations, confirmed by Reuters and Polygon.",
  "sources": ["Reuters", "Polygon"],
  "sentiment": "positive"
}
```

## ⚙️ Configuration

- **Dummy Mode**: `USE_DUMMY_DATA = True` in `config.py`
- **Similarity Threshold**: Adjust `SIMILARITY_THRESHOLD` for validation strictness
- **Quality Sources**: Modify `QUALITY_NEWS_SOURCES` list
- **Test Tickers**: Change `DEFAULT_TEST_TICKERS`

## 🔧 Extending

1. **Add New Agent**: Inherit from `Agent` class or create regular class
2. **New APIs**: Add to respective agent fetch methods
3. **Templates**: Create new Jinja2 templates in `templates/`
4. **Dummy Data**: Extend `dummy_data.py` for testing

## 📊 Example Output

```
============================================================
TESTING MULTI-AGENT NEWS RETRIEVAL SYSTEM
============================================================

✅ Scraper found articles for 3 tickers
✅ Cross-checker validated 7 articles  
✅ Generated 3 ticker summaries

📈 Ticker: AAPL
📰 Summary: Apple reported strong Q4 earnings driven by iPhone sales...
🔍 Sources: Reuters, Financial Times, Bloomberg
💭 Sentiment: positive
```

## 🛠️ Dependencies

- `jinja2`: Template engine
- `requests`: HTTP requests (when using real APIs)
- `difflib`: Content similarity
- HuggingFace models (via existing `hf_llm` utilities)

## 🔄 Mode Switching

The system supports seamless switching between:
- **Dummy Mode**: Use sample data for testing and development
- **Live Mode**: Connect to real APIs for production use

Simply toggle `USE_DUMMY_DATA` in `config.py` - no code changes required!