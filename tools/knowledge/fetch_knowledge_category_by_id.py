"""Tool for fetching a knowledge category by ID from the Dixa API."""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client


async def fetch_knowledge_category_by_id(
    category_id: str,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch details and a localized title for one knowledge category.

    Obtain ``category_id`` from ``fetch_knowledge_collection_catalog``; Dixa
    v1 does not provide a global category list or category-creation endpoint.
    This is a read-only detail lookup. Use
    ``fetch_knowledge_category_translations`` to retrieve every translated
    title.

    Args:
        category_id: Category ID discovered in a collection catalog.
        language: Language code for the localized category title. Omit it to
            use the default language.

    Returns:
        The unchanged Dixa response. Its ``data`` contains the category ID,
        localized title, placement/default-location fields, lock state, and
        restrictions returned by Dixa.
    """
    client = get_dixa_client()
    return client.get_knowledge_category(
        category_id=category_id,
        language=language,
    )
