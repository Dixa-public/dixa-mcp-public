"""Tool for publishing every translation of a knowledge article through Dixa.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def publish_knowledge_article(article_id: str) -> Dict[str, Any]:
    """Publish a new version of every translation for Knowledge search.

    Discover ``article_id`` in a collection catalog and call
    ``fetch_knowledge_article_translations`` first. This is a bulk action over
    all languages, not just one draft. This bulk action is required when the
    article has ``preRelease=true`` and is multilingual. Otherwise, use
    ``publish_knowledge_article_translation`` when only one language should be
    published.

    ⚠️ WARNING: This changes externally visible data in the Dixa organization.
    The AI assistant MUST obtain explicit confirmation that every translation
    should be published before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.

    Returns:
        ``{"success": True}`` when Dixa confirms publication with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.publish_knowledge_article(article_id=article_id)
