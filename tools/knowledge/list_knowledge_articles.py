"""
Tool for listing knowledge articles from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_knowledge_articles(
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all knowledge articles.
    
    Args:
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.
    
    Returns:
        Dictionary containing the list of knowledge articles.
    """
    client = get_dixa_client()
    return client.get_knowledge_articles(
        page_key=page_key,
        page_limit=page_limit
    )

