"""Dixa ai agents API methods."""
from typing import Any, Dict, List, Optional
from dixa_api.http import api_request


def get_ai_agents(
    self,
) -> Dict[str, Any]:
    """Call GET /ai-agents."""
    return api_request(
        self,
        'GET',
        '/ai-agents',
    )
