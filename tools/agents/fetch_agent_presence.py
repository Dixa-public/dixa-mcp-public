"""Get one agent or administrator's presence."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def fetch_agent_presence(agent_id: str) -> Dict[str, Any]:
    """Get one agent or administrator's presence. Obtain agent_id with list_agents or
    fetch_agent_by_id.
    """
    client = get_dixa_client()
    return client.get_agent_presence(agent_id=agent_id)
