"""Tool for deleting a knowledge article translation through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def remove_knowledge_article_translation(
    article_id: str,
    language_id: str,
) -> Dict[str, Any]:
    """Permanently delete every version of one article language.

    Discover ``article_id`` in a collection catalog and use
    ``fetch_knowledge_article_translations`` to confirm the ``language_id`` and
    its draft/published versions. This deletes both draft and published
    versions; it is not an unpublish operation. Use
    ``unpublish_knowledge_article_translation`` when the language should only
    be removed from search.

    ⚠️ WARNING: This deletes all versions of the selected translation and is
    typically irreversible. The AI assistant MUST obtain explicit confirmation
    of the article and language before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.
        language_id: ISO language code confirmed from the article translation
            response.

    Returns:
        ``{"success": True}`` when Dixa confirms deletion with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.delete_knowledge_article_translation(
        article_id=article_id,
        language_id=language_id,
    )
