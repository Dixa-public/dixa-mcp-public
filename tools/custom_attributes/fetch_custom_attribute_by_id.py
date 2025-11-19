"""
Tool for getting a custom attribute definition by ID from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_custom_attribute_by_id(
    custom_attribute_id: str
) -> Dict[str, Any]:
    """
    Get custom attribute definition by ID.
    
    Args:
        custom_attribute_id: The ID of the custom attribute to retrieve (required).
    
    Returns:
        Dictionary containing the custom attribute definition with the following structure:
        {
            "data": {
                "id": "...",
                "entityType": "Conversation" | "Contact",
                "identifier": "...",
                "label": "...",
                "inputDefinition": {...},
                "description": "...",
                "createdAt": "...",
                "isRequired": true/false,
                "isArchived": true/false,
                "isDeactivated": true/false
            }
        }
    """
    client = get_dixa_client()
    return client.get_custom_attribute(custom_attribute_id=custom_attribute_id)

