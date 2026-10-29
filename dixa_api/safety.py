"""Safe API errors and diagnostic output; never inspect or log credential values."""
import re
from typing import Any, NoReturn

from requests.exceptions import HTTPError, RequestException


REDACTED = "[REDACTED]"
ITEM_ERROR_MESSAGE = "Dixa reported an item failure; diagnostic details were withheld."
REQUEST_ERROR_MESSAGE = (
    "Dixa API request failed; the outcome may be unknown. "
    "Do not automatically retry a mutation."
)
ERROR_TYPES = frozenset({
    "EmptyPatchSet", "ErrorResponse", "Infrastructure", "Integrity",
    "InvalidArgument", "NotFound", "Validation",
})
_LANGUAGE_ID = re.compile(r"[a-z]{2,3}(?:-[A-Za-z0-9]{2,8}){0,3}\Z")
_RESOURCE_ID = re.compile(r"(?:[0-9]{1,20}|[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})\Z")


def raise_api_error(error: RequestException) -> NoReturn:
    """Raise only trusted metadata, without an attached request/response or cause."""
    if isinstance(error, HTTPError):
        status = getattr(getattr(error, "response", None), "status_code", None)
        status = status if type(status) is int and 100 <= status <= 599 else "unknown"
        raise HTTPError(f"Dixa API returned HTTP {status}") from None
    raise RequestException(REQUEST_ERROR_MESSAGE) from None


def _item_error(value: Any) -> Any:
    if value is None:
        return None
    result = {"message": ITEM_ERROR_MESSAGE}
    if isinstance(value, dict):
        # Arbitrary codes, IDs, messages and extra properties can themselves echo secrets.
        if isinstance(value.get("_type"), str) and value["_type"] in ERROR_TYPES:
            result["_type"] = value["_type"]
        identifier = value.get("id")
        if isinstance(identifier, str) and _RESOURCE_ID.fullmatch(identifier):
            result["id"] = identifier
        language = value.get("languageId")
        if isinstance(language, str) and _LANGUAGE_ID.fullmatch(language):
            result["languageId"] = language
        for name in ("code", "status", "statusCode"):
            code = value.get(name)
            if type(code) is int and 100 <= code <= 599:
                result[name] = code
    return result


def _partial_errors(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, list):
        return [_item_error(item) for item in value]
    # Preserve a visible failure even when the upstream diagnostic changes shape.
    return [_item_error(value)]


def sanitize_diagnostics(value: Any) -> Any:
    """Sanitize API-envelope diagnostics without traversing customer content.

    Dixa returns bulk failures in data[].error, and partialErrors at the root or
    under data. Successful records, pagination and failure item order are retained.
    """
    if not isinstance(value, dict):
        return value
    result = dict(value)
    if "partialErrors" in result:
        result["partialErrors"] = _partial_errors(result["partialErrors"])
    data = result.get("data")
    if isinstance(data, list):
        result["data"] = [
            {**item, "error": _item_error(item["error"])}
            if isinstance(item, dict) and "error" in item else item
            for item in data
        ]
    elif isinstance(data, dict) and "partialErrors" in data:
        result["data"] = {**data, "partialErrors": _partial_errors(data["partialErrors"])}
    return result


def decode_response(response: Any) -> Any:
    """Decode JSON without exposing a malformed response in exceptions."""
    try:
        value = response.json()
    except ValueError:
        raise RequestException(REQUEST_ERROR_MESSAGE) from None
    return sanitize_diagnostics(value)


def redact_webhook_diagnostics(value: Any) -> Any:
    """Withhold raw downstream bodies and event payloads, retaining status metadata."""
    if isinstance(value, list):
        return [redact_webhook_diagnostics(item) for item in value]
    if not isinstance(value, dict):
        return value
    return {
        key: (None if item is None else REDACTED)
        if key in {"responseText", "payload"}
        else redact_webhook_diagnostics(item)
        for key, item in value.items()
    }
