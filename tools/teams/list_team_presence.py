"""
Tool for listing team presence status from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_team_presence(
    team_id: str,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the presence status of all agents/admins in a team.
    
    Args:
        team_id: The ID of the team (required).
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.
    
    Returns:
        Dictionary containing the list of agents/admins presence status in the specified team.
    """
    client = get_dixa_client()
    return client.get_team_presence(
        team_id=team_id,
        page_key=page_key,
        page_limit=page_limit
    )

