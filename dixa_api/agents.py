"""
Agents-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException, HTTPError

def get_agent(self, agent_id: str) -> Dict[str, Any]:
    """
    Get an agent/admin by ID from the Dixa API.
        
    Args:
        agent_id: The ID of the agent to retrieve.
        
    Returns:
        Dictionary containing agent information with the following structure:
        {
            "data": {
                "id": "...",
                "createdAt": "...",
                "displayName": "...",
                "email": "...",
                "avatarUrl": "...",
                "phoneNumber": "...",
                "additionalEmails": [...],
                "additionalPhoneNumbers": [...],
                "firstName": "...",
                "lastName": "...",
                "middleNames": [...],
                "roles": [...]
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/agents/{agent_id}"
        
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
    


def get_agents(
    self,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get (list) all agents/admins in an organization.
        
    It is possible to filter by one of the mutually exclusive parameters: email or phone number.
    In case both are provided, an error is returned.
        
    Args:
        email: Filter by email address (mutually exclusive with phone).
        phone: Filter by phone number (mutually exclusive with email).
        page_key: Pagination key for retrieving next page of results.
        page_limit: Maximum number of results per page.
        
    Returns:
        Dictionary containing a list of agents with the following structure:
        {
            "data": [
                {
                    "id": "...",
                    "createdAt": "...",
                    "displayName": "...",
                    "email": "...",
                    "avatarUrl": "...",
                    "additionalEmails": [...],
                    "additionalPhoneNumbers": [...],
                    "middleNames": [...],
                    "roles": [...]
                },
                ...
            ]
        }
        
    Raises:
        ValueError: If both email and phone are provided (mutually exclusive).
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    # Validate mutually exclusive parameters
    if email and phone:
        raise ValueError("email and phone parameters are mutually exclusive. Provide only one.")
        
    url = f"{self.base_url}/agents"
    params = {}
        
    if email:
        params["email"] = email
    if phone:
        params["phone"] = phone
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
        
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
    


def get_agents_presence(self) -> list:
    """
    Get (list) the presence status for all agents/admins in an organization.
        
    Returns:
        List of dictionaries containing presence information for each agent:
        [
            {
                "userId": "...",
                "requestTime": "...",
                "lastSeen": "...",
                "presenceStatus": "...",
                "connectionStatus": "...",
                "activeChannels": [...]
            },
            ...
        ]
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/agents/presence"
        
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
    


def get_agent_teams(self, agent_id: str) -> Dict[str, Any]:
    """
    List the teams in which the agent/admin is a member.
        
    Args:
        agent_id: The ID of the agent to get teams for.
        
    Returns:
        Dictionary containing a list of teams with the following structure:
        {
            "data": [
                {
                    "id": "..."
                },
                ...
            ]
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/agents/{agent_id}/teams"
        
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
    


def create_agent(
    self,
    display_name: str,
    email: str,
    phone_number: Optional[str] = None,
    additional_emails: Optional[list] = None,
    additional_phone_numbers: Optional[list] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[list] = None,
    avatar_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new agent/admin in the organization.
        
    Args:
        display_name: Display name for the agent (required).
        email: Email address for the agent (required).
        phone_number: Primary phone number (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: First name of the agent (optional).
        last_name: Last name of the agent (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL for the agent's avatar image (optional).
        
    Returns:
        Dictionary containing the created agent information with the following structure:
        {
            "data": {
                "id": "...",
                "createdAt": "...",
                "displayName": "...",
                "email": "...",
                "avatarUrl": "...",
                "phoneNumber": "...",
                "additionalEmails": [...],
                "additionalPhoneNumbers": [...],
                "firstName": "...",
                "lastName": "...",
                "middleNames": [...],
                "roles": [...]
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/agents"
        
    payload = {
        "displayName": display_name,
        "email": email
    }
        
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
    if middle_names is not None:
        payload["middleNames"] = middle_names
    if avatar_url:
        payload["avatarUrl"] = avatar_url
        
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
    


def patch_agent(
    self,
    agent_id: str,
    display_name: Optional[str] = None,
    additional_emails: Optional[list] = None,
    additional_phone_numbers: Optional[list] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[list] = None,
    avatar_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Patch (partial update) an agent/admin in the organization.
        
    Args:
        agent_id: The ID of the agent to update (required).
        display_name: Display name for the agent (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: First name of the agent (optional).
        last_name: Last name of the agent (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL for the agent's avatar image (optional).
        
    Returns:
        Dictionary containing the updated agent information with the following structure:
        {
            "data": {
                "id": "...",
                "createdAt": "...",
                "displayName": "...",
                "email": "...",
                "avatarUrl": "...",
                "phoneNumber": "...",
                "additionalEmails": [...],
                "additionalPhoneNumbers": [...],
                "firstName": "...",
                "lastName": "...",
                "middleNames": [...],
                "roles": [...]
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/agents/{agent_id}"
        
    payload = {}
        
    if display_name is not None:
        payload["displayName"] = display_name
    if additional_emails is not None:
        payload["additionalEmails"] = additional_emails
    if additional_phone_numbers is not None:
        payload["additionalPhoneNumbers"] = additional_phone_numbers
    if first_name is not None:
        payload["firstName"] = first_name
    if last_name is not None:
        payload["lastName"] = last_name
    if middle_names is not None:
        payload["middleNames"] = middle_names
    if avatar_url is not None:
        payload["avatarUrl"] = avatar_url
        
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
    


def update_agent(
    self,
    agent_id: str,
    display_name: str,
    phone_number: Optional[str] = None,
    additional_emails: Optional[list] = None,
    additional_phone_numbers: Optional[list] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[list] = None,
    avatar_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update (full update) an agent/admin in the organization using PUT.
        
    Args:
        agent_id: The ID of the agent to update (required).
        display_name: Display name for the agent (required).
        phone_number: Primary phone number (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: First name of the agent (optional).
        last_name: Last name of the agent (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL for the agent's avatar image (optional).
        
    Returns:
        Dictionary containing the updated agent information with the following structure:
        {
            "data": {
                "id": "...",
                "createdAt": "...",
                "displayName": "...",
                "email": "...",
                "avatarUrl": "...",
                "phoneNumber": "...",
                "additionalEmails": [...],
                "additionalPhoneNumbers": [...],
                "firstName": "...",
                "lastName": "...",
                "middleNames": [...],
                "roles": [...]
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/agents/{agent_id}"
        
    payload = {
        "displayName": display_name
    }
        
    if phone_number is not None:
        payload["phoneNumber"] = phone_number
    if additional_emails is not None:
        payload["additionalEmails"] = additional_emails
    if additional_phone_numbers is not None:
        payload["additionalPhoneNumbers"] = additional_phone_numbers
    if first_name is not None:
        payload["firstName"] = first_name
    if last_name is not None:
        payload["lastName"] = last_name
    if middle_names is not None:
        payload["middleNames"] = middle_names
    if avatar_url is not None:
        payload["avatarUrl"] = avatar_url
        
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
    


def update_agent_working_channel(
    self,
    agent_id: str,
    channel: str,
    working: bool
) -> Dict[str, Any]:
    """
    Update the working channel status of an agent/admin.
        
    Args:
        agent_id: The ID of the agent to update (required).
        channel: The channel name. Accepted values: "Email", "InteractiveChat", "Messaging", "Speak" (required).
        working: Whether the agent is working on this channel (required).
        
    Raises:
        ValueError: If channel is not one of the accepted values.
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    # Validate channel value
    accepted_channels = ["Email", "InteractiveChat", "Messaging", "Speak"]
    if channel not in accepted_channels:
        raise ValueError(
            f"Invalid channel value: '{channel}'. "
            f"Accepted values are: {', '.join(accepted_channels)}"
        )
        
    url = f"{self.base_url}/agents/{agent_id}/presence/working-channel"
        
    payload = {
        "channel": channel,
        "working": working
    }
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        # 204 No Content means success
        if response.status_code == 204:
            return {"success": True, "message": "Agent working channel updated successfully"}
        # If there's content, return it
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
    
