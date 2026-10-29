"""Submit a result for an existing rating offer."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import RatingResultInput


async def submit_conversation_rating_result(conversation_id: int, rating_id: str, result: RatingResultInput) -> Dict[str, Any]:
    """Submit a result for an existing rating offer. rating_id must identify an offer for this
    conversation. result requires ratingResult {_type, value}; Csat is 1-5, Nps is 0-10,
    ThumbsUpOrDown is 0 or 1. Optional comment and submittedAt are preserved. userId is
    deprecated and may be omitted or null. Submit only the customer-provided rating; never
    invent a score.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.create_conversation_rating_result(conversation_id=conversation_id, rating_id=rating_id, result=result)
