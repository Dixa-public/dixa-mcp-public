"""Create a webhook subscription that can send future events to an external URL."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import WebhookCreateInput


async def add_webhook_subscription(subscription: WebhookCreateInput) -> Dict[str, Any]:
    """Create a webhook subscription that can send future events to an external URL.
    subscription requires name, url, authorization, and customHeaders. authorization uses
    _type NoAuth, BasicAuth (username/password), or TokenAuth (value). Optional events,
    enabled, and filters are preserved. Show the destination URL, event selection, filters,
    enabled state, and header names; obtain explicit approval for future deliveries before
    executing. Keep credentials private. Returned credential/header values are redacted.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.create_webhook(subscription=subscription)
