"""Get a webhook subscription."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def fetch_webhook_subscription(webhook_id: str) -> Dict[str, Any]:
    """Get a webhook subscription. First list_webhook_subscriptions for webhook_id. Inspect
    URL, events, enabled state, and filters before editing. Credential and custom-header
    values are redacted; never reuse [REDACTED] as a credential.
    """
    client = get_dixa_client()
    return client.get_webhook(webhook_id=webhook_id)
