"""Dixa templates API methods."""
from typing import Any, Dict, List, Optional
from dixa_api.http import api_request


def get_templates(
    self,
    template_type: Optional[str] = None,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Call GET /templates."""
    return api_request(
        self,
        'GET',
        '/templates',
        params={'type': template_type, 'pageKey': page_key, 'pageLimit': page_limit},
    )


def delete_template(
    self,
    template_id: str,
) -> Dict[str, Any]:
    """Call DELETE /templates/{template_id}."""
    return api_request(
        self,
        'DELETE',
        f'/templates/{template_id}',
    )
