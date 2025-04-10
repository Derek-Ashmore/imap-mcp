"""
Test cases for the IMAP MCP package.
"""

def test_version():
    from imap_mcp import __version__
    assert isinstance(__version__, str) 