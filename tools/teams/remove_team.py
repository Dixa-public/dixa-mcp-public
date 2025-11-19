"""
Tool for deleting a team from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def remove_team(team_id: str) -> Dict[str, Any]:
    """
    Delete a team.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will delete a team from your Dixa organization.
    This action is typically irreversible. The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        team_id: The ID of the team to delete (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Team deleted successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.delete_team(team_id=team_id)

