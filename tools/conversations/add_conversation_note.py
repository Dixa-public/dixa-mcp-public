"""
Tool for creating an internal note in a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def add_conversation_note(
    conversation_id: str,
    message: str,
    agent_id: Optional[str] = None,
    created_at: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an internal note in a conversation by providing the conversation ID.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create a note in a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation to add a note to (required).
        message: The note message content (required).
        agent_id: The ID of the agent creating the note (optional).
        created_at: ISO 8601 timestamp for when the note was created (e.g., "2021-12-01T12:46:36.581Z[GMT]") (optional).
    
    Returns:
        Dictionary containing the created note with the following structure:
        {
            "data": {
                "id": "...",
                "authorId": "...",
                "createdAt": "...",
                "csid": 9456,
                "message": "..."
            }
        }
    """
    client = get_dixa_client()
    return client.create_conversation_note(
        conversation_id=conversation_id,
        message=message,
        agent_id=agent_id,
        created_at=created_at
    )

