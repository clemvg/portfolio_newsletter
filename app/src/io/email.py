import logging
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(content: str, recipients: list[str]) -> None:
    """Send email using Gmail SMTP."""

    gmail_user = os.getenv("GMAIL_USER")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_app_password:
        logging.error(
            "Gmail credentials not configured. Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables."
        )
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Portfolio Newsletter - Daily Update"
    msg["From"] = gmail_user
    msg["To"] = ", ".join(recipients)

    html_part = MIMEText(content, "html")
    msg.attach(html_part)

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_user, gmail_app_password)
            server.sendmail(gmail_user, recipients, msg.as_string())

    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        raise
