import os
import requests
from typing import Optional, Dict, Any
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
    
    def get_organization(self) -> Dict[str, Any]:
        """
        Get organization information from the Dixa API.
        
        Returns:
            Dict containing the organization data from the API response.
        
        Raises:
            HTTPError: If the API returns an HTTP error status (4xx, 5xx).
            RequestException: If there's an error making the request.
        """
        url = f"{self.base_url}/organization"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except HTTPError as e:
            # Provide more context about the error
            error_msg = f"HTTP {response.status_code} error: {e}"
            try:
                error_detail = response.json()
                error_msg += f" - {error_detail}"
            except ValueError:
                error_msg += f" - {response.text}"
            raise HTTPError(error_msg, response=response) from e
        except RequestException as e:
            raise RequestException(f"Request failed: {e}") from e

