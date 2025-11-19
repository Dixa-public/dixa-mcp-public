"""
Tool for getting the position of a conversation in its queue from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def check_conversation_queue_position(
    queue_id: str,
    conversation_id: str
) -> Dict[str, Any]:
    """
    Get the position of a conversation in its current queue.
    
    Args:
        queue_id: The ID of the queue (required).
        conversation_id: The ID of the conversation (required).
    
    Returns:
        Dictionary containing the conversation's position in the queue.
    """
    client = get_dixa_client()
    return client.get_queue_conversation_position(
        queue_id=queue_id,
        conversation_id=conversation_id
    )

