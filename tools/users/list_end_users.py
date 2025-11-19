"""
Tool for getting (listing) all end users from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_end_users(
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all end users in an organization.
    
    Args:
        page_key: Base64 encoded form of pagination query parameters (optional).
        page_limit: Maximum number of results per page (optional).
    
    Returns:
        Dictionary containing the list of end users.
    """
    client = get_dixa_client()
    return client.get_end_users(
        page_key=page_key,
        page_limit=page_limit
    )

