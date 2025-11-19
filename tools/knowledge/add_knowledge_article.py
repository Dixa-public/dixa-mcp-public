"""
Tool for creating a knowledge article from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def add_knowledge_article(
    title: str,
    content: str,
    category_id: Optional[str] = None,
    published: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Create a knowledge article.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create a knowledge article in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get category_id (optional): Use `list_knowledge_categories` to list all categories and find the category ID if you want to assign the article to a category.
    
    Args:
        title: The title of the article (required).
        content: The content of the article (required).
        category_id: The ID of the category to assign the article to (optional).
        published: Whether the article should be published (optional).
    
    Returns:
        Dictionary containing the created knowledge article.
    """
    client = get_dixa_client()
    return client.create_knowledge_article(
        title=title,
        content=content,
        category_id=category_id,
        published=published
    )

