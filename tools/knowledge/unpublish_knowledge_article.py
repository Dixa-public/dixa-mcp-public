"""Tool for unpublishing every translation of a knowledge article through Dixa.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def unpublish_knowledge_article(article_id: str) -> Dict[str, Any]:
    """Remove every translation of an article from Knowledge search.

    Discover ``article_id`` in a collection catalog and call
    ``fetch_knowledge_article_translations`` first to confirm the full set of
    published languages. This retains the article and translation data; it is
    not deletion. Use ``unpublish_knowledge_article_translation`` when only one
    language should be removed from search.

    ⚠️ WARNING: This changes externally visible data in the Dixa organization.
    The AI assistant MUST obtain explicit confirmation that every translation
    should be removed from search before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.

    Returns:
        ``{"success": True}`` when Dixa confirms the change with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.unpublish_knowledge_article(article_id=article_id)
