"""
Base DixaClient class for interacting with the Dixa API.

This module provides the core client class that all API methods are attached to.
"""

import os
from typing import Optional
from requests.exceptions import RequestException, HTTPError


class DixaClient:
    """Client for interacting with the Dixa API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Dixa API client.
        
        Args:
            api_key: API key for authentication. If not provided, will use
                    DIXA_API_KEY environment variable.
        
        Raises:
            ValueError: If no API key is provided and DIXA_API_KEY env var is not set.
        """
        self.api_key = api_key or os.getenv("DIXA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Either pass it as a parameter or set "
                "DIXA_API_KEY environment variable."
            )
        self.base_url = "https://dev.dixa.io/v1"
        self.headers = {"Authorization": self.api_key}

