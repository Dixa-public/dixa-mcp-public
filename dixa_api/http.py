"""Shared JSON transport for the additional Dixa v1 endpoints."""
from typing import Any, Dict, Optional
import requests
from requests.exceptions import HTTPError, RequestException


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
    except HTTPError as exc:
        # Upstream error bodies can echo webhook credentials or message content.
        status = exc.response.status_code if exc.response is not None else "unknown"
        raise HTTPError(f"Dixa API returned HTTP {status}", response=exc.response) from None
    except RequestException:
        raise RequestException("Dixa API request failed; the outcome may be unknown. Do not automatically retry a mutation.") from None
    if response.status_code == 204:
        return {"success": True}
    return response.json()
