"""
Tool for importing conversations into Dixa from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def import_conversations(
    conversations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Import conversations into Dixa.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will import conversations into your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversations: List of conversation objects to import. Each conversation object should contain:
            - genericChannelName (string, required): The conversation channel (e.g., 'email', 'widgetchat')
            - requesterId (string, required): The unique identifier of the requester (end user)
            - requesterConnectionStatus (string, optional): Connection status ('Connected' or 'Disconnected')
            - createdAt (string, required): Creation date in ISO 8601 format
            - direction (string, required): Direction ('Inbound' or 'Outbound')
            - messages (array, required): Array of message objects with content, createdAt, and direction
    
    Returns:
        Dictionary containing the import results.
    """
    client = get_dixa_client()
    return client.create_conversations_import(conversations=conversations)

