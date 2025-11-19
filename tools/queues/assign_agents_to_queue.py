"""
Tool for assigning agents to a queue from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def assign_agents_to_queue(
    queue_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Assign one or more agents/admins to a given queue.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will assign agents to a queue in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get queue_id: Use `list_queues` to list all queues and find the queue ID.
    - To get agent_ids: Use `list_agents` to find the agent/admin IDs.
    
    Args:
        queue_id: The ID of the queue (required).
        agent_ids: List of agent/admin IDs to assign to the queue (required).
    
    Returns:
        Dictionary containing the list of patch action outcomes with the following structure:
        {
            "data": [
                {
                    "data": "...",
                    "_type": "BulkActionSuccess"
                },
                {
                    "error": {
                        "id": "...",
                        "message": "...",
                        "_type": "..."
                    },
                    "_type": "BulkActionFailure"
                }
            ]
        }
        
        Note: The response includes both successful and failed assignments. Check the "_type" field
        to determine if each agent was assigned successfully ("BulkActionSuccess") or failed ("BulkActionFailure").
    """
    client = get_dixa_client()
    return client.patch_queue_assign_agents(
        queue_id=queue_id,
        agent_ids=agent_ids
    )

