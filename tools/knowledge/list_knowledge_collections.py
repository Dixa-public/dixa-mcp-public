"""Tool for listing knowledge collections from the Dixa API."""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client


async def list_knowledge_collections(
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Discover the organization's top-level knowledge collections.

    Start Knowledge discovery with this read-only tool. Dixa v1 has no global
    article or category list: select a collection from this response, then call
    ``fetch_knowledge_collection_catalog`` to discover its category and article
    IDs.

    Args:
        page_key: Opaque continuation key from a previous Dixa response. Omit
            it for the first page, and pass a returned value through unchanged;
            never construct or modify it.
        page_limit: Maximum collections to request for this page. Omit it to
            use Dixa's default page size.

    Returns:
        The unchanged Dixa response. Its ``data`` contains collection records,
        including IDs and collection metadata such as titles, descriptions,
        settings, and restrictions. If Dixa supplies another page key, pass it
        unchanged in a follow-up call.
    """
    client = get_dixa_client()
    return client.get_knowledge_collections(
        page_key=page_key,
        page_limit=page_limit,
    )
