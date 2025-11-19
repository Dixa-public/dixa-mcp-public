"""
Tool for deleting a tag from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def remove_tag(tag_id: str) -> Dict[str, Any]:
    """
    Delete a tag and all its associations. Note that this operation is irreversible.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will delete a tag from your Dixa organization.
    This action is irreversible and will delete all tag associations. The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get tag_id: Use `list_tags` to list all tags and find the tag ID.
    
    Args:
        tag_id: The ID of the tag to delete (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Tag deleted successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.delete_tag(tag_id=tag_id)

