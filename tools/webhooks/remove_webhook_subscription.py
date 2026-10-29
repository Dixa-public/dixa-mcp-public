"""Delete a webhook subscription and stop its future event deliveries."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def remove_webhook_subscription(webhook_id: str) -> Dict[str, Any]:
    """Delete a webhook subscription and stop its future event deliveries. First list and fetch
    the subscription to verify its ID, URL and events; confirm the exact subscription and
    delivery impact.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.delete_webhook(webhook_id=webhook_id)
