"""
Settings-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException, HTTPError

def get_business_hours_status(
    self,
    schedule_id: str,
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get business hours status - check if a business is open either right now or at the specified timestamp.
        
    Args:
        schedule_id: The ID of the schedule to check (required).
        timestamp: ISO 8601 timestamp to check (e.g., "2019-08-24T14:15:22Z"). 
                  If not provided, checks current time (optional).
        
    Returns:
        Dictionary containing the business hours status with the following structure:
        {
            "data": {
                "isOpen": true/false,
                "timestamp": "2025-01-08T08:31:25Z"
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/business-hours/schedules/{schedule_id}/status"
        
    params = {}
    if timestamp:
        params["timestamp"] = timestamp
        
    try:
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e
    


def get_business_hours_schedules(self) -> Dict[str, Any]:
    """
    Get (list) business hours schedules in an organization with pagination.
        
    Returns:
        Dictionary containing a list of schedules with the following structure:
        {
            "data": {
                "schedules": [
                    {
                        "name": "...",
                        "id": "..."
                    },
                    ...
                ]
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/business-hours/schedules"
        
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e
    


def get_contact_endpoints(
    self,
    _type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get (list) all available contact endpoints in an organization.
        
    Args:
        _type: Filter by endpoint type (e.g., "TelephonyEndpoint", "EmailEndpoint") (optional).
        
    Returns:
        Dictionary containing a list of contact endpoints with the following structure:
        {
            "data": [
                {
                    "number": "...",
                    "functionality": [...],
                    "name": "...",
                    "_type": "TelephonyEndpoint"
                },
                {
                    "address": "...",
                    "senderOverride": "...",
                    "name": "...",
                    "_type": "EmailEndpoint"
                },
                ...
            ]
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/contact-endpoints"
        
    params = {}
    if _type:
        params["_type"] = _type
        
    try:
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e
    


def get_contact_endpoint(
    self,
    contact_endpoint_id: str
) -> Dict[str, Any]:
    """
    Get a contact endpoint by ID (email or phone number).
        
    Args:
        contact_endpoint_id: The ID of the contact endpoint to retrieve (required).
        
    Returns:
        Dictionary containing the contact endpoint details with the following structure:
        {
            "data": {
                "address": "...",  # For EmailEndpoint
                "senderOverride": "...",  # For EmailEndpoint
                "name": "...",
                "_type": "EmailEndpoint"
            }
        }
        OR
        {
            "data": {
                "number": "...",  # For TelephonyEndpoint
                "functionality": [...],
                "name": "...",
                "_type": "TelephonyEndpoint"
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/contact-endpoints/{contact_endpoint_id}"
        
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e
    
