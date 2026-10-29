"""
Organization-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException
from dixa_api.safety import decode_response, raise_api_error

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
        return decode_response(response)
    except RequestException as exc:
        raise_api_error(exc)
    
