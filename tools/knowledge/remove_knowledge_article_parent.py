"""Tool for removing a knowledge article parent through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def remove_knowledge_article_parent(article_id: str) -> Dict[str, Any]:
    """Remove an article's parent association without deleting either entity.

    Discover ``article_id`` in a collection catalog and fetch the article first
    to verify its current parent. The article remains in Dixa but has no parent
    category after this operation. Use ``move_knowledge_article`` instead when
    replacing the current parent with another category.

    ⚠️ WARNING: This modifies data in the Dixa organization.
    The AI assistant MUST obtain explicit confirmation of the article and
    parent association to remove before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.

    Returns:
        ``{"success": True}`` when Dixa confirms removal with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.delete_knowledge_article_parent(article_id=article_id)
