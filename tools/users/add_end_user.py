"""
Tool for creating an end user from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional, List
from tools.base import get_dixa_client


async def add_end_user(
    display_name: str,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    additional_emails: Optional[List[str]] = None,
    additional_phone_numbers: Optional[List[str]] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_names: Optional[List[str]] = None,
    avatar_url: Optional[str] = None,
    external_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an end user.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create an end user in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        display_name: The display name of the end user (required).
        email: The email address of the end user (optional).
        phone_number: The phone number of the end user (optional).
        additional_emails: List of additional email addresses (optional).
        additional_phone_numbers: List of additional phone numbers (optional).
        first_name: The first name of the end user (optional).
        last_name: The last name of the end user (optional).
        middle_names: List of middle names (optional).
        avatar_url: URL to the avatar image (optional).
        external_id: External identifier for the end user (optional).
    
    Returns:
        Dictionary containing the created end user.
    """
    client = get_dixa_client()
    return client.create_end_user(
        display_name=display_name,
        email=email,
        phone_number=phone_number,
        additional_emails=additional_emails,
        additional_phone_numbers=additional_phone_numbers,
        first_name=first_name,
        last_name=last_name,
        middle_names=middle_names,
        avatar_url=avatar_url,
        external_id=external_id
    )

