"""Deprecated singular rating endpoint."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def list_conversation_ratings_legacy(conversation_id: int) -> Dict[str, Any]:
    """Deprecated singular rating endpoint. Prefer list_conversation_ratings. Use only when a
    caller explicitly needs legacy compatibility.
    """
    client = get_dixa_client()
    return client.get_conversation_rating_legacy(conversation_id=conversation_id)
