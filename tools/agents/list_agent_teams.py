"""
Tool for retrieving teams for a specific agent/admin from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_agent_teams(agent_id: str) -> Dict[str, Any]:
    """
    List the teams in which the agent/admin is a member.
    
    Args:
        agent_id: The ID of the agent to get teams for.
    
    Returns:
        Dictionary containing a list of teams with the following structure:
        {
            "data": [
                {
                    "id": "..."
                },
                ...
            ]
        }
    """
    client = get_dixa_client()
    return client.get_agent_teams(agent_id)

