"""Tool for deleting a knowledge article through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict

from tools.base import get_dixa_client


async def remove_knowledge_article(article_id: str) -> Dict[str, Any]:
    """Permanently delete an entire knowledge article.

    Discover ``article_id`` in a collection catalog and inspect the article and
    all translations first. This removes the article rather than merely
    removing its published translations from search; use
    ``unpublish_knowledge_article`` when the content should be retained.

    ⚠️ WARNING: This deletes the article and its language/version data from the
    Dixa organization and is typically irreversible. The AI assistant MUST
    obtain explicit confirmation of the exact article before executing it.

    Args:
        article_id: Article ID discovered in a collection catalog.

    Returns:
        ``{"success": True}`` when Dixa confirms deletion with an empty 204
        response; otherwise the unchanged Dixa response.
    """
    client = get_dixa_client()
    return client.delete_knowledge_article(article_id=article_id)
