# Portfolio Newsletter

A scheduled Cloud Run Job that generates a newsletter for a list of stock tickers.

## Prerequisites

- Python 3.11+
- pip
- Docker
- Terraform

## Local Development

### 1. Setup

First, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the `app/` directory to manage local environment variables. Your `job_runner.py` script will use this file to get the list of tickers when running locally.

```
TICKERS="AAPL,GOOGL,MSFT"
```

### 3. Running the Job Directly

You can execute the job runner script directly to test the core logic. This will use the `TICKERS` variable from your `.env` file.

```bash
python job_runner.py
```

### 4. Running with Docker

To test the application in an environment that mirrors the production setup on Cloud Run, you can build and run the Docker container locally.

This command passes the `TICKERS` environment variable directly to the container, which is how Terraform will configure the job in the cloud.

```bash
# Build the image
docker build -t portfolio-newsletter-job .

# Run the container as a job
docker run --rm -e TICKERS="NVDA,TSLA,AMD" portfolio-newsletter-job
```

## Testing

A local test script is available to test the `core` logic in isolation without running the full application.

```bash
python scripts/test_local.py
```
