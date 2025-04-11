"""
Test cases for the IMAP MCP package.
"""
import pytest
from unittest.mock import MagicMock, patch
from imap_mcp.server import EmailConfig, IMAPConnection, SMTPConnection
from email.message import EmailMessage
import json
import asyncio

@pytest.fixture(autouse=True)
def reset_singletons():
    # Reset singleton instances before each test
    IMAPConnection._instance = None
    SMTPConnection._instance = None

@pytest.fixture
def mock_imap():
    with patch('imaplib.IMAP4_SSL') as mock:
        yield mock

@pytest.fixture
def mock_smtp():
    with patch('smtplib.SMTP_SSL') as mock:
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
        "imap_host": "imap.example.com",
        "imap_port": 993,
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True,
        "smtp_use_ssl": False,
        "smtp_use_tls": True
    }
    
    # Create EmailConfig and connect
    config = EmailConfig(**config_data)
    imap = IMAPConnection.get_instance()
    imap.connect(config)
    
    # Assertions
    mock_imap.assert_called_once_with(config_data["imap_host"], config_data["imap_port"])
    mock_imap_instance.login.assert_called_once_with(config_data["username"], config_data["password"])

@pytest.mark.asyncio
async def test_connect_imap_failure(mock_imap):
    # Setup mock to raise exception
    mock_imap_instance = MagicMock()
    mock_imap_instance.login.side_effect = Exception("Login failed")
    mock_imap.return_value = mock_imap_instance
    
    # Test data
    config_data = {
        "imap_host": "imap.example.com",
        "imap_port": 993,
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "test@example.com",
        "password": "wrong_password",
        "use_ssl": True,
        "smtp_use_ssl": False,
        "smtp_use_tls": True
    }
    
    # Create EmailConfig and expect exception
    config = EmailConfig(**config_data)
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
        "imap_host": "imap.example.com",
        "imap_port": 993,
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True,
        "smtp_use_ssl": False,
        "smtp_use_tls": True
    }
    config = EmailConfig(**config_data)
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
        "imap_host": "imap.example.com",
        "imap_port": 993,
        "smtp_host": "smtp.example.com",
        "smtp_port": 587,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True,
        "smtp_use_ssl": False,
        "smtp_use_tls": True
    }
    config = EmailConfig(**config_data)
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

@pytest.mark.asyncio
async def test_connect_smtp_success(mock_smtp):
    # Setup mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value = mock_smtp_instance
    
    # Test data
    config_data = {
        "imap_host": "imap.example.com",
        "imap_port": 993,
        "smtp_host": "smtp.example.com",
        "smtp_port": 465,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True,
        "smtp_use_ssl": True,
        "smtp_use_tls": False
    }
    
    # Create EmailConfig and connect
    config = EmailConfig(**config_data)
    smtp = SMTPConnection.get_instance()
    smtp.connect(config)
    
    # Assertions
    mock_smtp.assert_called_once_with(config_data["smtp_host"], config_data["smtp_port"])
    mock_smtp_instance.login.assert_called_once_with(config_data["username"], config_data["password"])

@pytest.mark.asyncio
async def test_connect_smtp_tls_success():
    # Setup mock
    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        
        # Test data
        config_data = {
            "imap_host": "imap.example.com",
            "imap_port": 993,
            "smtp_host": "smtp.example.com",
            "smtp_port": 587,
            "username": "test@example.com",
            "password": "password123",
            "use_ssl": True,
            "smtp_use_ssl": False,
            "smtp_use_tls": True
        }
        
        # Create EmailConfig and connect
        config = EmailConfig(**config_data)
        smtp = SMTPConnection.get_instance()
        smtp.connect(config)
        
        # Assertions
        mock_smtp.assert_called_once_with(config_data["smtp_host"], config_data["smtp_port"])
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(config_data["username"], config_data["password"])

@pytest.mark.asyncio
async def test_send_email_success(mock_smtp):
    # Setup mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value = mock_smtp_instance
    
    # First connect to the server
    config_data = {
        "imap_host": "imap.example.com",
        "imap_port": 993,
        "smtp_host": "smtp.example.com",
        "smtp_port": 465,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True,
        "smtp_use_ssl": True,
        "smtp_use_tls": False
    }
    config = EmailConfig(**config_data)
    smtp = SMTPConnection.get_instance()
    smtp.connect(config)
    
    # Call send_email
    to_email = "recipient@example.com"
    subject = "Test Subject"
    body = "Test email content"
    success = smtp.send_email(to_email, subject, body)
    
    # Assertions
    assert success is True
    mock_smtp_instance.send_message.assert_called_once()
    sent_message = mock_smtp_instance.send_message.call_args[0][0]
    assert sent_message["From"] == config_data["username"]
    assert sent_message["To"] == to_email
    assert sent_message["Subject"] == subject
    assert sent_message.get_content().strip() == body.strip()

@pytest.mark.asyncio
async def test_send_email_not_connected(mock_smtp):
    # Setup mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value = mock_smtp_instance
    
    # Create SMTP instance without connecting
    smtp = SMTPConnection.get_instance()
    
    # Call send_email and expect exception
    with pytest.raises(Exception) as exc_info:
        smtp.send_email("recipient@example.com", "Test Subject", "Test email content")
    
    assert "Not connected to SMTP server" in str(exc_info.value) 