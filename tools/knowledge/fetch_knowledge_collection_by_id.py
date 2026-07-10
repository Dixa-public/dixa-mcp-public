"""Tool for fetching a knowledge collection by ID from the Dixa API."""

from typing import Any, Dict

from tools.base import get_dixa_client


async def fetch_knowledge_collection_by_id(collection_id: str) -> Dict[str, Any]:
    """Fetch metadata for one knowledge collection, not its catalog tree.

    Obtain ``collection_id`` from ``list_knowledge_collections``. Use this
    read-only tool for collection details; use
    ``fetch_knowledge_collection_catalog`` when category or article IDs are
    needed.

    Args:
        collection_id: Collection ID returned by Knowledge collection
            discovery.

    Returns:
        The unchanged Dixa response. Its ``data`` contains the collection ID,
        title, optional description, internal-KB setting, and restrictions.
    """
    client = get_dixa_client()
    return client.get_knowledge_collection(collection_id=collection_id)
