"""Tool for moving a knowledge article through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def move_knowledge_article(
    article_id: str,
    parent_id: str,
) -> Dict[str, Any]:
    """Replace an article's current parent with a destination category.

    Discover both IDs with ``list_knowledge_collections`` and
    ``fetch_knowledge_collection_catalog``, then fetch the article to verify its
    current placement. This sets ``parent_id`` as the new parent; it does not add
    a second parent. Use ``remove_knowledge_article_parent`` when the article
    should have no parent category.

    ⚠️ WARNING: This modifies data in the Dixa organization.
    The AI assistant MUST obtain explicit confirmation of the article and exact
    destination category before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.
        parent_id: Destination category ID discovered in a collection catalog.

    Returns:
        ``{"success": True}`` when Dixa confirms the move with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.move_knowledge_article(
        article_id=article_id,
        parent_id=parent_id,
    )
