"""
Tool for retrieving organization information from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_organization_details() -> Dict[str, Any]:
    """
    Fetch organization details from the Dixa API.
    
    The API key is automatically extracted from:
    - Authorization header (for remote HTTP/SSE servers)
    - Command-line arguments (for local subprocess servers)
    - DIXA_API_KEY environment variable (fallback)
    
    Returns:
        Dictionary containing organization information from Dixa.
    """
    client = get_dixa_client()
    return client.get_organization()

