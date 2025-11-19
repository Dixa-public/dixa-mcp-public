"""
Tool for getting queue availability from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def check_queue_availability(queue_id: str) -> Dict[str, Any]:
    """
    Get queue availability.
    
    Args:
        queue_id: The ID of the queue (required).
    
    Returns:
        Dictionary containing queue availability information.
    """
    client = get_dixa_client()
    return client.get_queue_availability(queue_id=queue_id)

