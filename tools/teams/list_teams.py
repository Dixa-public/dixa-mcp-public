"""
Tool for listing teams from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_teams() -> Dict[str, Any]:
    """
    List all teams in an organization.
    
    Returns:
        Dictionary containing the list of teams in an organization.
    """
    client = get_dixa_client()
    return client.get_teams()

