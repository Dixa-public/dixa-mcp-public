"""
Tool for checking business hours status from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def check_business_hours_status(
    schedule_id: str,
    timestamp: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get business hours status - check if a business is open either right now or at the specified timestamp.
    
    Args:
        schedule_id: The ID of the schedule to check (required).
        timestamp: ISO 8601 timestamp to check (e.g., "2019-08-24T14:15:22Z"). 
                  If not provided, checks current time (optional).
    
    Returns:
        Dictionary containing the business hours status with the following structure:
        {
            "data": {
                "isOpen": true/false,
                "timestamp": "2025-01-08T08:31:25Z"
            }
        }
    """
    client = get_dixa_client()
    return client.get_business_hours_status(
        schedule_id=schedule_id,
        timestamp=timestamp
    )

