"""List one page of templates, optionally filtered by template_type."""

from typing import Any, Dict, Literal, Optional
from tools.base import get_dixa_client
from tools.pagination import PageLimit


async def list_templates(template_type: Optional[Literal["EmailAutoReply", "QuickResponse"]] = None, page_key: Optional[str] = None, page_limit: PageLimit = 50) -> Dict[str, Any]:
    """List one page of templates, optionally filtered by template_type. No prerequisite tool
    is required. Preserve pagination cursors unchanged. Use returned template IDs for
    remove_template; inspect content and translations before choosing a template.
    """
    client = get_dixa_client()
    return client.get_templates(template_type=template_type, page_key=page_key, page_limit=page_limit)
