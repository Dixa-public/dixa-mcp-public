"""
Tool for updating the working channel status of an agent/admin in the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Literal
from tools.base import get_dixa_client

# Accepted channel values
ChannelType = Literal["Email", "InteractiveChat", "Messaging", "Speak"]


async def set_agent_working_channel(
    agent_id: str,
    channel: ChannelType,
    working: bool
) -> Dict[str, Any]:
    """
    Update the working channel status of an agent/admin.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will update an agent's working channel status in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        agent_id: The ID of the agent to update (required).
        channel: The channel name. Accepted values: "Email", "InteractiveChat", "Messaging", "Speak" (required).
        working: Whether the agent is working on this channel (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Agent working channel updated successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_agent_working_channel(
        agent_id=agent_id,
        channel=channel,
        working=working
    )

