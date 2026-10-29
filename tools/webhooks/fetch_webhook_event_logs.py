"""Get recent delivery logs for one subscribed event."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def fetch_webhook_event_logs(webhook_id: str, event: str) -> Dict[str, Any]:
    """Get recent delivery logs for one subscribed event. First fetch_webhook_subscription to
    obtain an exact event name, then fetch_webhook_delivery_status to identify the affected
    event. event uses names such as ConversationNoteAdded, not display labels. Logs may
    include customer payloads; retrieve only the needed event.
    """
    client = get_dixa_client()
    return client.get_webhook_event_logs(webhook_id=webhook_id, event=event)
