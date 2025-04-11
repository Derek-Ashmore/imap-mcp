"""
IMAP MCP Server - A Python package for managing IMAP servers.
"""

from .server import mcp, EmailConfig, IMAPConnection, SMTPConnection

__version__ = "0.1.0"
__all__ = ["mcp", "EmailConfig", "IMAPConnection", "SMTPConnection"] 