"""Get the latest delivery statuses for a webhook subscription."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def fetch_webhook_delivery_status(webhook_id: str) -> Dict[str, Any]:
    """Get the latest delivery statuses for a webhook subscription. First
    list_webhook_subscriptions and fetch_webhook_subscription to verify the destination. Use
    fetch_webhook_event_logs for a specific event after inspecting status.
    Response bodies are withheld; timestamps, status codes and success flags remain available.
    """
    client = get_dixa_client()
    return client.get_webhook_delivery_status(webhook_id=webhook_id)
