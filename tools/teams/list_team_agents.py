"""
Tool for listing agents in a team from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_team_agents(team_id: str) -> Dict[str, Any]:
    """
    List all agents/admins in a team.
    
    Args:
        team_id: The ID of the team (required).
    
    Returns:
        Dictionary containing a list of agents/admins in the specified team.
    """
    client = get_dixa_client()
    return client.get_team_agents(team_id=team_id)

