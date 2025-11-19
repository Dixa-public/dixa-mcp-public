"""
Shared variables for API key management across the application.

This module ensures that context variables and global state are shared
between server.py and tools.base.py.
"""

from typing import Optional
from contextvars import ContextVar

# Context variable to store API key from client auth (for HTTP/SSE transport)
# This is a singleton - all modules import this same instance
_client_api_key: ContextVar[Optional[str]] = ContextVar('client_api_key', default=None)

# Global variable to store API key from initialization (for subprocess transport)
# This will be set by server.py when it processes command-line arguments
_api_key: Optional[str] = None

