"""
Tool for listing agents in a queue from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_queue_agents(queue_id: str) -> Dict[str, Any]:
    """
    List agents/admins that are members of a queue.
    
    Args:
        queue_id: The ID of the queue (required).
    
    Returns:
        Dictionary containing a list of agents/admins that are members of the queue.
    """
    client = get_dixa_client()
    return client.get_queue_agents(queue_id=queue_id)

