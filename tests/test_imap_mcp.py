"""
Test cases for the IMAP MCP package.
"""
import pytest
from unittest.mock import MagicMock, patch
from imap_mcp.server import IMAPConfig, IMAPConnection
from email.message import EmailMessage
import json
import asyncio

@pytest.fixture
def mock_imap():
    with patch('imaplib.IMAP4_SSL') as mock:
        yield mock

def test_version():
    from imap_mcp import __version__
    assert isinstance(__version__, str)

@pytest.mark.asyncio
async def test_connect_imap_success(mock_imap):
    # Setup mock
    mock_imap_instance = MagicMock()
    mock_imap.return_value = mock_imap_instance
    
    # Test data
    config_data = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True
    }
    
    # Create IMAPConfig and connect
    config = IMAPConfig(**config_data)
    imap = IMAPConnection.get_instance()
    imap.connect(config)
    
    # Assertions
    mock_imap.assert_called_once_with(config_data["host"], config_data["port"])
    mock_imap_instance.login.assert_called_once_with(config_data["username"], config_data["password"])

@pytest.mark.asyncio
async def test_connect_imap_failure(mock_imap):
    # Setup mock to raise exception
    mock_imap_instance = MagicMock()
    mock_imap_instance.login.side_effect = Exception("Login failed")
    mock_imap.return_value = mock_imap_instance
    
    # Test data
    config_data = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "wrong_password",
        "use_ssl": True
    }
    
    # Create IMAPConfig and expect exception
    config = IMAPConfig(**config_data)
    imap = IMAPConnection.get_instance()
    with pytest.raises(Exception) as exc_info:
        imap.connect(config)
    
    assert "Login failed" in str(exc_info.value)

@pytest.mark.asyncio
async def test_list_folders_success(mock_imap):
    # Setup mock
    mock_imap_instance = MagicMock()
    mock_imap.return_value = mock_imap_instance
    
    # First connect to the server
    config_data = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True
    }
    config = IMAPConfig(**config_data)
    imap = IMAPConnection.get_instance()
    imap.connect(config)
    
    # Setup list response
    mock_imap_instance.list.return_value = ('OK', [b'\\HasNoChildren "." INBOX'])
    
    # Call list_folders
    folders = imap.list_folders()
    
    # Assertions
    assert folders == ["INBOX"]
    mock_imap_instance.list.assert_called_once()

@pytest.mark.asyncio
async def test_get_emails_success(mock_imap):
    # Setup mock
    mock_imap_instance = MagicMock()
    mock_imap.return_value = mock_imap_instance
    
    # First connect to the server
    config_data = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True
    }
    config = IMAPConfig(**config_data)
    imap = IMAPConnection.get_instance()
    imap.connect(config)
    
    # Create a test email message
    email_msg = EmailMessage()
    email_msg["Subject"] = "Test Subject"
    email_msg["From"] = "sender@example.com"
    email_msg["Date"] = "Thu, 11 Apr 2024 10:00:00 +0000"
    email_msg.set_content("Test email content")
    
    # Setup mock responses
    mock_imap_instance.select.return_value = ('OK', [b'1'])
    mock_imap_instance.search.return_value = ('OK', [b'1'])
    mock_imap_instance.fetch.return_value = ('OK', [(b'1 (RFC822 {123}', email_msg.as_bytes())])
    
    # Call get_emails
    emails = imap.get_emails("INBOX", limit=2)
    
    # Assertions
    assert len(emails) == 1
    assert emails[0]["subject"] == "Test Subject"
    assert emails[0]["from"] == "sender@example.com"
    assert emails[0]["date"] == "Thu, 11 Apr 2024 10:00:00 +0000"
    mock_imap_instance.select.assert_called_once_with("INBOX")
    mock_imap_instance.search.assert_called_once()
    mock_imap_instance.fetch.assert_called_once() 