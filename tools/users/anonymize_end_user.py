"""
Tool for requesting end user anonymization from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def anonymize_end_user(
    user_id: str,
    force: bool = False
) -> Dict[str, Any]:
    """
    Request the anonymization of an end user. This can be done for data protection purposes required by GDPR.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will anonymize an end user in your Dixa organization.
    This action is typically irreversible and is used for GDPR compliance. The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        user_id: The ID of the end user to anonymize (required).
        force: Whether to force anonymization (default: False) (optional).
    
    Returns:
        Dictionary containing the anonymization request details.
    """
    client = get_dixa_client()
    return client.patch_end_user_anonymize(
        user_id=user_id,
        force=force
    )

