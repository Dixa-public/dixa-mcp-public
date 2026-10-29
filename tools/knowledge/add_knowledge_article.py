"""Tool for adding a knowledge article through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Any, Dict, Optional

from tools.base import get_dixa_client
from tools.knowledge.schemas import KnowledgeTagIdList, KnowledgeTranslationList


async def add_knowledge_article(
    translations: Optional[KnowledgeTranslationList] = None,
    parent_id: Optional[str] = None,
    tags: Optional[KnowledgeTagIdList] = None,
    pre_release: Optional[bool] = None,
) -> Dict[str, Any]:
    """Add a draft knowledge article with optional placement and metadata.

    Discover a parent category with ``list_knowledge_collections`` followed by
    ``fetch_knowledge_collection_catalog`` when the article should be nested
    or ``pre_release=True``. Pre-release creation requires a parent category;
    never disable pre-release merely to bypass a missing parent.
    Supply titles and HTML bodies inside ``translations``; there are no
    top-level ``title`` or ``content`` fields. Creation does not publish the
    draft for search.

    ⚠️ WARNING: This creates data in the Dixa organization.
    The AI assistant MUST obtain explicit user confirmation for the
    translations, parent, tags, and pre-release setting before executing it.

    Args:
        translations: Initial draft translations. Each item requires the ISO
            ``languageId`` and ``title`` and may include HTML ``content``.
            Omit the argument to send no translations; an explicit empty list
            is sent unchanged. Attachment content should reference public URLs
            returned by ``upload_knowledge_article_attachments``.
        parent_id: Parent category ID discovered in a collection catalog.
            Required when ``pre_release=True``; otherwise optional. Use the
            movement tools to change placement later.
        tags: Tag IDs to assign. Omit or pass an empty list for no tags. Empty
            lists are omitted from the API request because Dixa rejects them.
        pre_release: ``True`` to make the article pre-release only or ``False``
            to explicitly disable that setting. Omit it to use Dixa's default.

    Returns:
        The unchanged Dixa response. Its ``data`` contains the created article
        ID, metadata, placement, and draft/published translation state.

    Notes:
        Inspect the created article metadata and translations before publishing.
        When ``pre_release=True`` and the article is multilingual, Dixa requires
        ``publish_knowledge_article`` to publish all translations together;
        otherwise a translation publication tool can publish one language.
    """
    client = get_dixa_client()
    return client.create_knowledge_article(
        translations=translations,
        parent_id=parent_id,
        tags=tags,
        pre_release=pre_release,
    )
