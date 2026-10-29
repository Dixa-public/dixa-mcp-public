"""
Base utilities and helpers for creating Dixa MCP tools.

This module provides common functionality for all tools, including
API key extraction and DixaClient initialization.
"""

import os
from typing import Optional
from dixa_api import DixaClient

# Import shared variables - these are the same instances used in server.py
from tools.shared import _client_api_key, _api_key


def get_api_key() -> str:
    """
    Get the API key from various sources in priority order:
    1. HTTP Authorization header (for remote HTTP/SSE servers)
    2. Context variable (from middleware)
    3. Command-line argument
    4. Environment variable
    
    Returns:
        The API key string.
        
    Raises:
        ValueError: If no API key is found in any source.
    """
    # Try to get headers from the HTTP request using FastMCP's built-in function
    api_key_from_header = None
    try:
        from fastmcp.server.dependencies import get_http_headers
        headers = get_http_headers(include={'authorization'})
        if headers:
            # Headers are typically lowercase in HTTP
            auth_header = headers.get("authorization") or headers.get("Authorization", "")
            if auth_header:
                # Remove "Bearer " prefix if present
                api_key_from_header = auth_header.replace("Bearer ", "").strip()
    except Exception:
        # HTTP context is unavailable for local/stdio calls. Never log exception details.
        pass

    # Priority: HTTP header > context var (from middleware) > command-line arg > env var
    final_api_key = (
        api_key_from_header or
        _client_api_key.get() or 
        _api_key or 
        os.getenv("DIXA_API_KEY")
    )
    
    if not final_api_key:
        raise ValueError(
            "API key is required but not found. "
            "For remote servers, ensure the Authorization header is set in your Claude Desktop config. "
            "For local servers, set DIXA_API_KEY environment variable or use --api-key command-line argument."
        )
    
    return final_api_key


def get_dixa_client() -> DixaClient:
    """
    Get a DixaClient instance with the appropriate API key.
    
    Returns:
        A configured DixaClient instance.
        
    Raises:
        ValueError: If no API key is found.
    """
    api_key = get_api_key()
    return DixaClient(api_key=api_key)

