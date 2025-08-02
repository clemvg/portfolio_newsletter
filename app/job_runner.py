import logging

from config import TICKERS
from src import core

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Starting newsletter generation job.")

    if not TICKERS:
        logging.error("TICKERS environment variable is not set. Exiting.")
    else:
        tickers_list = [ticker.strip() for ticker in TICKERS.split(',')]
        logging.info(f"Generating newsletter for tickers: {tickers_list}")

        result = core.generate_newsletter(tickers_list)

        logging.info("Job finished successfully.")
        logging.info(f"Result: {result}")
