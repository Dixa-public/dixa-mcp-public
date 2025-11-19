"""
Tool for deleting a knowledge article from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client


async def remove_knowledge_article(
    article_id: str
) -> Dict[str, Any]:
    """
    Delete a knowledge article.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will delete a knowledge article from your Dixa organization.
    This action is typically irreversible. The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        article_id: The ID of the article to delete (required).
    
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Knowledge article deleted successfully"}.
        On error, returns the error response.
    """
    client = get_dixa_client()
    return client.delete_knowledge_article(article_id=article_id)

