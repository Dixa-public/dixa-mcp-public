"""
Tool for getting (listing) the organization activity log from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_organization_activity_log() -> Dict[str, Any]:
    """
    List organization activity log for all conversations.
    
    Returns:
        Dictionary containing the organization activity log entries.
    """
    client = get_dixa_client()
    return client.get_organization_activity_log()

