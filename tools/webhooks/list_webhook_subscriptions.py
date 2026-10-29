"""List webhook subscriptions."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def list_webhook_subscriptions() -> Dict[str, Any]:
    """List webhook subscriptions. No prerequisite tool is required. Use returned subscription
    IDs for detail, update, delete, and delivery tools. Credential and custom-header values
    are redacted.
    """
    client = get_dixa_client()
    return client.get_webhooks()
