"""
Users-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException, HTTPError

def get_end_users(
    self,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all end users in an organization.
        
    Args:
        page_key: Base64 encoded form of pagination query parameters (optional).
        page_limit: Maximum number of results per page (optional).
        
    Returns:
        Dictionary containing the list of end users.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers"
        
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers, params=params)
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
    


def get_end_user(
    self,
    user_id: str
) -> Dict[str, Any]:
    """
    Get an end user by ID.
        
    Args:
        user_id: The ID of the end user to retrieve (required).
        
    Returns:
        Dictionary containing the end user details.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/{user_id}"
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers)
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
    


def create_end_user(
    self,
    display_name: str,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    additional_emails: Optional[List[str]] = None,
    additional_phone_numbers: Optional[List[str]] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[List[str]] = None,
    avatar_url: Optional[str] = None,
    external_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an end user.
        
    Args:
        display_name: The display name of the end user (required).
        email: The email address of the end user (optional).
        phone_number: The phone number of the end user (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: The first name of the end user (optional).
        last_name: The last name of the end user (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL to the avatar image (optional).
        external_id: External identifier for the end user (optional).
        
    Returns:
        Dictionary containing the created end user.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers"
        
    payload = {
        "displayName": display_name
    }
        
    if email:
        payload["email"] = email
    if phone_number:
        payload["phoneNumber"] = phone_number
    if additional_emails:
        payload["additionalEmails"] = additional_emails
    if additional_phone_numbers:
        payload["additionalPhoneNumbers"] = additional_phone_numbers
    if first_name:
        payload["firstName"] = first_name
    if last_name:
        payload["lastName"] = last_name
    if middle_names:
        payload["middleNames"] = middle_names
    if avatar_url:
        payload["avatarUrl"] = avatar_url
    if external_id:
        payload["externalId"] = external_id
        
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
    


def create_end_users_bulk(
    self,
    end_users: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create multiple end users in a single bulk action.
        
    Args:
        end_users: List of end user objects to create (required).
                  Each object should contain the same fields as create_end_user.
        
    Returns:
        Dictionary containing the results of the bulk creation operation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/bulk"
        
    payload = {
        "data": end_users
    }
        
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
    


def patch_end_user(
    self,
    user_id: str,
    display_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    additional_emails: Optional[List[str]] = None,
    additional_phone_numbers: Optional[List[str]] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[List[str]] = None,
    avatar_url: Optional[str] = None,
    external_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Patch (partially update) an end user.
        
    Args:
        user_id: The ID of the end user to update (required).
        display_name: The display name of the end user (optional).
        email: The email address of the end user (optional).
        phone_number: The phone number of the end user (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: The first name of the end user (optional).
        last_name: The last name of the end user (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL to the avatar image (optional).
        external_id: External identifier for the end user (optional).
        
    Returns:
        Dictionary containing the updated end user.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/{user_id}"
        
    payload = {}
        
    if display_name:
        payload["displayName"] = display_name
    if email:
        payload["email"] = email
    if phone_number:
        payload["phoneNumber"] = phone_number
    if additional_emails is not None:
        payload["additionalEmails"] = additional_emails
    if additional_phone_numbers is not None:
        payload["additionalPhoneNumbers"] = additional_phone_numbers
    if first_name:
        payload["firstName"] = first_name
    if last_name:
        payload["lastName"] = last_name
    if middle_names is not None:
        payload["middleNames"] = middle_names
    if avatar_url:
        payload["avatarUrl"] = avatar_url
    if external_id:
        payload["externalId"] = external_id
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.patch(url, json=payload, headers=headers)
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
    


def patch_end_users_bulk(
    self,
    end_users: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Patch (partially update) multiple end users in a single bulk action.
        
    Args:
        end_users: List of end user objects to patch (required).
                  Each object should contain the user ID and fields to update.
        
    Returns:
        Dictionary containing the results of the bulk patch operation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/bulk"
        
    payload = {
        "data": end_users
    }
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.patch(url, json=payload, headers=headers)
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
    


def update_end_user(
    self,
    user_id: str,
    display_name: str,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    additional_emails: Optional[List[str]] = None,
    additional_phone_numbers: Optional[List[str]] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[List[str]] = None,
    avatar_url: Optional[str] = None,
    external_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update (full update) an end user.
        
    Args:
        user_id: The ID of the end user to update (required).
        display_name: The display name of the end user (required).
        email: The email address of the end user (optional).
        phone_number: The phone number of the end user (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: The first name of the end user (optional).
        last_name: The last name of the end user (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL to the avatar image (optional).
        external_id: External identifier for the end user (optional).
        
    Returns:
        Dictionary containing the updated end user.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/{user_id}"
        
    payload = {
        "displayName": display_name
    }
        
    if email:
        payload["email"] = email
    if phone_number:
        payload["phoneNumber"] = phone_number
    if additional_emails is not None:
        payload["additionalEmails"] = additional_emails
    if additional_phone_numbers is not None:
        payload["additionalPhoneNumbers"] = additional_phone_numbers
    if first_name:
        payload["firstName"] = first_name
    if last_name:
        payload["lastName"] = last_name
    if middle_names is not None:
        payload["middleNames"] = middle_names
    if avatar_url:
        payload["avatarUrl"] = avatar_url
    if external_id:
        payload["externalId"] = external_id
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, json=payload, headers=headers)
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
    


def update_end_users_bulk(
    self,
    end_users: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update (full update) multiple end users in a single bulk action.
        
    Args:
        end_users: List of end user objects to update (required).
                  Each object should contain the user ID and all required fields.
        
    Returns:
        Dictionary containing the results of the bulk update operation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/bulk"
        
    payload = {
        "data": end_users
    }
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, json=payload, headers=headers)
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
    


def get_end_user_conversations(
    self,
    user_id: str,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List conversations requested by a specific end user.
        
    Args:
        user_id: The ID of the end user (required).
        page_key: Base64 encoded form of pagination query parameters (optional).
        page_limit: Maximum number of results per page (optional).
        
    Returns:
        Dictionary containing the list of conversations for the end user.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/{user_id}/conversations"
        
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers, params=params)
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
    


def patch_end_user_anonymize(
    self,
    user_id: str,
    force: bool = False
) -> Dict[str, Any]:
    """
    Request the anonymization of an end user. This can be done for data protection purposes required by GDPR.
        
    Args:
        user_id: The ID of the end user to anonymize (required).
        force: Whether to force anonymization (default: False) (optional).
        
    Returns:
        Dictionary containing the anonymization request details.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/endusers/{user_id}/anonymize"
        
    params = {}
    if force:
        params["force"] = "true"
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.patch(url, headers=headers, params=params)
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
    
