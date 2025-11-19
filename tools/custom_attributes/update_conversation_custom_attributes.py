"""
Tool for patching (updating) conversation custom attributes from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def update_conversation_custom_attributes(
    conversation_id: str,
    custom_attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Patch (update) custom attributes for a conversation.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will update custom attributes of a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get conversation_id: Use `fetch_conversation_by_id` or `search_conversations` to find the conversation ID first.
    - To get custom_attributes: Use `list_custom_attributes` to get the list of custom attribute definitions and their IDs. The custom_attributes parameter requires a dictionary mapping custom attribute IDs (UUIDs) to values. Filter the results to only include attributes with entityType "Conversation".
    
    Args:
        conversation_id: The ID of the conversation to update custom attributes for (required).
        custom_attributes: Dictionary mapping custom attribute IDs to their values (required).
                          Format: Map[UUID, Option[AttributeValue]]
                          - For Text type custom attributes: string value
                          - For Select type custom attributes: array of strings (String[])
                          Example: {
                              "2f5515b6-7e98-4f4d-9010-bfd2a27d4f35": "012345",
                              "e14708a6-eed9-495c-9d88-c72331e9e247": ["str1", "str2"]
                          }
    
    Returns:
        Dictionary containing the patched conversation attributes with the following structure:
        {
            "data": [
                {
                    "id": "...",
                    "name": "...",
                    "identifier": "...",
                    "value": "..." or ["...", "..."]
                }
            ]
        }
    """
    client = get_dixa_client()
    return client.patch_conversation_custom_attributes(
        conversation_id=conversation_id,
        custom_attributes=custom_attributes
    )

