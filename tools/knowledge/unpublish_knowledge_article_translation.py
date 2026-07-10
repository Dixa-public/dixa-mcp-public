"""Tool for unpublishing a knowledge article translation through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def unpublish_knowledge_article_translation(
    article_id: str,
    language_id: str,
) -> Dict[str, Any]:
    """Mark one article translation as unpublished and remove it from search.

    Discover ``article_id`` in a collection catalog, then call
    ``fetch_knowledge_article_translations`` to confirm the selected published
    ``language_id``. This retains the translation data; use
    ``remove_knowledge_article_translation`` only when every draft and
    published version of that language should be deleted.

    ⚠️ WARNING: This changes externally visible data in the Dixa organization.
    The AI assistant MUST obtain explicit confirmation of the article and
    language to remove from search before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.
        language_id: ISO language code confirmed from the article translation
            response.

    Returns:
        ``{"success": True}`` when Dixa confirms the change with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.unpublish_knowledge_article_translation(
        article_id=article_id,
        language_id=language_id,
    )
