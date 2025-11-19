"""
Tool for updating a knowledge article from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def modify_knowledge_article(
    article_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    category_id: Optional[str] = None,
    published: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update a knowledge article (partial update).
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will update a knowledge article in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get article_id: Use `list_knowledge_articles` to list all articles and find the article ID.
    - To get category_id (optional): Use `list_knowledge_categories` to list all categories and find the category ID if you want to change the article's category.
    
    Args:
        article_id: The ID of the article to update (required).
        title: The title of the article (optional).
        content: The content of the article (optional).
        category_id: The ID of the category to assign the article to (optional).
        published: Whether the article should be published (optional).
    
    Returns:
        Dictionary containing the updated knowledge article.
    """
    client = get_dixa_client()
    return client.patch_knowledge_article(
        article_id=article_id,
        title=title,
        content=content,
        category_id=category_id,
        published=published
    )

