"""
Tool for getting a tag by ID from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_tag_by_id(tag_id: str) -> Dict[str, Any]:
    """
    Get a tag by ID.
    
    Args:
        tag_id: The ID of the tag to retrieve (required).
    
    Returns:
        Dictionary containing the tag information.
    """
    client = get_dixa_client()
    return client.get_tag(tag_id=tag_id)

