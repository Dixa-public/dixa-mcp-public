"""
Tool for bulk tagging conversations from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def tag_conversation_bulk(
    conversation_id: str,
    tag_names: List[str]
) -> Dict[str, Any]:
    """
    Initiate bulk tag of a conversation and process it asynchronously. 
    If a tag with corresponding name does not exist it will be created.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will add tags to a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation to tag (required).
        tag_names: List of tag names to add to the conversation (required).
    
    Returns:
        Dictionary containing the bulk tagging operation details.
    """
    client = get_dixa_client()
    return client.create_conversation_tags_bulk(
        conversation_id=conversation_id,
        tag_names=tag_names
    )

