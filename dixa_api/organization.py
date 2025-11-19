"""
Organization-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException, HTTPError

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
    
