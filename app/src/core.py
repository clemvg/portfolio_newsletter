"""
Core module for the portfolio newsletter service.
"""

import logging

from src.io import email
from src.utils import email_formatter


def generate_newsletter(tickers: list[str], recipients: list[str]) -> str:
    """Generate a newsletter for the given tickers and send it via email."""

    newsletter_content = email_formatter.create_newsletter_content(tickers)

    if recipients:
        email.send_email(newsletter_content, recipients)
        logging.info(f"Newsletter sent to {recipients}")
    else:
        logging.warning("No recipients provided, newsletter not sent")

    return newsletter_content
