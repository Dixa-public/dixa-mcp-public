"""
Tool for getting (listing) linked conversations for a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_linked_conversations(
    conversation_id: str
) -> Dict[str, Any]:
    """
    List linked conversations for a conversation.
    
    Args:
        conversation_id: The ID of the conversation to get linked conversations for (required).
    
    Returns:
        Dictionary containing the list of linked conversations.
    """
    client = get_dixa_client()
    return client.get_conversation_linked(conversation_id=conversation_id)

