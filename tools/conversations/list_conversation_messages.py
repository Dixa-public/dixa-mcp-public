"""
Tool for getting (listing) messages for a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_conversation_messages(
    conversation_id: str
) -> Dict[str, Any]:
    """
    List messages for a conversation.
    
    Args:
        conversation_id: The ID of the conversation to get messages for (required).
    
    Returns:
        Dictionary containing the list of messages for the conversation.
    """
    client = get_dixa_client()
    return client.get_conversation_messages(conversation_id=conversation_id)

