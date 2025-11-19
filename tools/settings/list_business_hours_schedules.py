"""
Tool for listing business hours schedules from the Dixa API.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def list_business_hours_schedules() -> Dict[str, Any]:
    """
    Get (list) business hours schedules in an organization with pagination.
    
    Returns:
        Dictionary containing a list of schedules with the following structure:
        {
            "data": {
                "schedules": [
                    {
                        "name": "...",
                        "id": "..."
                    },
                    ...
                ]
            }
        }
    """
    client = get_dixa_client()
    return client.get_business_hours_schedules()

