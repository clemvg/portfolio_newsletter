import os

import dotenv

dotenv.load_dotenv()

# TODO: add defaults 
TICKERS = os.getenv("TICKERS")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
