"""Add an inbound or outbound message to a conversation."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import ConversationMessageInput


async def add_conversation_message(conversation_id: int, message: ConversationMessageInput) -> Dict[str, Any]:
    """Add an inbound or outbound message to a conversation. message requires _type (Inbound or
    Outbound) and content {_type: Text, Html, or Markdown, value: text}. Outbound also
    requires agentId. cc and bcc contain end-user IDs, not email addresses. Attachments
    contain url and optional prettyName. Inspect the conversation channel first: SMS is
    outbound only; WhatsApp is outbound and Markdown only, with at most one attachment
    (.jpg, .jpeg, .png, .pdf, .doc, .docx, .pptx, .xlsx). Outbound messages can be sent to
    customers. Show the final message, recipient, channel, cc/bcc, and attachment URLs and
    wait for separate explicit approval before executing.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.create_conversation_message(conversation_id=conversation_id, message=message)
