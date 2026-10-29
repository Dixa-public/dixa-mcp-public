"""Fully update agents in bulk."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import AgentUpdateList


async def update_agents_bulk(agents: AgentUpdateList) -> Dict[str, Any]:
    """Fully update agents in bulk. Each item requires id and displayName. Fetch each current
    agent before building complete replacements; omitted optional values may be cleared. The
    API accepts a raw array. Inspect every result for individual failures.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.update_agents_bulk(agents=agents)
