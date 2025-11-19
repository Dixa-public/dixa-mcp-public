"""
Tool for getting a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_conversation_by_id(
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get a conversation by its ID.
    
    Args:
        conversation_id: The ID of the conversation to retrieve (required).
    
    Returns:
        Dictionary containing the conversation details.
    """
    client = get_dixa_client()
    return client.get_conversation(conversation_id=conversation_id)

