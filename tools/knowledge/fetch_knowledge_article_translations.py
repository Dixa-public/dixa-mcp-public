"""Tool for fetching knowledge article translations from the Dixa API."""

from typing import Any, Dict

from tools.base import get_dixa_client


async def fetch_knowledge_article_translations(article_id: str) -> Dict[str, Any]:
    """Inspect every draft and published translation for an article.

    Obtain ``article_id`` from ``fetch_knowledge_collection_catalog``. Call
    this read-only tool before editing, publishing, unpublishing, or deleting a
    language so the affected versions are explicit. A draft returned here is
    not searchable until it is published.

    Args:
        article_id: Article ID discovered in a collection catalog.

    Returns:
        The unchanged Dixa response. Its ``data.translations`` separates
        ``draft`` and ``published`` arrays and includes each translation's
        language, title, HTML/plaintext content, availability, and version
        metadata.
    """
    client = get_dixa_client()
    return client.get_knowledge_article_translations(article_id=article_id)
