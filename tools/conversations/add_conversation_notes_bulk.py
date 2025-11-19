"""
Tool for creating internal notes in bulk for a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def add_conversation_notes_bulk(
    conversation_id: str,
    notes: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create internal notes in bulk for a conversation by providing the conversation ID.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create multiple notes in a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation to add notes to (required).
        notes: List of note objects to create. Each note should be a dictionary with:
            - message (required): The note message content
            - agentId (optional): The ID of the agent creating the note
            - createdAt (optional): ISO 8601 timestamp for when the note was created (e.g., "2021-12-01T12:46:36.581Z[GMT]")
    
    Returns:
        Dictionary containing the results of the bulk operation with the following structure:
        {
            "data": [
                {
                    "data": {
                        "id": "...",
                        "authorId": "...",
                        "createdAt": "...",
                        "csid": 9456,
                        "message": "..."
                    },
                    "_type": "BulkActionSuccess"
                },
                {
                    "error": {
                        "message": "..."
                    },
                    "_type": "BulkActionFailure"
                }
            ]
        }
        
        Note: The response includes both successful and failed note creations. Check the "_type" field
        to determine if each note was created successfully ("BulkActionSuccess") or failed ("BulkActionFailure").
    """
    client = get_dixa_client()
    return client.create_conversation_notes_bulk(
        conversation_id=conversation_id,
        notes=notes
    )

