import logging

from config import EMAIL_RECIPIENTS, TICKERS
from src import core

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Starting newsletter generation job.")

    if not TICKERS:
        logging.error("TICKERS environment variable is not set. Exiting.")
        exit(1)

    if not EMAIL_RECIPIENTS:
        logging.error("EMAIL_RECIPIENTS environment variable is not set. Exiting.")
        exit(1)

    # Parse environment variables
    tickers_list = [ticker.strip() for ticker in TICKERS.split(",")]
    recipients_list = [email.strip() for email in EMAIL_RECIPIENTS.split(",")]

    logging.info(f"Generating newsletter for tickers: {tickers_list}")
    logging.info(f"Sending to recipients: {recipients_list}")

    result = core.generate_newsletter(tickers_list, recipients_list)

    logging.info("Job finished successfully.")
    logging.info(f"Newsletter content generated: {len(result)} characters")
