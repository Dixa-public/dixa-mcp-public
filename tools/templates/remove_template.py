"""Permanently delete a template."""

from typing import Any, Dict
from tools.base import get_dixa_client


async def remove_template(template_id: str) -> Dict[str, Any]:
    """Permanently delete a template. First list_templates to identify the exact template and
    inspect its content. Confirm it is not used by flows or automations; the API has no
    complete template-usage lookup, so ask the user to verify unresolved usage. This
    operation is irreversible.

    WARNING: This modifies Dixa data. The AI assistant MUST obtain explicit user
    confirmation for the exact target and final changes before executing this tool.
    """
    client = get_dixa_client()
    return client.delete_template(template_id=template_id)
