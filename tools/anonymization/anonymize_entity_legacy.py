"""Deprecated anonymization endpoint."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import LegacyAnonymizationInput


async def anonymize_entity_legacy(request: LegacyAnonymizationInput) -> Dict[str, Any]:
    """Deprecated anonymization endpoint. Prefer anonymize_end_user, anonymize_conversation, or
    anonymize_conversation_message. request requires entityId; use _type User, Conversation,
    or Message. forceAnonymization closes an open conversation and must be separately
    explained and confirmed. This is irreversible. Preserve the returned request ID for
    fetch_anonymization_status.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.create_anonymization_legacy(request=request)
