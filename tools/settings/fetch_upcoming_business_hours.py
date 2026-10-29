"""Get resolved business hours for the next 1-90 days, default 7."""

from typing import Any, Dict
from typing_extensions import Annotated
from pydantic import Field
from tools.base import get_dixa_client


async def fetch_upcoming_business_hours(schedule_id: str, days: Annotated[int, Field(ge=1, le=90)] = 7) -> Dict[str, Any]:
    """Get resolved business hours for the next 1-90 days, default 7. First
    list_business_hours_schedules for schedule_id. Open entries mean open only inside their
    listed intervals; outside intervals and on Closed entries the business is closed. Days
    without configured hours are omitted, so an empty list does not mean always open.
    """
    client = get_dixa_client()
    return client.get_business_hours_upcoming(schedule_id=schedule_id, days=days)
