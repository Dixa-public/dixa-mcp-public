"""
Tool for getting tags for a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_conversation_tags(conversation_id: str) -> Dict[str, Any]:
    """
    Get the tags for a particular conversation by providing the conversation ID.
    
    Args:
        conversation_id: The ID of the conversation (required).
    
    Returns:
        Dictionary containing the list of tags for the conversation.
    """
    client = get_dixa_client()
    return client.get_conversation_tags(conversation_id=conversation_id)

