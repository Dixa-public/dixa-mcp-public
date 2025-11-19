"""
Tool for getting (listing) conversations for an end user from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_end_user_conversations(
    user_id: str,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List conversations requested by a specific end user.
    
    Args:
        user_id: The ID of the end user (required).
        page_key: Base64 encoded form of pagination query parameters (optional).
        page_limit: Maximum number of results per page (optional).
    
    Returns:
        Dictionary containing the list of conversations for the end user.
    """
    client = get_dixa_client()
    return client.get_end_user_conversations(
        user_id=user_id,
        page_key=page_key,
        page_limit=page_limit
    )

