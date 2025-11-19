"""
Tool for adding agents to a team from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def add_agents_to_team(
    team_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Add agents/admins to a team.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will add agents to a team in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get team_id: Use `list_teams` to list all teams and find the team ID.
    - To get agent_ids: Use `list_agents` to find the agent/admin IDs.
    
    Args:
        team_id: The ID of the team (required).
        agent_ids: List of agent/admin IDs to add to the team (required).
    
    Returns:
        Dictionary containing the operation result.
    """
    client = get_dixa_client()
    return client.patch_team_add_agents(
        team_id=team_id,
        agent_ids=agent_ids
    )

