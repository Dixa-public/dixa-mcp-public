"""Get the status of an anonymization request."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def fetch_anonymization_status(request_id: str) -> Dict[str, Any]:
    """Get the status of an anonymization request. request_id is returned by an anonymization
    operation, not the user or conversation ID. Reuse the existing request ID; do not
    resubmit anonymization to check progress.
    """
    client = get_dixa_client()
    return client.get_anonymization_status(request_id=request_id)
