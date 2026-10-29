"""Patch a webhook subscription."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import WebhookPatchInput


async def modify_webhook_subscription(webhook_id: str, changes: WebhookPatchInput) -> Dict[str, Any]:
    """Patch a webhook subscription. Omitted fields stay unchanged; explicit False, empty lists
    and objects are intentional. Fetch the current subscription before editing; do not
    resend redacted credentials. Changes to URL, events, filters or enabled can alter future
    external deliveries, so show the final destination and delivery configuration and obtain
    separate explicit approval. Returned credential/header values are redacted.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.patch_webhook(webhook_id=webhook_id, changes=changes)
