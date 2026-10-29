"""Create a rating offer for a conversation."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import RatingOfferInput


async def create_conversation_rating_offer(conversation_id: int, offer: RatingOfferInput) -> Dict[str, Any]:
    """Create a rating offer for a conversation. offer requires userId, agentId, and ratingType
    (Csat, Nps, ThumbsUpOrDown), with optional offeredAt. Use the actual conversation
    requester and participating agent; a different agent can skew metrics. Preserve the
    returned rating ID for submit_conversation_rating_result.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.create_conversation_rating_offer(conversation_id=conversation_id, offer=offer)
