"""
Tool for closing a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def close_conversation(
    conversation_id: str,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Mark a conversation as closed by providing its ID.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will close a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation to close (required).
        user_id: The ID of the user closing the conversation (optional).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation closed successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_conversation_close(
        conversation_id=conversation_id,
        user_id=user_id
    )

