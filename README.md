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
│   │   ├── data/                            # Data modules
│   │   │   ├── news_data.py                 # News data fetching
│   │   │   └── stock_data.py                # Stock data fetching
│   │   ├── io/                              # Input/Output modules
│   │   │   └── email.py                     # Email functionality
│   │   └── utils/                           # Utility modules
│   │       └── email_formatter.py           # Email formatting utilities
│   ├── sandbox/                             # Experimental code (not tracked)
│   ├── tests/                               # Test files (not tracked)
│   ├── venv/                                # Python virtual environment
│   ├── config.py                            # Application configuration
│   ├── job_runner.py                        # Job execution runner
│   ├── preview_newsletter.py                # Newsletter preview generator
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