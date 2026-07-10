"""Tool for fetching a knowledge collection catalog from the Dixa API."""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client


async def fetch_knowledge_collection_catalog(
    collection_id: str,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Discover all category and article IDs in a collection catalog.

    First obtain ``collection_id`` with ``list_knowledge_collections``. This
    read-only tool replaces the removed global article/category listing tools
    and returns the nested hierarchy, including root-level articles. Use the
    dedicated article translation tool when every draft and published version
    is needed.

    Args:
        collection_id: Collection ID returned by collection discovery.
        language: Language code for localized catalog titles. Omit it to use
            the collection's default language.

    Returns:
        The unchanged Dixa response. Its ``data`` is the nested collection
        catalog with category and article IDs and titles in the selected
        language.
    """
    client = get_dixa_client()
    return client.get_knowledge_collection_catalog(
        collection_id=collection_id,
        language=language,
    )
