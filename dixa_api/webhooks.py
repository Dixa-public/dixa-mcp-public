"""Webhook subscription API methods with credential-safe responses."""
from typing import Any, Dict
from dixa_api.http import api_request
from dixa_api.safety import redact_webhook_diagnostics


def redact_webhook_credentials(value):
    """Hide response signing secrets/headers and request-form credentials.

    Dixa returns ``secretKey`` and ``headers`` on subscriptions; create/update
    inputs instead use ``authorization`` and ``customHeaders``. Preserve
    metadata and header names, without changing the original response or input.
    """
    if isinstance(value, list):
        return [redact_webhook_credentials(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key == "secretKey":
            result[key] = None if item is None else "[REDACTED]"
        elif key in ("authorization", "customHeaders", "headers"):
            if isinstance(item, dict):
                result[key] = {
                    name: content if key == "authorization" and name == "_type" else "[REDACTED]"
                    for name, content in item.items()
                }
            else:
                # Do not expose credentials if an upstream field changes shape.
                result[key] = None if item is None else "[REDACTED]"
        else:
            result[key] = redact_webhook_credentials(item)
    return result


def get_webhooks(
    self,
) -> Dict[str, Any]:
    """Call GET /webhooks."""
    result = api_request(
        self,
        'GET',
        '/webhooks',
    )
    return redact_webhook_credentials(result)


def get_webhook(
    self,
    webhook_id: str,
) -> Dict[str, Any]:
    """Call GET /webhooks/{webhook_id}."""
    result = api_request(
        self,
        'GET',
        f'/webhooks/{webhook_id}',
    )
    return redact_webhook_credentials(result)


def create_webhook(
    self,
    subscription: Dict[str, Any],
) -> Dict[str, Any]:
    """Call POST /webhooks."""
    result = api_request(
        self,
        'POST',
        '/webhooks',
        payload=subscription,
    )
    return redact_webhook_credentials(result)


def patch_webhook(
    self,
    webhook_id: str,
    changes: Dict[str, Any],
) -> Dict[str, Any]:
    """Call PATCH /webhooks/{webhook_id}."""
    result = api_request(
        self,
        'PATCH',
        f'/webhooks/{webhook_id}',
        payload=changes,
    )
    return redact_webhook_credentials(result)


def delete_webhook(
    self,
    webhook_id: str,
) -> Dict[str, Any]:
    """Call DELETE /webhooks/{webhook_id}."""
    return api_request(
        self,
        'DELETE',
        f'/webhooks/{webhook_id}',
    )


def get_webhook_delivery_status(
    self,
    webhook_id: str,
) -> Dict[str, Any]:
    """Call GET /webhooks/{webhook_id}/delivery-status."""
    result = api_request(
        self,
        'GET',
        f'/webhooks/{webhook_id}/delivery-status',
    )
    return redact_webhook_diagnostics(redact_webhook_credentials(result))


def get_webhook_event_logs(
    self,
    webhook_id: str,
    event: str,
) -> Dict[str, Any]:
    """Call GET /webhooks/{webhook_id}/delivery-status/logs/{event}."""
    result = api_request(
        self,
        'GET',
        f'/webhooks/{webhook_id}/delivery-status/logs/{event}',
    )
    return redact_webhook_diagnostics(redact_webhook_credentials(result))
