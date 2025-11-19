"""
Tool for requesting message anonymization from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def anonymize_conversation_message(
    conversation_id: str,
    message_id: str
) -> Dict[str, Any]:
    """
    Request the anonymization of a single message in a conversation.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will anonymize a message in a conversation in your Dixa organization.
    This action is typically irreversible and is used for GDPR compliance. The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation containing the message (required).
        message_id: The ID of the message to anonymize (required).
    
    Returns:
        Dictionary containing the anonymization request details with the following structure:
        {
            "data": {
                "id": "...",
                "entityType": "MessageAnonymizationType",
                "_type": "Message",
                "initiatedAt": "...",
                "targetEntityId": "...",
                "requestedBy": "..."
            }
        }
    """
    client = get_dixa_client()
    return client.patch_conversation_message_anonymize(
        conversation_id=conversation_id,
        message_id=message_id
    )

