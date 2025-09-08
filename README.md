# Portfolio Newsletter

## Problem Statement
Keeping up with portfolio news requires significant time investment in massive amount of information.

## Solution
Automated newsletter delivered on personal email on a recurring basis, tailored to your portfolio tickers with high information density (max 3-minute read).

## Further documentation

- For deploying the solution on GCP, see [DEPLOYMENT.md](DEPLOYMENT.md).
- For instructions on running and testing the application locally, refer to the [app/README.md](app/README.md).

## Project Structure

```
portfolio_newsletter/
├── .git/                                    # Git version control
├── README.md                                # Main project README
├── DEPLOYMENT.md                            # Deployment documentation
├── .gitignore                               # Git ignore rules
├── app/                                     # Main application directory
│   ├── src/                                 # Source code
│   │   ├── core.py                          # Main application logic
│   │   ├── io/                              # Input/Output modules
│   │   │   └── email.py                     # Email functionality
│   │   └── utils/                           # Utility modules
│   │       └── email_formatter.py           # Email formatting utilities
│   ├── sandbox/                             # Experimental code
│   │   ├── news/                            # News-related experiments
│   │   │   ├── agno_experiment.py           # Agno experiment
│   │   │   ├── custom_news_api_tool.py      # Custom news API tool
│   │   │   └── hf_llm/                      # Hugging Face LLM experiments
│   │   │       ├── llama_huggingface.py     # Llama model integration
│   │   │       ├── sentiment_analysis.py    # Sentiment analysis
│   │   │       └── summarization.py         # Text summarization
│   │   └── stock_prices/                    # Stock price experiments
│   │       ├── price_change_detection.py    # Price change detection logic
│   │       └── test_price_detection.py      # Price detection tests
│   ├── tests/                               # Test files
│   │   ├── test_email_credentials.py        # Email credentials tests
│   │   └── test_local.py                    # Local testing script
│   ├── venv/                                # Python virtual environment
│   ├── config.py                            # Application configuration
│   ├── job_runner.py                        # Job execution runner
│   ├── requirements.txt                     # Production dependencies
│   ├── requirements-dev.txt                 # Development dependencies
│   ├── README.md                            # App-specific README
│   ├── Dockerfile                           # Docker container definition
│   └── .gitignore                           # App-specific git ignore
└── terraform/                               # Infrastructure as Code
    ├── .terraform.lock.hcl                  # Terraform lock file
    ├── artifact_registry.tf                 # Google Artifact Registry config
    ├── cloud_run.tf                         # Google Cloud Run config
    ├── iam.tf                               # Identity and Access Management
    ├── locals.tf                            # Terraform local variables
    ├── outputs.tf                           # Terraform outputs
    ├── provider.tf                          # Terraform provider config
    ├── scheduler.tf                         # Cloud Scheduler config
    ├── terraform.tfstate                    # Terraform state file
    ├── terraform.tfstate.backup             # Terraform state backup
    ├── terraform.tfvars                     # Terraform variables file
    └── variables.tf                         # Terraform variables
```