"""
Helpers for Analytics API periodFilter payloads.
"""

import re
from typing import Any, Dict


DATE_ONLY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_WITHOUT_TZ_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T.*(?<!Z)$")
TIMEZONE_SUFFIX_PATTERN = re.compile(r"(Z|[+-]\d{2}:?\d{2})$")


def normalize_period_filter(period_filter: Any) -> Any:
    """
    Normalize shorthand interval filters into the typed ISO 8601 shape the API expects.
    """
    if not isinstance(period_filter, dict):
        return period_filter

    normalized: Dict[str, Any] = dict(period_filter)
    if "start" in normalized and "end" in normalized:
        normalized.setdefault("_type", "Interval")
        normalized["start"] = normalize_timestamp(normalized["start"])
        normalized["end"] = normalize_timestamp(normalized["end"])

    return normalized


def normalize_timestamp(value: Any) -> Any:
    if not isinstance(value, str):
        return value

    if DATE_ONLY_PATTERN.match(value):
        return f"{value}T00:00:00Z"

    if DATETIME_WITHOUT_TZ_PATTERN.match(value) and not TIMEZONE_SUFFIX_PATTERN.search(value):
        return f"{value}Z"

    return value
