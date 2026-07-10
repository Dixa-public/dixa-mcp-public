"""Tool for fetching a knowledge article by ID from the Dixa API."""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client


async def fetch_knowledge_article_by_id(
    article_id: str,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch article metadata and draft/published state in one language.

    Obtain ``article_id`` from ``fetch_knowledge_collection_catalog``. This is
    a direct, read-only lookup; successfully fetching an article does not mean
    its draft is published or searchable. Use
    ``fetch_knowledge_article_translations`` to inspect every language and
    version.

    Args:
        article_id: Article ID discovered in a collection catalog.
        language: Language code for the returned translation. Omit it to use
            the default language.

    Returns:
        The unchanged Dixa response. Its ``data`` contains article metadata,
        placement, ownership, tags, restrictions, and a ``translation`` with a
        draft and, when one exists, its published version.
    """
    client = get_dixa_client()
    return client.get_knowledge_article(article_id=article_id, language=language)
