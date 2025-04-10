"""
Test cases for the IMAP MCP package.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from imap_mcp.server import app, IMAPConfig
from email.message import EmailMessage

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_imap():
    with patch('imaplib.IMAP4_SSL') as mock:
        yield mock

def test_version():
    from imap_mcp import __version__
    assert isinstance(__version__, str)

def test_connect_imap_success(client, mock_imap):
    # Setup mock
    mock_imap_instance = MagicMock()
    mock_imap.return_value = mock_imap_instance
    
    # Test data
    config = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True
    }
    
    # Make request
    response = client.post("/mcp/connect", json=config)
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["status"] == "connected"
    assert response.json()["config"] == config
    mock_imap.assert_called_once_with(config["host"], config["port"])
    mock_imap_instance.login.assert_called_once_with(config["username"], config["password"])

def test_connect_imap_failure(client, mock_imap):
    # Setup mock to raise exception
    mock_imap_instance = MagicMock()
    mock_imap_instance.login.side_effect = Exception("Login failed")
    mock_imap.return_value = mock_imap_instance
    
    # Test data
    config = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "wrong_password",
        "use_ssl": True
    }
    
    # Make request
    response = client.post("/mcp/connect", json=config)
    
    # Assertions
    assert response.status_code == 500
    assert response.json()["detail"] == "Login failed"

def test_list_folders_success(client, mock_imap):
    # Setup mock
    mock_imap_instance = MagicMock()
    mock_imap.return_value = mock_imap_instance
    
    # First connect to the server
    config = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True
    }
    client.post("/mcp/connect", json=config)
    
    # Setup list response
    mock_imap_instance.list.return_value = ('OK', [b'\\HasNoChildren "." INBOX'])
    
    # Make request
    response = client.post("/mcp/list_folders")
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["folders"] == ["INBOX"]
    mock_imap_instance.list.assert_called_once()

def test_get_emails_success(client, mock_imap):
    # Setup mock
    mock_imap_instance = MagicMock()
    mock_imap.return_value = mock_imap_instance
    
    # First connect to the server
    config = {
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "password123",
        "use_ssl": True
    }
    client.post("/mcp/connect", json=config)
    
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
    
    # Test data
    params = {
        "folder": "INBOX",
        "limit": 2
    }
    
    # Make request
    response = client.post("/mcp/get_emails", params=params)
    
    # Assertions
    assert response.status_code == 200
    emails = response.json()["emails"]
    assert len(emails) == 1
    assert emails[0]["subject"] == "Test Subject"
    assert emails[0]["from"] == "sender@example.com"
    assert emails[0]["date"] == "Thu, 11 Apr 2024 10:00:00 +0000"
    mock_imap_instance.select.assert_called_once_with(params["folder"])
    mock_imap_instance.search.assert_called_once()
    mock_imap_instance.fetch.assert_called_once() 