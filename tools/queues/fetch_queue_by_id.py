"""
Tool for getting a queue by ID from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_queue_by_id(queue_id: str) -> Dict[str, Any]:
    """
    Get a queue by ID.
    
    Args:
        queue_id: The ID of the queue to retrieve (required).
    
    Returns:
        Dictionary containing the queue information.
    """
    client = get_dixa_client()
    return client.get_queue(queue_id=queue_id)

