"""Tool for updating a knowledge article through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client
from tools.knowledge.schemas import KnowledgeTagUpdateInput


async def modify_knowledge_article(
    article_id: str,
    owned_by: Optional[str] = None,
    tags: Optional[KnowledgeTagUpdateInput] = None,
    pre_release: Optional[bool] = None,
) -> Dict[str, Any]:
    """Partially update article ownership, tags, or pre-release metadata.

    Discover ``article_id`` in a collection catalog and fetch the current
    article before preparing this patch. This tool does not change translation
    titles/content, parent placement, or publication/search visibility.

    ⚠️ WARNING: This modifies data in the Dixa organization.
    The AI assistant MUST obtain explicit user confirmation for the exact
    metadata changes before executing this tool.

    Args:
        article_id: Article ID discovered in a collection catalog.
        owned_by: Dixa user ID that should own the article.
        tags: Tag changes shaped as ``{"add": [...], "remove": [...]}``.
            Tag IDs can be discovered with the tag tools. Explicit empty lists
            are preserved.
        pre_release: ``True`` to make the article pre-release only or ``False``
            to explicitly disable that setting.

    Returns:
        The unchanged Dixa response. Its ``data`` contains the updated article
        metadata and current draft/published translation state.

    Notes:
        Omitted optional arguments are not sent and therefore remain unchanged;
        explicit ``False`` and empty lists are intentional values. Use
        ``modify_knowledge_article_translations`` for title/content changes,
        movement tools for parent changes, and publication tools for visibility.
    """
    client = get_dixa_client()
    return client.patch_knowledge_article(
        article_id=article_id,
        owned_by=owned_by,
        tags=tags,
        pre_release=pre_release,
    )
