"""
Tool for getting (listing) internal notes for a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_conversation_notes(
    conversation_id: str
) -> Dict[str, Any]:
    """
    List internal notes for a conversation.
    
    Args:
        conversation_id: The ID of the conversation to get notes for (required).
    
    Returns:
        Dictionary containing the list of internal notes for the conversation.
    """
    client = get_dixa_client()
    return client.get_conversation_notes(conversation_id=conversation_id)

