"""
Tool for getting an end user by ID from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_end_user_by_id(
    user_id: str
) -> Dict[str, Any]:
    """
    Get an end user by ID.
    
    Args:
        user_id: The ID of the end user to retrieve (required).
    
    Returns:
        Dictionary containing the end user details.
    """
    client = get_dixa_client()
    return client.get_end_user(user_id=user_id)

