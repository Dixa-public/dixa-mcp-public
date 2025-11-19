"""
Tool for retrieving agent/admin information from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_agent_by_id(agent_id: str) -> Dict[str, Any]:
    """
    Get an agent/admin by ID from the Dixa API.
    
    Args:
        agent_id: The ID of the agent to retrieve.
    
    Returns:
        Dictionary containing agent information with the following structure:
        {
            "data": {
                "id": "...",
                "createdAt": "...",
                "displayName": "...",
                "email": "...",
                "avatarUrl": "...",
                "phoneNumber": "...",
                "additionalEmails": [...],
                "additionalPhoneNumbers": [...],
                "firstName": "...",
                "lastName": "...",
                "middleNames": [...],
                "roles": [...]
            }
        }
    """
    client = get_dixa_client()
    return client.get_agent(agent_id)

