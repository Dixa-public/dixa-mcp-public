"""
Tool for getting (listing) all custom attribute definitions from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_custom_attributes() -> Dict[str, Any]:
    """
    List all custom attributes definitions in an organization.
    
    Returns:
        Dictionary containing the list of custom attribute definitions with the following structure:
        {
            "data": [
                {
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
            ]
        }
    """
    client = get_dixa_client()
    return client.get_custom_attributes()

