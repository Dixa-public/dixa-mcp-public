"""
Tool for getting a team by ID from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_team_by_id(team_id: str) -> Dict[str, Any]:
    """
    Get a team by ID.
    
    Args:
        team_id: The ID of the team to retrieve (required).
    
    Returns:
        Dictionary containing the team information.
    """
    client = get_dixa_client()
    return client.get_team(team_id=team_id)

