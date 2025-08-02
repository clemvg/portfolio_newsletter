# Portfolio Newsletter

## Problem Statement
Keeping up with portfolio news requires significant time investment in massive amount of information.

## Solution
Automated newsletter delivered on a recurring basis, tailored to your portfolio with high information density (max 3-minute read).

## Alert Triggers
- **Stock Price Changes**: ±X% movement (averaged over time period)
- **Quarterly Results**: Company earnings and performance updates
- **Big News Events**: Threshold-based on article volume
- **Context Awareness**: Company-specific vs. global climate news

## Nice-to-Haves
- Macro news impact analysis on individual stocks (e.g., tariffs)
- Configurable alert levels per individual stock

## Development Roadmap

### POC 1 (Local)
- List of tickers via environment variables
- No UI, command-line operation
- Two sections:
  - Stock price changes
  - Big news events (News API integration)

### POC 2 (Cloud)
- Email delivery via subscriber configuration
- Cloud deployment with recurrent job execution


## Setup

### Prerequisites
- Python 3.11+ installed on your system

### Initial Setup
```bash
# Navigate to the app directory
cd app

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Daily Usage
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate when done
deactivate
```


## Environment Variables
- `TICKERS`: Comma-separated list of stock tickers
- `NEWS_API_KEY`: API key for news aggregation
- `EMAIL_SUBSCRIBER`: Email address for newsletter delivery 
