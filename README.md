# IMAP MCP Server

This is a Mission Control Protocol (MCP) server that provides tools for interacting with email accounts via IMAP.

## Features

- Connect to email accounts using IMAP
- List available email folders

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your email credentials (optional):
```
EMAIL=your.email@example.com
EMAIL_PASSWORD=your_password
IMAP_SERVER=imap.gmail.com
```

## Usage

1. Start the server:
```bash
python server.py
```

2. The server provides the following tool:

### list_email_folders

Lists all available folders in the email account.

Parameters:
- `email` (string): Email address to connect to
- `password` (string): Password for the email account
- `imap_server` (string, optional): IMAP server address (default: imap.gmail.com)

Example response:
```json
{
    "status": "success",
    "folders": ["INBOX", "Sent", "Drafts", "Trash"]
}
```

## Security Note

- Never commit your `.env` file or expose your email credentials
- For Gmail accounts, you may need to use an App Password instead of your regular password
- Enable 2-factor authentication and generate an App Password for better security
