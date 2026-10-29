"""Partially update agents in bulk."""

from typing import Any, Dict
from tools.base import get_dixa_client
from tools.input_schemas import AgentPatchList


async def modify_agents_bulk(agents: AgentPatchList) -> Dict[str, Any]:
    """Partially update agents in bulk. Each item requires id. Omit fields to preserve them;
    explicit empty arrays are sent unchanged. The API accepts a raw array. Inspect every
    result for individual failures.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.patch_agents_bulk(agents=agents)
