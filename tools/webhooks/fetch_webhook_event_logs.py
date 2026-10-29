"""Get recent delivery logs for one subscribed event."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def fetch_webhook_event_logs(webhook_id: str, event: str) -> Dict[str, Any]:
    """Get recent delivery logs for one subscribed event. First fetch_webhook_subscription to
    obtain an exact event name, then fetch_webhook_delivery_status to identify the affected
    event. event uses names such as ConversationNoteAdded, not display labels. Raw event payloads and receiver response bodies are withheld to protect secrets.
    Delivery timestamps, status codes and success flags remain available. Retrieve only the needed event.
    """
    client = get_dixa_client()
    return client.get_webhook_event_logs(webhook_id=webhook_id, event=event)
