"""
Tool for listing agents/admins from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_agents(
    email: Optional[str] = None,
    phone: Optional[str] = None,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get (list) all agents/admins in an organization.
    
    It is possible to filter by one of the mutually exclusive parameters: email or phone number.
    In case both are provided, an error is returned.
    
    Args:
        email: Filter by email address (mutually exclusive with phone).
        phone: Filter by phone number (mutually exclusive with email).
        page_key: Pagination key for retrieving next page of results.
        page_limit: Maximum number of results per page.
    
    Returns:
        Dictionary containing a list of agents with the following structure:
        {
            "data": [
                {
                    "id": "...",
                    "createdAt": "...",
                    "displayName": "...",
                    "email": "...",
                    "avatarUrl": "...",
                    "additionalEmails": [...],
                    "additionalPhoneNumbers": [...],
                    "middleNames": [...],
                    "roles": [...]
                },
                ...
            ]
        }
    """
    client = get_dixa_client()
    return client.get_agents(
        email=email,
        phone=phone,
        page_key=page_key,
        page_limit=page_limit
    )

