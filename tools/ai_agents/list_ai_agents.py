"""List native Mim agents and external chatbot integrations."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def list_ai_agents() -> Dict[str, Any]:
    """List native Mim agents and external chatbot integrations. No prerequisite tool is
    required.
    """
    client = get_dixa_client()
    return client.get_ai_agents()
