#!/usr/bin/env python3
"""
Local test script to verify Gmail SMTP credentials.
This script tests the connection and authentication with Gmail SMTP server.
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText


def test_gmail_credentials():
    """Test Gmail SMTP credentials and connection."""

    # Get credentials from environment or use the ones from terraform.tfvars
    gmail_user = os.getenv(
        "GMAIL_USER", "portfolio.newsletter.service@gmail.com"
    )
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD", "rwyg eund zdsw zvyv")

    # gmail_user = "autretruc1@gmail.com"
    # gmail_app_password = "PETITport1!"

    print(f"Testing Gmail credentials...")
    print(f"User: {gmail_user}")
    print(f"App Password: {gmail_app_password[:4]}...{gmail_app_password[-4:]}")
    print("-" * 50)

    if not gmail_user or not gmail_app_password:
        print("❌ Error: Gmail credentials not found!")
        print(
            "Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables"
        )
        return False

    try:
        # Create SSL context
        context = ssl.create_default_context()

        print("🔗 Connecting to Gmail SMTP server...")

        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            print("✅ Successfully connected to Gmail SMTP server")

            print("🔐 Attempting to authenticate...")

            # Try to login
            server.login(gmail_user, gmail_app_password)
            print("✅ Successfully authenticated with Gmail!")

            # Test sending a simple email to yourself
            print("📧 Testing email sending...")

            msg = MIMEText(
                "This is a test email from your portfolio newsletter service."
            )
            msg["Subject"] = "Portfolio Newsletter - Credential Test"
            msg["From"] = gmail_user
            msg["To"] = gmail_user  # Send to yourself for testing

            server.sendmail(gmail_user, [gmail_user], msg.as_string())
            print("✅ Successfully sent test email!")

            print(
                "\n🎉 All tests passed! Your Gmail credentials are working correctly."
            )
            return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\nPossible solutions:")
        print("1. Check if the app password is correct")
        print(
            "2. Make sure 2-factor authentication is enabled on your Gmail account"
        )
        print("3. Generate a new app password from Google Account settings")
        print("4. Ensure the email address is correct")
        return False

    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_with_custom_credentials():
    """Test with custom credentials provided by user."""
    print("\n" + "=" * 60)
    print("CUSTOM CREDENTIALS TEST")
    print("=" * 60)

    # Get custom credentials from user
    custom_user = input("Enter your Gmail address: ").strip()
    custom_password = input("Enter your Gmail app password: ").strip()

    if not custom_user or not custom_password:
        print("❌ No credentials provided")
        return False

    # Temporarily set environment variables
    os.environ["GMAIL_USER"] = custom_user
    os.environ["GMAIL_APP_PASSWORD"] = custom_password

    return test_gmail_credentials()


if __name__ == "__main__":
    print("Gmail SMTP Credentials Test")
    print("=" * 40)

    # Test with current credentials
    success = test_gmail_credentials()

    if not success:
        print(
            "\nWould you like to test with different credentials? (y/n): ",
            end="",
        )
        response = input().strip().lower()

        if response in ["y", "yes"]:
            test_with_custom_credentials()

    print("\nTest completed.")
