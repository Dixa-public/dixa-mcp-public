"""Discover record queries without expanding every filter value set."""
from typing import Any, Dict, Optional
from tools.base import get_dixa_client
from tools.pagination import PageLimit


async def prepare_analytics_record_query(
    record_id: Optional[str] = None,
    page_key: Optional[str] = None,
    page_limit: PageLimit = 50,
) -> Dict[str, Any]:
    """Discover record IDs, then inspect a selected record's fields and filters.

    For summary questions first use prepare_analytics_metric_query and
    fetch_aggregated_data. Without record_id, return one page of the record
    catalogue. Pass any pagination cursor unchanged as page_key when another
    page is needed. With record_id, return the complete Dixa record description
    including fields and filter metadata; this does not fetch records or expand
    all filter-value catalogues. Use fetch_analytics_filter_values for a selected
    filter attribute before constructing fetch_unaggregated_data arguments.
    """
    if not isinstance(page_limit, int) or isinstance(page_limit, bool) or not 1 <= page_limit <= 100:
        raise ValueError("page_limit must be between 1 and 100")
    client = get_dixa_client()
    if record_id is None:
        return client.get_analytics_records_catalogue(page_key=page_key, page_limit=page_limit)
    return client.get_analytics_record_description(record_id=record_id)
