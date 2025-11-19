"""
Tool for removing agents from a queue from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def remove_agents_from_queue(
    queue_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Bulk remove agents/admins from the specified queue.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will remove agents from a queue in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get queue_id: Use `list_queues` to list all queues and find the queue ID.
    - To get agent_ids: Use `list_queue_agents` to see current queue members, or use `list_agents` to find agent IDs.
    
    Args:
        queue_id: The ID of the queue (required).
        agent_ids: List of agent/admin IDs to remove from the queue (required, up to 10 members).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Agents removed from queue successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.delete_queue_remove_agents(
        queue_id=queue_id,
        agent_ids=agent_ids
    )

