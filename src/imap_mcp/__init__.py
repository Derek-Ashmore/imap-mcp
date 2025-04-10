"""
IMAP MCP Server - A Python package for managing IMAP servers.
"""

from .server import app, mcp, IMAPConfig

__version__ = "0.1.0"
__all__ = ["app", "mcp", "IMAPConfig"] 