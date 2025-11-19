"""
Tool for getting a knowledge article by ID from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_knowledge_article_by_id(
    article_id: str
) -> Dict[str, Any]:
    """
    Get a knowledge article by ID.
    
    Args:
        article_id: The ID of the knowledge article to retrieve (required).
    
    Returns:
        Dictionary containing the knowledge article information.
    """
    client = get_dixa_client()
    return client.get_knowledge_article(article_id=article_id)

