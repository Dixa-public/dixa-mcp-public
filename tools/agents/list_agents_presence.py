"""
Tool for listing agent/admin presence status from the Dixa API.
"""

from typing import List, Dict, Any
from tools.base import get_dixa_client


async def list_agents_presence() -> List[Dict[str, Any]]:
    """
    Get (list) the presence status for all agents/admins in an organization.
    
    Returns:
        List of dictionaries containing presence information for each agent:
        [
            {
                "userId": "...",
                "requestTime": "...",
                "lastSeen": "...",
                "presenceStatus": "...",
                "connectionStatus": "...",
                "activeChannels": [...]
            },
            ...
        ]
    """
    client = get_dixa_client()
    return client.get_agents_presence()

