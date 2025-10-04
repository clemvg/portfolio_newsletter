import os

import dotenv

dotenv.load_dotenv()

# TODO: add defaults
TICKERS = os.getenv("TICKERS")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# HuggingFace Configuration
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# News Configuration
USE_LLM_SUMMARIZATION = os.getenv("USE_LLM_SUMMARIZATION", "false").lower() == "true"
