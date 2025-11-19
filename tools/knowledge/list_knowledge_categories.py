"""
Tool for listing knowledge categories from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_knowledge_categories(
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all knowledge categories.
    
    Args:
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.
    
    Returns:
        Dictionary containing the list of knowledge categories.
    """
    client = get_dixa_client()
    return client.get_knowledge_categories(
        page_key=page_key,
        page_limit=page_limit
    )

