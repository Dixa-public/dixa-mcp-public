"""
Tool for getting (listing) the activity log for a conversation from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_conversation_activity_log(
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get (list) the activity log for a conversation.
    
    Args:
        conversation_id: The ID of the conversation to get the activity log for (required).
    
    Returns:
        Dictionary containing the activity log entries for the conversation.
    """
    client = get_dixa_client()
    return client.get_conversation_activity_log(conversation_id=conversation_id)

