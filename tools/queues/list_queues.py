"""
Tool for listing queues from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_queues() -> Dict[str, Any]:
    """
    List all queues in an organization.
    
    Returns:
        Dictionary containing the list of queues in an organization.
    """
    client = get_dixa_client()
    return client.get_queues()

