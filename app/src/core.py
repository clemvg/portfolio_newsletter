import logging

from src.io.email import send_email
from src.utils.email_formatter import create_newsletter_content


def generate_newsletter(tickers: list[str], recipients: list[str]) -> str:
    """Generate a newsletter for the given tickers and send it via email."""

    newsletter_content = create_newsletter_content(tickers)

    if recipients:
        send_email(newsletter_content, recipients)
        logging.info(f"Newsletter sent to {recipients}")
    else:
        logging.warning("No recipients provided, newsletter not sent")

    return newsletter_content
