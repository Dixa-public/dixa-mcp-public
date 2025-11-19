"""
Tool for tagging a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def tag_conversation(
    conversation_id: str,
    tag_id: str
) -> Dict[str, Any]:
    """
    Tag a conversation. You may only use active tags to tag conversations.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will tag a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get tag_id: Use `list_tags` to list all tags and find the tag ID by name, or use `add_tag` if the tag doesn't exist yet.
    - To get conversation_id: Use `fetch_conversation_by_id` or `search_conversations` to find the conversation ID first.
    
    Args:
        conversation_id: The ID of the conversation to tag (required).
        tag_id: The ID of the tag to apply (required). Only active tags can be used.
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation tagged successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_conversation_tag(
        conversation_id=conversation_id,
        tag_id=tag_id
    )

