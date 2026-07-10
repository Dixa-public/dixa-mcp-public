"""Tool for updating knowledge article translations through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client
from tools.knowledge.schemas import KnowledgeTranslationList


async def modify_knowledge_article_translations(
    article_id: str,
    translations: Optional[KnowledgeTranslationList] = None,
) -> Dict[str, Any]:
    """Create or update draft translations without publishing them for search.

    Discover ``article_id`` in a collection catalog and call
    ``fetch_knowledge_article_translations`` first to inspect existing draft and
    published versions. Each supplied language is upserted independently, so
    this operation can partially succeed.

    ⚠️ WARNING: This modifies data in the Dixa organization.
    The AI assistant MUST obtain explicit user confirmation for the exact
    languages, titles, and content before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.
        translations: Draft translations to create or update. Each item
            requires ISO ``languageId`` and ``title`` and may include HTML
            ``content``. Omit the argument to send no ``translations`` field;
            an explicit empty list and explicit empty strings are sent as
            intentional values.

    Returns:
        The unchanged Dixa response. ``data`` contains successfully upserted
        translations and ``partialErrors`` contains per-language failures.
        Always inspect and report both; the presence of successful ``data``
        does not mean every requested translation succeeded.

    Notes:
        Draft updates do not make content searchable. After verifying the
        update result, fetch the article metadata and all translations. Dixa
        requires ``publish_knowledge_article`` for a multilingual article with
        ``preRelease=true``; otherwise
        ``publish_knowledge_article_translation`` can publish one language.
    """
    client = get_dixa_client()
    return client.patch_knowledge_article_translations(
        article_id=article_id,
        translations=translations,
    )
