"""
Tool for getting (listing) flows for a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_conversation_flows(
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get (list) flows for a conversation.
    
    Args:
        conversation_id: The ID of the conversation to get flows for (required).
    
    Returns:
        Dictionary containing the list of flows for the conversation.
    """
    client = get_dixa_client()
    return client.get_conversation_flows(conversation_id=conversation_id)

