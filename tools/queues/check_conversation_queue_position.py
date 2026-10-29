"""Get a conversation's approximate position in its current queue."""
from typing import Any, Dict
from tools.base import get_dixa_client

async def check_conversation_queue_position(conversation_id: int) -> Dict[str, Any]:
    """Get the current queue position; no queue ID is required.

    First search_conversations or fetch_conversation_by_id to identify
    the conversation and verify its queued state.
    """
    return get_dixa_client().get_queue_conversation_position(conversation_id=conversation_id)
