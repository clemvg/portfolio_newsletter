"""
Email Integration Tests  

Purpose: Test the complete email workflow from core.generate_newsletter() through delivery.
Focus: End-to-end integration and error propagation between layers.

Tests should cover:
- Complete newsletter generation and email sending flow
- Error handling and propagation from email layer to core
- Integration between content generation and email delivery
- Credential validation at the application level

Keep tests focused on integration concerns, not implementation details.
"""

from unittest.mock import patch, MagicMock
import pytest

from src import core


class TestEmailIntegration:
    """Test complete email workflow integration."""

    def test_newsletter_generation_and_sending(self):
        """Test complete flow from newsletter generation to email delivery."""
        tickers = ["AAPL", "GOOGL"]
        recipients = ["user@example.com"]
        
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch.dict('os.environ', {
                'GMAIL_USER': 'test@gmail.com',
                'GMAIL_APP_PASSWORD': 'test_password'
            }):
                result = core.generate_newsletter(tickers, recipients)
            
            # Verify newsletter content was generated
            assert isinstance(result, str)
            assert "AAPL" in result
            assert "GOOGL" in result
            assert "<html>" in result
            
            # Verify email was sent
            mock_server.login.assert_called_once()
            mock_server.sendmail.assert_called_once()

    def test_newsletter_no_recipients(self, caplog):
        """Test newsletter generation when no recipients provided."""
        tickers = ["AAPL"]
        recipients = []
        
        result = core.generate_newsletter(tickers, recipients)
        
        # Should still generate content
        assert isinstance(result, str)
        assert "AAPL" in result
        
        # Should log warning about no recipients
        assert "No recipients provided" in caplog.text

    def test_email_failure_propagation(self):
        """Test that email sending failures propagate to core layer."""
        tickers = ["AAPL"]
        recipients = ["user@example.com"]
        
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            mock_server = MagicMock()
            mock_server.login.side_effect = Exception("SMTP Error")
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            with patch.dict('os.environ', {
                'GMAIL_USER': 'test@gmail.com',
                'GMAIL_APP_PASSWORD': 'test_password'
            }):
                with pytest.raises(Exception, match="SMTP Error"):
                    core.generate_newsletter(tickers, recipients)

    def test_missing_credentials_handling(self, caplog):
        """Test handling of missing email credentials at integration level."""
        tickers = ["AAPL"]
        recipients = ["user@example.com"]
        
        with patch.dict('os.environ', {}, clear=True):
            result = core.generate_newsletter(tickers, recipients)
        
        # Should still generate content
        assert isinstance(result, str)
        assert "AAPL" in result
        
        # Should log credential error
        assert "Gmail credentials not configured" in caplog.text