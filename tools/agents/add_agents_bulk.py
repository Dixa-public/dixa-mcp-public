"""Create agents in bulk."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import AgentCreateList


async def add_agents_bulk(agents: AgentCreateList) -> Dict[str, Any]:
    """Create agents in bulk. Each agent requires displayName and email. Optional contact/name
    arrays are preserved. The API uses a data envelope for creation. Inspect every result
    for individual failures.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.create_agents_bulk(agents=agents)
