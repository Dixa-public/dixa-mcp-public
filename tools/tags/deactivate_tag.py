"""
Tool for deactivating a tag from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def deactivate_tag(tag_id: str) -> Dict[str, Any]:
    """
    Deactivate a tag.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will deactivate a tag in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get tag_id: Use `list_tags` to list all tags and find the tag ID.
    
    Args:
        tag_id: The ID of the tag to deactivate (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Tag deactivated successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.patch_tag_deactivate(tag_id=tag_id)

