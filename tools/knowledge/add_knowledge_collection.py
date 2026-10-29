"""Create a knowledge collection."""

from typing import Any, Dict, Optional
from tools.base import get_dixa_client


async def add_knowledge_collection(title: str, description: Optional[str] = None, internal_kb_enabled: Optional[bool] = None) -> Dict[str, Any]:
    """Create a knowledge collection. First list_knowledge_collections to avoid duplicates.
    title is required. Optional description and internal_kb_enabled are omitted when None;
    False is sent unchanged. Dixa defaults internalKbEnabled to true. Use the returned
    collection ID as parent_id in add_knowledge_category.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.create_knowledge_collection(title=title, description=description, internal_kb_enabled=internal_kb_enabled)
