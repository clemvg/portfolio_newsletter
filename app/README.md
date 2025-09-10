# Portfolio Newsletter

This README provides instructions for running and testing the portfolio newsletter application locally.

## Setup

### Prerequisites
- Python 3.11+
- Docker (for production testing)

### Environment Setup

1. **Create virtual environment**
```bash
cd app
python3.11 -m venv venv
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optional, for development
```

**Note on requirements files:**
- `requirements.txt`: Contains production dependencies needed to run the application
- `requirements-dev.txt`: Contains development dependencies (testing, linting, etc.) that are not needed in production containers
- For Docker/Cloud Run deployment, only `requirements.txt` is used to keep the container lightweight

Create a `.env` file in the `app/` directory to configure the main environment variables:

- `TICKERS`: A comma-separated list of stock tickers to include in the newsletter. For example:
  ```
  TICKERS="AAPL,GOOGL,MSFT"
  ```
- `EMAIL`: The recipient email address where the newsletter will be sent. For example:
  ```
  EMAIL="your.email@example.com"
  ```

These variables are required for the application to know which tickers to generate news for and which email address to send the newsletter to.

## Running the Application

### Local Development
Run the job directly for testing:
```bash
# From the app/ directory
python job_runner.py
```
This file is the main entrypoint of the newsletter and by running it locally an email with some ticker list dummy content is sent to an email defined in the .env variables.

### Docker (Production Testing)
Start Docker and test in a Cloud Run-like environment locally (build and run):
```bash
docker build -t portfolio-newsletter-job .
docker run --rm -e TICKERS="NVDA,TSLA,AMD" portfolio-newsletter-job
```

**Command breakdown:**
- `-t portfolio-newsletter-job`: Tags the image with a name for reference
- `--rm`: Automatically removes the container after execution
- `-e TICKERS="..."`: Sets environment variables for the container

**Benefits:**
- Tests your app in the same environment as Cloud Run
- Verifies dependencies work in containerized environment
- Allows testing different configurations without affecting local setup

**Managing Docker images:**
```bash
# List all images
docker images

# Remove specific image
docker rmi portfolio-newsletter-job

# Remove all unused images
docker image prune
```

## Development

### IDE Setup (VS Code)
Open the `app/` directory as your workspace root. The `pyrightconfig.json` file ensures proper Python import resolution and IntelliSense for `src/` modules.

### Testing
Run tests using pytest:
```bash
pytest tests/                              # All tests
pytest tests/test_email_smtp.py           # SMTP tests
pytest tests/test_email_rendering.py      # Content tests
pytest tests/test_email_integration.py    # Integration tests
pytest tests/ --cov=src --cov-report=html # With coverage
```

**Test Structure:**
- **SMTP Tests**: Connection, authentication, Gmail configuration
- **Content Tests**: Newsletter HTML generation and formatting
- **Integration Tests**: End-to-end workflow testing

Note that the `pytest.ini` is a file amde for dependency imports purposes.

## Deployment
See deployment documentation in the parent directory for Cloud Run setup and configuration: [DEPLOYMENT.md](../DEPLOYMENT.md).


## Todos

- Architecture diagram of my different components (GCP), to put in readme
- Implement content fetching via agents
- Database if several users with different ticker list
- User interface to update ticker list
- Tests 