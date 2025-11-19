"""
Tool for reopening a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def reopen_conversation(
    conversation_id: str
) -> Dict[str, Any]:
    """
    Reopen a conversation by providing its ID.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will reopen a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation to reopen (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation reopened successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_conversation_reopen(
        conversation_id=conversation_id
    )

