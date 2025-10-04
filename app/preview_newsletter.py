"""Script to generate and preview the newsletter in a browser."""

import logging
import webbrowser
from pathlib import Path

from config import TICKERS
from src.utils.email_formatter import create_newsletter_content

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Generating newsletter preview...")

    # Use default tickers if not set
    if not TICKERS:
        tickers_list = ["AAPL", "GOOGL", "MSFT"]
        logging.warning(
            f"TICKERS not set in .env, using defaults: {tickers_list}"
        )
    else:
        tickers_list = [ticker.strip() for ticker in TICKERS.split(",")]

    logging.info(f"Generating newsletter for tickers: {tickers_list}")

    # Generate the newsletter content
    html_content = create_newsletter_content(tickers_list)

    # Save to file
    output_path = Path(__file__).parent / ".html"
    with open(output_path, "w") as f:
        f.write(html_content)

    logging.info(f"Newsletter saved to: {output_path}")
    logging.info("Opening in browser...")

    # Open in default browser
    webbrowser.open(f"file://{output_path.absolute()}")
