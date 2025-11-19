"""
Teams-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List
from requests.exceptions import RequestException, HTTPError


def get_teams(self) -> Dict[str, Any]:
    """
    List all teams in an organization.
    
    Returns:
        Dictionary containing the list of teams in an organization.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams"
    
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


def get_team(self, team_id: str) -> Dict[str, Any]:
    """
    Get a team by ID.
    
    Args:
        team_id: The ID of the team to retrieve (required).
    
    Returns:
        Dictionary containing the team information.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams/{team_id}"
    
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


def get_team_agents(self, team_id: str) -> Dict[str, Any]:
    """
    List all agents/admins in a team.
    
    Args:
        team_id: The ID of the team (required).
    
    Returns:
        Dictionary containing a list of agents/admins in the specified team.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams/{team_id}/agents"
    
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


def get_team_presence(
    self,
    team_id: str,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the presence status of all agents/admins in a team.
    
    Args:
        team_id: The ID of the team (required).
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.
    
    Returns:
        Dictionary containing the list of agents/admins presence status in the specified team.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams/{team_id}/presence"
    
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit
    
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


def create_team(self, name: str) -> Dict[str, Any]:
    """
    Create a team.
    
    Args:
        name: The name of the team (required).
    
    Returns:
        Dictionary containing the created team.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams"
    
    payload = {
        "name": name
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


def patch_team_add_agents(
    self,
    team_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Add agents/admins to a team.
    
    Args:
        team_id: The ID of the team (required).
        agent_ids: List of agent/admin IDs to add to the team (required).
    
    Returns:
        Dictionary containing the operation result.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams/{team_id}/agents"
    
    payload = {
        "agentIds": agent_ids
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


def delete_team_remove_agents(
    self,
    team_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Remove agents/admins from a team.
    
    Args:
        team_id: The ID of the team (required).
        agent_ids: List of agent/admin IDs to remove from the team (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Agents removed from team successfully"}.
        On error, returns the error response.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams/{team_id}/agents"
    
    payload = {
        "agentIds": agent_ids
    }
    
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
    
    try:
        response = requests.delete(url, json=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Agents removed from team successfully"}
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


def delete_team(self, team_id: str) -> Dict[str, Any]:
    """
    Delete a team.
    
    Args:
        team_id: The ID of the team to delete (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Team deleted successfully"}.
        On error, returns the error response.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/teams/{team_id}"
    
    headers = {
        **self.headers
    }
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Team deleted successfully"}
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

