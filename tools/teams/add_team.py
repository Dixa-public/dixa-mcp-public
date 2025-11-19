"""
Tool for creating a team from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def add_team(name: str) -> Dict[str, Any]:
    """
    Create a team.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create a team in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        name: The name of the team (required).
    
    Returns:
        Dictionary containing the created team.
    """
    client = get_dixa_client()
    return client.create_team(name=name)

