"""
Tool for requesting conversation anonymization from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def anonymize_conversation(
    conversation_id: str,
    force: bool = False
) -> Dict[str, Any]:
    """
    Request the anonymization of a conversation. This can be done for data protection purposes required by GDPR.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will anonymize a conversation in your Dixa organization.
    This action is typically irreversible and is used for GDPR compliance. The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        conversation_id: The ID of the conversation to anonymize (required).
        force: Whether to force anonymization (default: False) (optional).
    
    Returns:
        Dictionary containing the anonymization request details with the following structure:
        {
            "data": {
                "id": "...",
                "entityType": "ConversationAnonymizationType",
                "_type": "Conversation",
                "initiatedAt": "...",
                "targetEntityId": "...",
                "requestedBy": "..."
            }
        }
    """
    client = get_dixa_client()
    return client.patch_conversation_anonymize(
        conversation_id=conversation_id,
        force=force
    )

