"""Downgrade an agent or administrator to an end user."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def remove_agent(agent_id: str) -> Dict[str, Any]:
    """Downgrade an agent or administrator to an end user. This removes the agent role; it does
    not erase or anonymize the user. Confirm the exact user and loss of agent access.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.delete_agent(agent_id=agent_id)
