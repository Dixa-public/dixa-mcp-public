"""Fetch one bounded page of analytics records."""
from typing import Any, Dict, List, Optional, Union
from tools.base import get_dixa_client
from tools.analytics.period_filter import normalize_period_filter
from tools.input_schemas import decode_json
from tools.pagination import PageLimit


async def fetch_unaggregated_data(
    record_id: str,
    timezone: str,
    period_filter: Optional[Union[Dict[str, Any], str]] = None,
    csid_filter: Optional[Union[List[int], str]] = None,
    filters: Optional[Union[List[Dict[str, Any]], str]] = None,
    page_key: Optional[str] = None,
    page_limit: PageLimit = 50,
) -> Dict[str, Any]:
    """Get one page of individual analytics records, default 50, maximum 100.

    First prepare_analytics_metric_query and fetch_aggregated_data for summary
    questions. If row-level evidence is needed, call prepare_analytics_record_query
    without record_id to discover IDs, then with the selected ID to inspect
    fields and filter metadata. Never guess record IDs or filter values.

    Supply record_id, timezone, and either period_filter, csid_filter, or filters.
    Period filters take precedence over csid_filter, matching aggregated queries.
    JSON-encoded structured arguments are accepted. Period intervals may use
    shorthand dates; they are normalized to typed ISO timestamps.

    Fetch further pages only when necessary, using the returned pagination cursor
    unchanged as page_key. Retain record_id, timezone, and filters on every page.
    This tool never loops over pages or silently truncates returned data. Report
    whether your answer covers one page or the complete requested dataset.
    """
    if not isinstance(page_limit, int) or isinstance(page_limit, bool) or not 1 <= page_limit <= 100:
        raise ValueError("page_limit must be between 1 and 100")
    period_filter = decode_json(period_filter)
    csid_filter = decode_json(csid_filter)
    filters = decode_json(filters)
    if filters is not None:
        if not isinstance(filters, list) or any(
            not isinstance(item, dict) or not isinstance(item.get("attribute"), str)
            or not isinstance(item.get("values"), list) or not item["values"]
            or any(not isinstance(value, str) for value in item["values"])
            for item in filters
        ):
            raise ValueError("filters must contain attribute and non-empty string values arrays")
    request: Dict[str, Any] = {"id": record_id, "timezone": timezone}
    if period_filter is not None:
        if not isinstance(period_filter, dict):
            raise ValueError("period_filter must be an object")
        request["periodFilter"] = normalize_period_filter(period_filter)
    elif csid_filter is not None:
        if not isinstance(csid_filter, list) or not csid_filter or any(
            not isinstance(item, int) or isinstance(item, bool) for item in csid_filter
        ):
            raise ValueError("csid_filter must be a non-empty integer array")
        request["csidFilter"] = csid_filter
    elif not filters:
        raise ValueError("Provide period_filter, csid_filter, or non-empty filters, including on subsequent pages")
    request["filters"] = filters if filters is not None else []
    return get_dixa_client().post_analytics_metric_records_data(
        request=request, page_key=page_key, page_limit=page_limit,
    )
