"""Shared JSON transport for the additional Dixa v1 endpoints."""
from typing import Any, Dict, Optional
import requests
from requests.exceptions import RequestException
from dixa_api.safety import decode_response, raise_api_error


def api_request(client, method: str, path: str, *, payload: Any = None,
                params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make one bounded request; never log bodies, headers, or credentials."""
    headers = dict(client.headers)
    kwargs: Dict[str, Any] = {"headers": headers, "timeout": 30}
    if payload is not None:
        headers["Content-Type"] = "application/json"
        kwargs["json"] = payload
    if params is not None:
        kwargs["params"] = {key: value for key, value in params.items() if value is not None}
    try:
        response = requests.request(method, f"{client.base_url}{path}", **kwargs)
        response.raise_for_status()
    except RequestException as exc:
        raise_api_error(exc)
    if response.status_code == 204:
        return {"success": True}
    return decode_response(response)
