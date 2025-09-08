"""
Email Content & Rendering Tests

Purpose: Test email content generation and basic HTML structure.
Focus: Content formatting and email message structure.

Tests should cover:
- Newsletter HTML content generation
- Basic email headers (Subject, To, From)
- Content includes expected ticker data
- Basic HTML structure validation

Keep tests simple and focused on current implementation.
Avoid testing detailed formatting that may change as features evolve.
"""

from unittest.mock import patch, MagicMock

from src.utils.email_formatter import create_newsletter_content
from src.io.email import send_email


class TestEmailRendering:
    """Test email content generation and formatting."""

    def test_newsletter_content_generation(self):
        """Test basic newsletter content is generated with tickers."""
        tickers = ["AAPL", "GOOGL"]
        content = create_newsletter_content(tickers)
        
        # Check basic HTML structure
        assert "<html>" in content
        assert "</html>" in content
        assert "<h2>Portfolio Newsletter</h2>" in content
        
        # Check tickers are included
        for ticker in tickers:
            assert ticker in content

    def test_newsletter_empty_tickers(self):
        """Test newsletter generation with no tickers."""
        content = create_newsletter_content([])
        
        assert "<html>" in content
        assert "<h2>Portfolio Newsletter</h2>" in content

    def test_email_headers_and_structure(self):
        """Test that email has correct headers and recipients."""
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch.dict('os.environ', {
                'GMAIL_USER': 'test@gmail.com',
                'GMAIL_APP_PASSWORD': 'test_password'
            }):
                send_email("<p>Test content</p>", ["user1@example.com", "user2@example.com"])
            
            # Verify email was sent to correct recipients
            args = mock_server.sendmail.call_args[0]
            sent_recipients = args[1]
            message_string = args[2]
            
            assert sent_recipients == ["user1@example.com", "user2@example.com"]
            assert "Subject: Portfolio Newsletter - Daily Update" in message_string
            assert "From: test@gmail.com" in message_string

    def test_html_content_in_email(self):
        """Test that HTML content is properly included in email."""
        test_content = "<h1>Test Newsletter</h1><p>Test ticker: AAPL</p>"
        
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch.dict('os.environ', {
                'GMAIL_USER': 'test@gmail.com',
                'GMAIL_APP_PASSWORD': 'test_password'
            }):
                send_email(test_content, ["recipient@example.com"])
            
            # Verify HTML content is in the sent message
            args = mock_server.sendmail.call_args[0]
            message_string = args[2]
            assert test_content in message_string
            assert "Content-Type: text/html" in message_string