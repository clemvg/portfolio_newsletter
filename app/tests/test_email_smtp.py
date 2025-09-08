"""
SMTP Connection Tests

Purpose: Test SMTP connectivity, authentication, and basic email sending functionality.
Focus: Infrastructure-level concerns (connection, auth, server communication).

Tests should cover:
- SMTP server connection and authentication
- Environment variable handling for credentials  
- Basic error handling for connection/auth failures
- SSL/TLS configuration

Keep tests focused on SMTP mechanics, not email content formatting.
"""

import os
import smtplib
from unittest.mock import patch, MagicMock

import pytest

from src.io.email import send_email


class TestSMTPConnection:
    """Test SMTP connection and authentication."""

    def test_smtp_connection_success(self):
        """Test successful SMTP connection and email sending."""
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch.dict(os.environ, {
                'GMAIL_USER': 'test@gmail.com',
                'GMAIL_APP_PASSWORD': 'test_password'
            }):
                send_email("<p>Test content</p>", ["recipient@example.com"])
            
            mock_server.login.assert_called_once()
            mock_server.sendmail.assert_called_once()

    def test_smtp_missing_credentials(self, caplog):
        """Test behavior when Gmail credentials are missing."""
        with patch.dict(os.environ, {}, clear=True):
            send_email("<p>Test content</p>", ["recipient@example.com"])
            
        assert "Gmail credentials not configured" in caplog.text

    def test_smtp_authentication_failure(self):
        """Test handling of SMTP authentication errors."""
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_server = MagicMock()
            mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "Authentication failed")
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch.dict(os.environ, {
                'GMAIL_USER': 'test@gmail.com',
                'GMAIL_APP_PASSWORD': 'wrong_password'
            }):
                with pytest.raises(smtplib.SMTPAuthenticationError):
                    send_email("<p>Test content</p>", ["recipient@example.com"])

    def test_smtp_server_configuration(self):
        """Test that correct Gmail SMTP server settings are used."""
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch.dict(os.environ, {
                'GMAIL_USER': 'test@gmail.com',
                'GMAIL_APP_PASSWORD': 'test_password'
            }):
                send_email("<p>Test content</p>", ["recipient@example.com"])
            
            # Verify Gmail SMTP server and port
            args, kwargs = mock_smtp.call_args
            assert args[0] == "smtp.gmail.com"
            assert args[1] == 465
            assert "context" in kwargs