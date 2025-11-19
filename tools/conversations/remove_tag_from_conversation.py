"""
Tool for untagging a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def remove_tag_from_conversation(
    conversation_id: str,
    tag_id: str
) -> Dict[str, Any]:
    """
    Untag a conversation. You may remove active or inactive tags from a conversation.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will remove a tag from a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get tag_id: Use `list_conversation_tags` to see tags on a conversation, or use `list_tags` to find the tag ID.
    - To get conversation_id: Use `fetch_conversation_by_id` or `search_conversations` to find the conversation ID first.
    
    Args:
        conversation_id: The ID of the conversation to untag (required).
        tag_id: The ID of the tag to remove (required). Both active and inactive tags can be removed.
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation untagged successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.delete_conversation_tag(
        conversation_id=conversation_id,
        tag_id=tag_id
    )

