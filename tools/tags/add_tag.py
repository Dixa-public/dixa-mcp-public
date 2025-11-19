"""
Tool for creating a tag from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def add_tag(
    name: str,
    color: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a tag.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create a tag in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        name: The name of the tag (required).
        color: The color of the tag (e.g., "#000000") (optional).
    
    Returns:
        Dictionary containing the created tag or an existing tag with the same name.
        Note that the tag is not updated to match the input in case it already exists.
    """
    client = get_dixa_client()
    return client.create_tag(name=name, color=color)

