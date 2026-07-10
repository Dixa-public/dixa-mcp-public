"""Tool for publishing a knowledge article translation through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def publish_knowledge_article_translation(
    article_id: str,
    language_id: str,
) -> Dict[str, Any]:
    """Publish one article translation for Knowledge search.

    Discover ``article_id`` in a collection catalog, then call both
    ``fetch_knowledge_article_by_id`` and
    ``fetch_knowledge_article_translations`` to confirm the article metadata,
    target ``language_id``, and intended draft. Dixa rejects single-translation
    publication when the article has ``preRelease=true`` and is multilingual;
    use ``publish_knowledge_article`` to publish all translations in that
    state. Never disable ``pre_release`` merely to bypass this rule: that is a
    separate metadata change requiring its own explanation and confirmation.

    ⚠️ WARNING: This changes externally visible data in the Dixa organization.
    The AI assistant MUST obtain explicit confirmation of the article,
    language, and draft to publish before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.
        language_id: ISO language code confirmed from the article translation
            response.

    Returns:
        ``{"success": True}`` when Dixa confirms publication with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.publish_knowledge_article_translation(
        article_id=article_id,
        language_id=language_id,
    )
