"""
Queues-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List
from requests.exceptions import RequestException, HTTPError


def get_queues(self) -> Dict[str, Any]:
    """
    List all queues in an organization.
    
    Returns:
        Dictionary containing the list of queues in an organization.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues"
    
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


def get_queue(self, queue_id: str) -> Dict[str, Any]:
    """
    Get a queue by ID.
    
    Args:
        queue_id: The ID of the queue to retrieve (required).
    
    Returns:
        Dictionary containing the queue information.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues/{queue_id}"
    
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


def get_queue_availability(self, queue_id: str) -> Dict[str, Any]:
    """
    Get queue availability.
    
    Args:
        queue_id: The ID of the queue (required).
    
    Returns:
        Dictionary containing queue availability information.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues/{queue_id}/availability"
    
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


def get_queue_conversation_position(
    self,
    queue_id: str,
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get the position of a conversation in its current queue.
    
    Args:
        queue_id: The ID of the queue (required).
        conversation_id: The ID of the conversation (required).
    
    Returns:
        Dictionary containing the conversation's position in the queue.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues/{queue_id}/conversations/{conversation_id}/position"
    
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


def get_queue_agents(self, queue_id: str) -> Dict[str, Any]:
    """
    List agents/admins that are members of a queue.
    
    Args:
        queue_id: The ID of the queue (required).
    
    Returns:
        Dictionary containing a list of agents/admins that are members of the queue.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues/{queue_id}/members"
    
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


def create_queue(
    self,
    name: str,
    call_functionality: Optional[bool] = None,
    is_default: Optional[bool] = None,
    queue_thresholds: Optional[Dict[str, Any]] = None,
    offer_timeout: Optional[int] = None,
    offer_algorithm: Optional[str] = None,
    wrapup_timeout: Optional[int] = None,
    priority: Optional[int] = None,
    offer_abandoned_conversations: Optional[bool] = None,
    do_not_offer_timeouts: Optional[Dict[str, Any]] = None,
    is_do_not_offer_enabled: Optional[bool] = None,
    preferred_agent_timeouts: Optional[Dict[str, Any]] = None,
    is_preferred_agent_enabled: Optional[bool] = None,
    preferred_agent_offline_timeout: Optional[int] = None,
    personal_agent_offline_timeout: Optional[int] = None,
    is_restricted: Optional[bool] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a queue.
    
    Args:
        name: The name of the queue (required).
        call_functionality: Whether the queue has call functionality (optional).
        is_default: Whether this is the default queue (optional).
        queue_thresholds: Dictionary of queue thresholds (optional).
        offer_timeout: Offer timeout in seconds (optional).
        offer_algorithm: The offering algorithm (e.g., "AllAtOnce", "OneAtATimeRandom") (optional).
        wrapup_timeout: Wrap-up timeout in seconds (optional).
        priority: Queue priority (optional).
        offer_abandoned_conversations: Whether to offer abandoned conversations (optional).
        do_not_offer_timeouts: Dictionary of do-not-offer timeouts by channel (optional).
        is_do_not_offer_enabled: Whether do-not-offer is enabled (optional).
        preferred_agent_timeouts: Dictionary of preferred agent timeouts by channel (optional).
        is_preferred_agent_enabled: Whether preferred agent is enabled (optional).
        preferred_agent_offline_timeout: Preferred agent offline timeout (optional).
        personal_agent_offline_timeout: Personal agent offline timeout (optional).
        is_restricted: Whether the queue is restricted (optional).
        **kwargs: Additional queue properties as per Dixa API specification.
    
    Returns:
        Dictionary containing the created queue.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues"
    
    request_payload = {
        "name": name
    }
    
    if call_functionality is not None:
        request_payload["callFunctionality"] = call_functionality
    if is_default is not None:
        request_payload["isDefault"] = is_default
    if queue_thresholds is not None:
        request_payload["queueThresholds"] = queue_thresholds
    if offer_timeout is not None:
        request_payload["offerTimeout"] = offer_timeout
    if offer_algorithm is not None:
        request_payload["offerAlgorithm"] = offer_algorithm
    if wrapup_timeout is not None:
        request_payload["wrapupTimeout"] = wrapup_timeout
    if priority is not None:
        request_payload["priority"] = priority
    if offer_abandoned_conversations is not None:
        request_payload["offerAbandonedConversations"] = offer_abandoned_conversations
    if do_not_offer_timeouts is not None:
        request_payload["doNotOfferTimeouts"] = do_not_offer_timeouts
    if is_do_not_offer_enabled is not None:
        request_payload["isDoNotOfferEnabled"] = is_do_not_offer_enabled
    if preferred_agent_timeouts is not None:
        request_payload["preferredAgentTimeouts"] = preferred_agent_timeouts
    if is_preferred_agent_enabled is not None:
        request_payload["isPreferredAgentEnabled"] = is_preferred_agent_enabled
    if preferred_agent_offline_timeout is not None:
        request_payload["preferredAgentOfflineTimeout"] = preferred_agent_offline_timeout
    if personal_agent_offline_timeout is not None:
        request_payload["personalAgentOfflineTimeout"] = personal_agent_offline_timeout
    if is_restricted is not None:
        request_payload["isRestricted"] = is_restricted
    
    # Add any additional kwargs
    request_payload.update(kwargs)
    
    payload = {
        "request": request_payload
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


def patch_queue_assign_agents(
    self,
    queue_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Assign one or more agents/admins to a given queue.
    
    Args:
        queue_id: The ID of the queue (required).
        agent_ids: List of agent/admin IDs to assign to the queue (required).
    
    Returns:
        Dictionary containing the list of patch action outcomes with the following structure:
        {
            "data": [
                {
                    "data": "...",
                    "_type": "BulkActionSuccess"
                },
                {
                    "error": {
                        "id": "...",
                        "message": "...",
                        "_type": "..."
                    },
                    "_type": "BulkActionFailure"
                }
            ]
        }
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues/{queue_id}/members"
    
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


def delete_queue_remove_agents(
    self,
    queue_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Bulk remove agents/admins from the specified queue.
    
    Args:
        queue_id: The ID of the queue (required).
        agent_ids: List of agent/admin IDs to remove from the queue (required, up to 10 members).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Agents removed from queue successfully"}.
        On error, returns the error response.
    
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/queues/{queue_id}/members"
    
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
            return {"success": True, "message": "Agents removed from queue successfully"}
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

