"""
Conversations-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException, HTTPError

def create_conversation_note(
    self,
    conversation_id: str,
    message: str,
    agent_id: Optional[str] = None,
    created_at: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an internal note in a conversation by providing the conversation ID.
        
    Args:
        conversation_id: The ID of the conversation to add a note to (required).
        message: The note message content (required).
        agent_id: The ID of the agent creating the note (optional).
        created_at: ISO 8601 timestamp for when the note was created (e.g., "2021-12-01T12:46:36.581Z[GMT]") (optional).
        
    Returns:
        Dictionary containing the created note with the following structure:
        {
            "data": {
                "id": "...",
                "authorId": "...",
                "createdAt": "...",
                "csid": 9456,
                "message": "..."
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/notes"
        
    payload = {
        "message": message
    }
        
    if agent_id:
        payload["agentId"] = agent_id
        
    if created_at:
        payload["createdAt"] = created_at
        
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
    


def create_conversation_notes_bulk(
    self,
    conversation_id: str,
    notes: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create internal notes in bulk for a conversation by providing the conversation ID.
        
    Args:
        conversation_id: The ID of the conversation to add notes to (required).
        notes: List of note objects to create. Each note should have:
            - message (required): The note message content
            - agentId (optional): The ID of the agent creating the note
            - createdAt (optional): ISO 8601 timestamp for when the note was created (e.g., "2021-12-01T12:46:36.581Z[GMT]")
        
    Returns:
        Dictionary containing the results of the bulk operation with the following structure:
        {
            "data": [
                {
                    "data": {
                        "id": "...",
                        "authorId": "...",
                        "createdAt": "...",
                        "csid": 9456,
                        "message": "..."
                    },
                    "_type": "BulkActionSuccess"
                },
                {
                    "error": {
                        "message": "..."
                    },
                    "_type": "BulkActionFailure"
                }
            ]
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/notes/bulk"
        
    # Prepare the notes data
    notes_data = []
    for note in notes:
        note_dict = {
            "message": note.get("message")
        }
        if "agentId" in note:
            note_dict["agentId"] = note["agentId"]
        if "createdAt" in note:
            note_dict["createdAt"] = note["createdAt"]
        notes_data.append(note_dict)
        
    payload = {
        "data": notes_data
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
    


def patch_conversation_anonymize(
    self,
    conversation_id: str,
    force: bool = False
) -> Dict[str, Any]:
    """
    Request the anonymization of a conversation. This can be done for data protection purposes required by GDPR.
        
    Args:
        conversation_id: The ID of the conversation to anonymize (required).
        force: Whether to force anonymization (default: False) (optional).
        
    Returns:
        Dictionary containing the anonymization request details with the following structure:
        {
            "data": {
                "id": "...",
                "entityType": "ConversationAnonymizationType",
                "_type": "Conversation",
                "initiatedAt": "...",
                "targetEntityId": "...",
                "requestedBy": "..."
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/anonymize"
        
    params = {
        "force": str(force).lower()
    }
        
    try:
        response = requests.patch(url, headers=self.headers, params=params)
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
    


def patch_conversation_message_anonymize(
    self,
    conversation_id: str,
    message_id: str
) -> Dict[str, Any]:
    """
    Request the anonymization of a single message in a conversation.
        
    Args:
        conversation_id: The ID of the conversation containing the message (required).
        message_id: The ID of the message to anonymize (required).
        
    Returns:
        Dictionary containing the anonymization request details with the following structure:
        {
            "data": {
                "id": "...",
                "entityType": "MessageAnonymizationType",
                "_type": "Message",
                "initiatedAt": "...",
                "targetEntityId": "...",
                "requestedBy": "..."
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/messages/{message_id}/anonymize"
        
    try:
        response = requests.patch(url, headers=self.headers)
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
    


def create_conversation_tags_bulk(
    self,
    conversation_id: str,
    tag_names: List[str]
) -> Dict[str, Any]:
    """
    Initiate bulk tag of a conversation and process it asynchronously. 
    If a tag with corresponding name does not exist it will be created.
        
    Args:
        conversation_id: The ID of the conversation to tag (required).
        tag_names: List of tag names to add to the conversation (required).
        
    Returns:
        Dictionary containing the bulk tagging operation details.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/tags/bulk"
        
    payload = {
        "data": [{"name": name} for name in tag_names]
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
    


def update_conversation_claim(
    self,
    conversation_id: str,
    agent_id: str,
    force: bool = False
) -> Dict[str, Any]:
    """
    Claim a conversation for a given agent. To avoid taking over assigned conversations, set the force parameter to false.
        
    Args:
        conversation_id: The ID of the conversation to claim (required).
        agent_id: The ID of the agent to claim the conversation for (required).
        force: Whether to force claiming even if the conversation is already assigned (default: False) (optional).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation claimed successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/claim"
        
    payload = {
        "agentId": agent_id,
        "force": force
    }
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Conversation claimed successfully"}
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
    


def update_conversation_close(
    self,
    conversation_id: str,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Mark a conversation as closed by providing its ID.
        
    Args:
        conversation_id: The ID of the conversation to close (required).
        user_id: The ID of the user closing the conversation (optional).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation closed successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/close"
        
    payload = {}
    if user_id:
        payload["userId"] = user_id
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Conversation closed successfully"}
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
    


def create_conversation(
    self,
    requester_id: str,
    conversation_type: Literal["Callback", "Chat", "ContactForm", "Email", "Sms"],
    message_content: str,
    message_type: Literal["Inbound", "Outbound"],
    subject: Optional[str] = None,
    email_integration_id: Optional[str] = None,
    language: Optional[str] = None,
    agent_id: Optional[str] = None,
    attachments: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create a conversation. For inbound messages the author is assumed to be the requester of the conversation (end user). 
    For outbound messages the author is specified using the agentId field.
        
    Channel-specific requirements:
    - Email: email_integration_id is typically required (format: <email-address>@email.dixa.io)
    - Sms: Only Outbound messages are supported
    - Chat, ContactForm, Callback: Standard requirements apply
        
    Args:
        requester_id: The ID of the requester (end user) (required).
        conversation_type: The type of conversation. Accepted values: "Callback", "Chat", "ContactForm", "Email", "Sms" (required).
        message_content: The content of the message (required).
        message_type: The type of message. Accepted values: "Inbound", "Outbound" (required).
                      Note: Sms only supports "Outbound".
        subject: The subject of the conversation (optional, commonly used for Email).
        email_integration_id: The email integration ID (required for Email type conversations).
                             Format: <email-address>@email.dixa.io (optional).
        language: The language code (e.g., "en") (optional).
        agent_id: The ID of the agent (required for outbound messages) (optional).
        attachments: List of attachment objects with structure: [{"url": "...", "prettyName": "..."}] (optional).
        
    Returns:
        Dictionary containing the created conversation with the following structure:
        {
            "data": {
                "id": 100
            }
        }
        
    Raises:
        ValueError: If conversation_type or message_type is not one of the accepted values, or if Sms is used with Inbound message_type.
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    # Validate conversation_type
    accepted_conversation_types = ["Callback", "Chat", "ContactForm", "Email", "Sms"]
    if conversation_type not in accepted_conversation_types:
        raise ValueError(
            f"Invalid conversation_type value: '{conversation_type}'. "
            f"Accepted values are: {', '.join(accepted_conversation_types)}"
        )
        
    # Validate message_type
    accepted_message_types = ["Inbound", "Outbound"]
    if message_type not in accepted_message_types:
        raise ValueError(
            f"Invalid message_type value: '{message_type}'. "
            f"Accepted values are: {', '.join(accepted_message_types)}"
        )
        
    # Validate Sms only supports Outbound
    if conversation_type == "Sms" and message_type == "Inbound":
        raise ValueError(
            "Sms conversations only support Outbound messages. "
            "Please use message_type='Outbound' for Sms conversations."
        )
        
    url = f"{self.base_url}/conversations"
        
    payload = {
        "requesterId": requester_id,
        "message": {
            "content": {
                "value": message_content,
                "_type": "Text"
            },
            "attachments": attachments or [],
            "_type": message_type
        },
        "_type": conversation_type
    }
        
    if subject:
        payload["subject"] = subject
        
    if email_integration_id:
        payload["emailIntegrationId"] = email_integration_id
        
    if language:
        payload["language"] = language
        
    if agent_id:
        payload["agentId"] = agent_id
        
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
    


def get_conversation(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get a conversation by its ID.
        
    Args:
        conversation_id: The ID of the conversation to retrieve (required).
        
    Returns:
        Dictionary containing the conversation details.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}"
        
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
    


def get_conversation_flows(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get (list) flows for a conversation.
        
    Args:
        conversation_id: The ID of the conversation to get flows for (required).
        
    Returns:
        Dictionary containing the list of flows for the conversation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/flows"
        
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
    


def get_conversation_activity_log(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get (list) the activity log for a conversation.
        
    Args:
        conversation_id: The ID of the conversation to get the activity log for (required).
        
    Returns:
        Dictionary containing the activity log entries for the conversation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/activity-log"
        
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
    


def update_conversation_link(
    self,
    conversation_id: str,
    parent_conversation_id: str
) -> Dict[str, Any]:
    """
    Link a conversation to a parent conversation.
        
    Args:
        conversation_id: The ID of the conversation to link (required).
        parent_conversation_id: The ID of the parent conversation to link to (required).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation linked successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/link"
        
    payload = {
        "parentConversationId": parent_conversation_id
    }
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Conversation linked successfully"}
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
    


def create_conversations_import(
    self,
    conversations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Import conversations into Dixa.
        
    Args:
        conversations: List of conversation objects to import. Each conversation object should contain:
            - genericChannelName (string, required): The conversation channel (e.g., 'email', 'widgetchat')
            - requesterId (string, required): The unique identifier of the requester (end user)
            - requesterConnectionStatus (string, optional): Connection status ('Connected' or 'Disconnected')
            - createdAt (string, required): Creation date in ISO 8601 format
            - direction (string, required): Direction ('Inbound' or 'Outbound')
            - messages (array, required): Array of message objects
        
    Returns:
        Dictionary containing the import results.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/import"
        
    payload = {
        "conversations": conversations
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
    


def get_conversation_notes(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    List internal notes for a conversation.
        
    Args:
        conversation_id: The ID of the conversation to get notes for (required).
        
    Returns:
        Dictionary containing the list of internal notes for the conversation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/notes"
        
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
    


def get_conversation_linked(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    List linked conversations for a conversation.
        
    Args:
        conversation_id: The ID of the conversation to get linked conversations for (required).
        
    Returns:
        Dictionary containing the list of linked conversations.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/linked"
        
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
    


def get_conversation_messages(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    List messages for a conversation.
        
    Args:
        conversation_id: The ID of the conversation to get messages for (required).
        
    Returns:
        Dictionary containing the list of messages for the conversation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/messages"
        
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
    


def get_organization_activity_log(
    self
) -> Dict[str, Any]:
    """
    List organization activity log for all conversations.
        
    Returns:
        Dictionary containing the organization activity log entries.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/activity-log"
        
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
    


def get_conversation_ratings(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    List ratings for a conversation.
        
    Args:
        conversation_id: The ID of the conversation to get ratings for (required).
        
    Returns:
        Dictionary containing the list of ratings for the conversation.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/ratings"
        
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
    


def patch_conversation_custom_attributes(
    self,
    conversation_id: str,
    custom_attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Patch (update) custom attributes for a conversation.
        
    Args:
        conversation_id: The ID of the conversation to update custom attributes for (required).
        custom_attributes: Dictionary of custom attributes to update (required).
                          The structure depends on your organization's custom attribute definitions.
        
    Returns:
        Dictionary containing the updated conversation with custom attributes.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/custom-attributes"
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.patch(url, json=custom_attributes, headers=headers)
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
    


def update_conversation_reopen(
    self,
    conversation_id: str
) -> Dict[str, Any]:
    """
    Reopen a conversation by providing its ID.
        
    Args:
        conversation_id: The ID of the conversation to reopen (required).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation reopened successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/reopen"
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Conversation reopened successfully"}
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
    


def post_search_conversations(
    self,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None,
    filters: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Search for conversations containing a particular text or by filter or combine them both.
        
    Args:
        page_key: Base64 encoded form of pagination query parameters. Do not try to construct or change programmatically as the internal structure may change without notice (optional).
        page_limit: Maximum number of results per page. Must be less than or equal to 50. May be used in combination with pageKey to change the number of results in between page requests (optional).
        filters: Dictionary containing filter conditions to apply to the search (optional).
        query: Dictionary containing query parameters for text search (optional).
        
    Returns:
        Dictionary containing the search results with the following structure:
        {
            "data": [
                {
                    "id": 1234,
                    "highlights": {}
                }
            ],
            "meta": {
                "next": "/<api-version>/search/conversations/?pageKey=..."
            }
        }
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/search/conversations"
    
    # Validate page_limit doesn't exceed API maximum
    if page_limit is not None and page_limit > 50:
        raise ValueError(f"page_limit must be less than or equal to 50, but got {page_limit}")
        
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit
        
    payload = {}
    if filters:
        payload["filters"] = filters
    if query:
        payload["query"] = query
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        # Only send JSON body if there's something to send
        if payload:
            response = requests.post(url, json=payload, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, params=params)
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
    


def update_conversation_tag(
    self,
    conversation_id: str,
    tag_id: str
) -> Dict[str, Any]:
    """
    Tag a conversation. You may only use active tags to tag conversations.
        
    Args:
        conversation_id: The ID of the conversation to tag (required).
        tag_id: The ID of the tag to apply (required).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation tagged successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/tags/{tag_id}"
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Conversation tagged successfully"}
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
    


def delete_conversation_tag(
    self,
    conversation_id: str,
    tag_id: str
) -> Dict[str, Any]:
    """
    Untag a conversation. You may remove active or inactive tags from a conversation.
        
    Args:
        conversation_id: The ID of the conversation to untag (required).
        tag_id: The ID of the tag to remove (required).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation untagged successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/tags/{tag_id}"
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Conversation untagged successfully"}
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
    


def update_conversation_followup(
    self,
    conversation_id: str,
    follow_up: bool
) -> Dict[str, Any]:
    """
    Update the follow-up status of a conversation.
        
    Args:
        conversation_id: The ID of the conversation to update (required).
        follow_up: The follow-up status to set (True for follow-up, False otherwise) (required).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation follow-up status updated successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/conversations/{conversation_id}/followup"
        
    payload = {
        "followUp": follow_up
    }
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Conversation follow-up status updated successfully"}
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
    
