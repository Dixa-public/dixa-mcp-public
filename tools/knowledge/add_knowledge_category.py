"""Tool for adding a knowledge category through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client
from tools.knowledge.schemas import KnowledgeCategoryTranslationList


async def add_knowledge_category(
    parent_id: str,
    translations: Optional[KnowledgeCategoryTranslationList] = None,
) -> Dict[str, Any]:
    """Add a knowledge category under a collection or another category.

    Every category belongs to a collection. Discover collection IDs with
    ``list_knowledge_collections`` and category IDs with
    ``fetch_knowledge_collection_catalog``. Requires ``knowledge.content:w``.

    ⚠️ WARNING: This creates data in the Dixa organization.
    The AI assistant MUST obtain explicit user confirmation for the parent
    collection or category and translated titles before executing it.

    Args:
        parent_id: Required parent ID. Use a collection ID to create a top-level
            category, or a category ID to create a subcategory.
        translations: Optional translated titles. Each item requires an ISO
            ``languageId`` and ``title``; category translations have no article
            content. Omit to send no translations field; an explicit empty
            list is preserved.

    Returns:
        The unchanged Dixa response. Its ``data`` contains the created category,
        including its ID, title, restrictions, and parent placement.
    """
    client = get_dixa_client()
    return client.create_knowledge_category(
        parent_id=parent_id,
        translations=translations,
    )
