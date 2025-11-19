"""
Tool for linking a conversation to a parent conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def link_conversation_to_parent(
    conversation_id: str,
    parent_conversation_id: str
) -> Dict[str, Any]:
    """
    Link a conversation to a parent conversation.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will link a conversation to a parent conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get conversation_id: Use `fetch_conversation_by_id` or `search_conversations` to find the conversation ID first.
    - To get parent_conversation_id: Use `fetch_conversation_by_id` or `search_conversations` to find the parent conversation ID first.
    
    Args:
        conversation_id: The ID of the conversation to link (required).
        parent_conversation_id: The ID of the parent conversation to link to (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation linked successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_conversation_link(
        conversation_id=conversation_id,
        parent_conversation_id=parent_conversation_id
    )

