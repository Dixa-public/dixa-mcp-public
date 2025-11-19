"""
Tool for patching (updating) end user custom attributes from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def update_end_user_custom_attributes(
    user_id: str,
    custom_attributes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Patch (update) custom attributes for an end user.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will update custom attributes of an end user in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get user_id: Use `list_end_users` to find the end user ID first.
    - To get custom_attributes: Use `list_custom_attributes` to get the list of custom attribute definitions and their IDs. The custom_attributes parameter requires a dictionary mapping custom attribute IDs (UUIDs) to values. Filter the results to only include attributes with entityType "Contact" (which represents end users).
    
    Args:
        user_id: The ID of the end user to update custom attributes for (required).
        custom_attributes: Dictionary mapping custom attribute IDs to their values (required).
                         Format: Map[UUID, Option[AttributeValue]]
                         - For Text type custom attributes: string value
                         - For Select type custom attributes: array of strings (String[])
                         Example: {
                             "2f5515b6-7e98-4f4d-9010-bfd2a27d4f35": "012345",
                             "e14708a6-eed9-495c-9d88-c72331e9e247": ["str1", "str2"]
                         }
    
    Returns:
        Dictionary containing the patched end user attributes with the following structure:
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
    return client.patch_end_user_custom_attributes(
        user_id=user_id,
        custom_attributes=custom_attributes
    )

