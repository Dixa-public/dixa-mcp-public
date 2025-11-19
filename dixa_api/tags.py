"""
Tags-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional
from requests.exceptions import RequestException, HTTPError


def get_tags(self, include_deactivated: Optional[bool] = None) -> Dict[str, Any]:
    """
    List all tags in an organization. Only active tags are returned by default.
    To include deactivated tags use include_deactivated=True.
    
    Args:
        include_deactivated: Whether to include deactivated tags in the response.
                           If not provided, only active tags are listed (default: False).
    
    Returns:
        Dictionary containing the list of all tags in an organization.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/tags"
    
    params = {}
    if include_deactivated is not None:
        params["includeDeactivated"] = include_deactivated
    
    try:
        response = requests.get(url, headers=self.headers, params=params if params else None)
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


def get_tag(self, tag_id: str) -> Dict[str, Any]:
    """
    Get a tag by ID.
    
    Args:
        tag_id: The ID of the tag to retrieve (required).
    
    Returns:
        Dictionary containing the tag information.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/tags/{tag_id}"
    
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


def create_tag(
    self,
    name: str,
    color: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a tag.
    
    Args:
        name: The name of the tag (required).
        color: The color of the tag (e.g., "#000000") (optional).
    
    Returns:
        Dictionary containing the created tag or an existing tag with the same name.
        Note that the tag is not updated to match the input in case it already exists.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/tags"
    
    payload = {
        "name": name
    }
    
    if color:
        payload["color"] = color
    
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
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


def patch_tag_activate(self, tag_id: str) -> Dict[str, Any]:
    """
    Activate a tag.
    
    Args:
        tag_id: The ID of the tag to activate (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Tag activated successfully"}.
        On error, returns the error response.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/tags/{tag_id}/activate"
    
    headers = {
        **self.headers
    }
    
    try:
        response = requests.patch(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Tag activated successfully"}
        if response.content:
            return response.json()
        return {"success": True}
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


def patch_tag_deactivate(self, tag_id: str) -> Dict[str, Any]:
    """
    Deactivate a tag.
    
    Args:
        tag_id: The ID of the tag to deactivate (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Tag deactivated successfully"}.
        On error, returns the error response.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/tags/{tag_id}/deactivate"
    
    headers = {
        **self.headers
    }
    
    try:
        response = requests.patch(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Tag deactivated successfully"}
        if response.content:
            return response.json()
        return {"success": True}
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


def delete_tag(self, tag_id: str) -> Dict[str, Any]:
    """
    Delete a tag and all its associations. Note that this operation is irreversible.
    
    Args:
        tag_id: The ID of the tag to delete (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Tag deleted successfully"}.
        On error, returns the error response.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/tags/{tag_id}"
    
    headers = {
        **self.headers
    }
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Tag deleted successfully"}
        if response.content:
            return response.json()
        return {"success": True}
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


def get_conversation_tags(self, conversation_id: str) -> Dict[str, Any]:
    """
    Get the tags for a particular conversation by providing the conversation ID.
    
    Args:
        conversation_id: The ID of the conversation (required).
    
    Returns:
        Dictionary containing the list of tags for the conversation.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/tags"
    
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

