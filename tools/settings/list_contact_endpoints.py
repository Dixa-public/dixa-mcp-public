"""
Tool for getting (listing) contact endpoints from the Dixa API.

Contact endpoints are configuration settings that define how the organization
receives contacts (e.g., phone numbers, email addresses).
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def list_contact_endpoints(
    _type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get (list) all available contact endpoints in an organization.
    
    Args:
        _type: Filter by endpoint type (e.g., "TelephonyEndpoint", "EmailEndpoint") (optional).
    
    Returns:
        Dictionary containing a list of contact endpoints with the following structure:
        {
            "data": [
                {
                    "number": "...",
                    "functionality": [...],
                    "name": "...",
                    "_type": "TelephonyEndpoint"
                },
                {
                    "address": "...",
                    "senderOverride": "...",
                    "name": "...",
                    "_type": "EmailEndpoint"
                },
                ...
            ]
        }
    """
    client = get_dixa_client()
    return client.get_contact_endpoints(_type=_type)

