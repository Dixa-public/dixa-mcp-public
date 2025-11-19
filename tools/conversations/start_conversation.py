"""
Tool for creating a conversation from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional, List, Literal
from tools.base import get_dixa_client

# Accepted conversation types
ConversationType = Literal["Callback", "Chat", "ContactForm", "Email", "Sms"]

# Accepted message types
MessageType = Literal["Inbound", "Outbound"]


async def start_conversation(
    requester_id: str,
    conversation_type: ConversationType,
    message_content: str,
    message_type: MessageType,
    subject: Optional[str] = None,
    email_integration_id: Optional[str] = None,
    language: Optional[str] = None,
    agent_id: Optional[str] = None,
    attachments: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create a conversation. For inbound messages the author is assumed to be the requester of the conversation (end user). 
    For outbound messages the author is specified using the agentId field.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create a conversation in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get requester_id: Use `list_end_users` to find an existing end user, or `add_end_user` if they don't exist yet.
    - To get agent_id (for outbound messages): Use `list_agents` to find the agent ID.
    
    Channel-specific requirements:
    - Email: email_integration_id is typically required (format: <email-address>@email.dixa.io)
    - Sms: Only Outbound messages are supported (message_type must be "Outbound")
    - Chat, ContactForm, Callback: Standard requirements apply
    
    Args:
        requester_id: The ID of the requester (end user) (required).
        conversation_type: The type of conversation. Accepted values: "Callback", "Chat", "ContactForm", "Email", "Sms" (required).
        message_content: The content of the message (required).
        message_type: The type of message. Accepted values: "Inbound", "Outbound" (required).
                      Note: Sms only supports "Outbound" messages.
        subject: The subject of the conversation (optional, commonly used for Email conversations).
        email_integration_id: The email integration ID (required for Email type conversations).
                             Format: <email-address>@email.dixa.io (optional).
        language: The language code (e.g., "en") (optional).
        agent_id: The ID of the agent (required for outbound messages) (optional).
        attachments: List of attachment objects with structure: [{"url": "...", "prettyName": "..."}] (optional).
    
    Returns:
        Dictionary containing the created conversation with the following structure:
        {
            "data": {
                "id": 100
            }
        }
    """
    client = get_dixa_client()
    return client.create_conversation(
        requester_id=requester_id,
        conversation_type=conversation_type,
        message_content=message_content,
        message_type=message_type,
        subject=subject,
        email_integration_id=email_integration_id,
        language=language,
        agent_id=agent_id,
        attachments=attachments
    )

