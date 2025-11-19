"""
Tool for getting (listing) ratings for a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_conversation_ratings(
    conversation_id: str
) -> Dict[str, Any]:
    """
    List ratings for a conversation.
    
    Args:
        conversation_id: The ID of the conversation to get ratings for (required).
    
    Returns:
        Dictionary containing the list of ratings for the conversation.
    """
    client = get_dixa_client()
    return client.get_conversation_ratings(conversation_id=conversation_id)

