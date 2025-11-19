"""
Tool for creating a knowledge category from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def add_knowledge_category(
    name: str,
    parent_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a knowledge category.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create a knowledge category in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        name: The name of the category (required).
        parent_id: The ID of the parent category (optional).
    
    Returns:
        Dictionary containing the created knowledge category.
    """
    client = get_dixa_client()
    return client.create_knowledge_category(
        name=name,
        parent_id=parent_id
    )

