"""
Tool for creating multiple end users in bulk from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def add_end_users_bulk(
    end_users: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create multiple end users in a single bulk action.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create multiple end users in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        end_users: List of end user objects to create (required).
                  Each object should contain the same fields as create_end_user:
                  - displayName (required)
                  - email (optional)
                  - phoneNumber (optional)
                  - additionalEmails (optional)
                  - additionalPhoneNumbers (optional)
                  - firstName (optional)
                  - lastName (optional)
                  - middleNames (optional)
                  - avatarUrl (optional)
                  - externalId (optional)
    
    Returns:
        Dictionary containing the results of the bulk creation operation.
    """
    client = get_dixa_client()
    return client.create_end_users_bulk(end_users=end_users)

