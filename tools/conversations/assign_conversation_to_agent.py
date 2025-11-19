"""
Tool for claiming a conversation for an agent from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def assign_conversation_to_agent(
    conversation_id: str,
    agent_id: str,
    force: bool = False
) -> Dict[str, Any]:
    """
    Claim a conversation for a given agent. To avoid taking over assigned conversations, set the force parameter to false.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will assign a conversation to an agent in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Prerequisites:
    - To get conversation_id: Use `fetch_conversation_by_id` or `search_conversations` to find the conversation ID first.
    - To get agent_id: Use `list_agents` to find the agent ID.
    
    Args:
        conversation_id: The ID of the conversation to claim (required).
        agent_id: The ID of the agent to claim the conversation for (required).
        force: Whether to force claiming even if the conversation is already assigned (default: False) (optional).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Conversation claimed successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.update_conversation_claim(
        conversation_id=conversation_id,
        agent_id=agent_id,
        force=force
    )

