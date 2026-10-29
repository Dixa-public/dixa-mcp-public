"""
Custom_Attributes-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException
from dixa_api.safety import decode_response, raise_api_error

def get_custom_attribute(
    self,
    custom_attribute_id: str
) -> Dict[str, Any]:
    """
    Get custom attribute definition by ID.
        
    Args:
        custom_attribute_id: The ID of the custom attribute to retrieve (required).
        
    Returns:
        Dictionary containing the custom attribute definition.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/custom-attributes/{custom_attribute_id}"
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return decode_response(response)
    except RequestException as exc:
        raise_api_error(exc)
    


def get_custom_attributes(
    self
) -> Dict[str, Any]:
    """
    List all custom attributes definitions in an organization.
        
    Returns:
        Dictionary containing the list of custom attribute definitions.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/custom-attributes"
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return decode_response(response)
    except RequestException as exc:
        raise_api_error(exc)
    


def patch_end_user_custom_attributes(
    self,
    user_id: str,
    custom_attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Patch (update) custom attributes for an end user.
        
    Args:
        user_id: The ID of the end user to update custom attributes for (required).
        custom_attributes: Dictionary mapping custom attribute IDs to their values (required).
                         Format: Map[UUID, Option[AttributeValue]]
                         - For Text type: string value
                         - For Select type: array of strings (String[])
                         Example: {
                             "2f5515b6-7e98-4f4d-9010-bfd2a27d4f35": "012345",
                             "e14708a6-eed9-495c-9d88-c72331e9e247": ["str1", "str2"]
                         }
        
    Returns:
        Dictionary containing the patched end user attributes.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/{user_id}/custom-attributes"
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.patch(url, json=custom_attributes, headers=headers)
        response.raise_for_status()
        return decode_response(response)
    except RequestException as exc:
        raise_api_error(exc)
    
