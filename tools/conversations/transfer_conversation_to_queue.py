"""
Tool for transferring a conversation to a queue from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def transfer_conversation_to_queue(
    conversation_id: str,
    queue_id: str,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transfer a conversation to a target queue.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will transfer a conversation to a queue in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get conversation_id: Use `fetch_conversation_by_id` or `search_conversations` to find the conversation ID first.
    - To get queue_id: Use `list_queues` to list all queues and find the target queue ID.
    - To get user_id: Use `list_agents` to find the agent/admin ID if you want to specify who originated the transfer.
    
    Args:
        conversation_id: The ID of the conversation to transfer (required).
        queue_id: The ID of the target queue (required).
        user_id: The ID of the agent/admin originating the transfer (optional).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation transferred to queue successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_conversation_transfer_queue(
        conversation_id=conversation_id,
        queue_id=queue_id,
        user_id=user_id
    )
