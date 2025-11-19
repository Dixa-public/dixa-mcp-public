"""
Tool for updating (full update) an agent/admin in the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional, List
from tools.base import get_dixa_client


async def update_agent_full(
    agent_id: str,
    display_name: str,
    phone_number: Optional[str] = None,
    additional_emails: Optional[List[str]] = None,
    additional_phone_numbers: Optional[List[str]] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[List[str]] = None,
    avatar_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update (full update) an agent/admin in the organization using PUT.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will update an existing agent in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Note: This is a PUT endpoint for full updates. For partial updates, use patch_agent instead.
    
    Args:
        agent_id: The ID of the agent to update (required).
        display_name: Display name for the agent (required).
        phone_number: Primary phone number (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: First name of the agent (optional).
        last_name: Last name of the agent (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL for the agent's avatar image (optional).
    
    Returns:
        Dictionary containing the updated agent information with the following structure:
        {
            "data": {
                "id": "...",
                "createdAt": "...",
                "displayName": "...",
                "email": "...",
                "avatarUrl": "...",
                "phoneNumber": "...",
                "additionalEmails": [...],
                "additionalPhoneNumbers": [...],
                "firstName": "...",
                "lastName": "...",
                "middleNames": [...],
                "roles": [...]
            }
        }
    """
    client = get_dixa_client()
    return client.update_agent(
        agent_id=agent_id,
        display_name=display_name,
        phone_number=phone_number,
        additional_emails=additional_emails,
        additional_phone_numbers=additional_phone_numbers,
        first_name=first_name,
        last_name=last_name,
        middle_names=middle_names,
        avatar_url=avatar_url
    )

