"""Get a business-hours schedule definition, including timezone, recurring rules and exceptions."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def fetch_business_hours_definition(schedule_id: str) -> Dict[str, Any]:
    """Get a business-hours schedule definition, including timezone, recurring rules and
    exceptions. Obtain schedule_id with list_business_hours_schedules.
    """
    client = get_dixa_client()
    return client.get_business_hours_definition(schedule_id=schedule_id)
