"""
Tool for updating the follow-up status of a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def set_conversation_followup_status(
    conversation_id: str,
    follow_up: bool
) -> Dict[str, Any]:
    """
    Update the follow-up status of a conversation.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will update the follow-up status of a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation to update (required).
        follow_up: The follow-up status to set (True for follow-up, False otherwise) (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation follow-up status updated successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_conversation_followup(
        conversation_id=conversation_id,
        follow_up=follow_up
    )

