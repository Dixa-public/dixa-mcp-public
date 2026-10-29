"""Discover organization-wide conversation flows."""
from typing import Any, Dict, Optional
from tools.base import get_dixa_client

async def list_conversation_flows(channel: Optional[str] = None) -> Dict[str, Any]:
    """List organization flows; no prerequisite or conversation ID is needed.

    channel optionally filters by WhatsApp, Voicemail, WidgetChat,
    FacebookMessenger, Email, ContactForm, Callback, PstnPhone, or Messenger.
    Dixa defaults to PstnPhone when omitted. Returned flow IDs identify the organization's configured flows.
    """
    return get_dixa_client().get_conversation_flows(channel=channel)
