"""
Tool for getting a contact endpoint by ID from the Dixa API.

Contact endpoints are configuration settings that define how the organization
receives contacts (e.g., phone numbers, email addresses).
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def fetch_contact_endpoint_by_id(
    contact_endpoint_id: str
) -> Dict[str, Any]:
    """
    Get a contact endpoint by ID (email or phone number).
    
    Args:
        contact_endpoint_id: The ID of the contact endpoint to retrieve (required).
    
    Returns:
        Dictionary containing the contact endpoint details with the following structure:
        {
            "data": {
                "address": "...",  # For EmailEndpoint
                "senderOverride": "...",  # For EmailEndpoint
                "name": "...",
                "_type": "EmailEndpoint"
            }
        }
        OR
        {
            "data": {
                "number": "...",  # For TelephonyEndpoint
                "functionality": [...],
                "name": "...",
                "_type": "TelephonyEndpoint"
            }
        }
    """
    client = get_dixa_client()
    return client.get_contact_endpoint(contact_endpoint_id=contact_endpoint_id)

