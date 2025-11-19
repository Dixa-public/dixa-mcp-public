"""
Tool for updating (full update) multiple end users in bulk from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, List
from tools.base import get_dixa_client


async def update_end_users_bulk(
    end_users: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update (full update) multiple end users in a single bulk action.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will update multiple end users in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        end_users: List of end user objects to update (required).
                  Each object should contain the user ID and all required fields.
    
    Returns:
        Dictionary containing the results of the bulk update operation.
    """
    client = get_dixa_client()
    return client.update_end_users_bulk(end_users=end_users)

