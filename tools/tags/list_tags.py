"""
Tool for listing tags from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_tags(include_deactivated: Optional[bool] = None) -> Dict[str, Any]:
    """
    List all tags in an organization. Only active tags are returned by default.
    To include deactivated tags use include_deactivated=True.
    
    Args:
        include_deactivated: Whether to include deactivated tags in the response.
                           If not provided, only active tags are listed (default: False).
    
    Returns:
        Dictionary containing the list of all tags in an organization.
    """
    client = get_dixa_client()
    return client.get_tags(include_deactivated=include_deactivated)

