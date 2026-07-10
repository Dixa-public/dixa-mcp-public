"""Tool for fetching knowledge category translations from the Dixa API."""

from typing import Any, Dict

from tools.base import get_dixa_client


async def fetch_knowledge_category_translations(category_id: str) -> Dict[str, Any]:
    """Fetch every translated title for one knowledge category.

    Obtain ``category_id`` from ``fetch_knowledge_collection_catalog``. Use
    this read-only tool when all available category languages are needed; it
    does not return the category's child articles or categories, which belong
    to the collection catalog.

    Args:
        category_id: Category ID discovered in a collection catalog.

    Returns:
        The unchanged Dixa response. Its ``data.titles`` contains translated
        title entries with ``languageId`` and ``title``.
    """
    client = get_dixa_client()
    return client.get_knowledge_category_translations(category_id=category_id)
