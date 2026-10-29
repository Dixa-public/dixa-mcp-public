"""Deprecated text-search endpoint."""

from typing import Any, Dict, Optional
from typing_extensions import Annotated
from pydantic import Field
from tools.base import get_dixa_client
from tools.pagination import PageLimit


async def search_conversations_legacy(query: Annotated[str, Field(min_length=1)], exact_match: Optional[bool] = None, page_key: Optional[str] = None, page_limit: PageLimit = 50) -> Dict[str, Any]:
    """Deprecated text-search endpoint. Prefer search_conversations, which supports structured
    filters. query is non-empty text. exact_match is optional. Return one page; pass the
    response cursor unchanged as page_key and retain the query. Use only for legacy
    compatibility.
    """
    client = get_dixa_client()
    return client.get_search_conversations_legacy(query=query, exact_match=exact_match, page_key=page_key, page_limit=page_limit)
