"""
Tool for removing agents from a team from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def remove_agents_from_team(
    team_id: str,
    agent_ids: List[str]
) -> Dict[str, Any]:
    """
    Remove agents/admins from a team.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will remove agents from a team in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get team_id: Use `list_teams` to list all teams and find the team ID.
    - To get agent_ids: Use `list_team_agents` to see current team members, or use `list_agents` to find agent IDs.
    
    Args:
        team_id: The ID of the team (required).
        agent_ids: List of agent/admin IDs to remove from the team (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Agents removed from team successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.delete_team_remove_agents(
        team_id=team_id,
        agent_ids=agent_ids
    )

