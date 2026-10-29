"""Dixa anonymization API methods."""
from typing import Any, Dict, List, Optional
from dixa_api.http import api_request


def get_anonymization_status(
    self,
    request_id: str,
) -> Dict[str, Any]:
    """Call GET /anonymization/request/{request_id}."""
    return api_request(
        self,
        'GET',
        f'/anonymization/request/{request_id}',
    )


def create_anonymization_legacy(
    self,
    request: Dict[str, Any],
) -> Dict[str, Any]:
    """Call POST /anonymization."""
    return api_request(
        self,
        'POST',
        '/anonymization',
        payload=request,
    )
