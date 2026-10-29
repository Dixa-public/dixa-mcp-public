"""Fetch one page of valid analytics filter values."""
from typing import Any, Dict, Optional
from tools.base import get_dixa_client
from tools.pagination import PageLimit

async def fetch_analytics_filter_values(
    filter_attribute: str, page_key: Optional[str] = None, page_limit: PageLimit = 50,
) -> Dict[str, Any]:
    """Get one page of values for an analytics filter attribute.

    First prepare_analytics_metric_query or prepare_analytics_record_query with
    the selected metric/record ID. Use an attribute returned in that metadata;
    never guess its name. Preserve pagination cursors unchanged for later pages.
    The returned values can be used by fetch_aggregated_data or fetch_unaggregated_data.
    """
    return get_dixa_client().get_analytics_filter_values(
        filter_attribute=filter_attribute, page_key=page_key, page_limit=page_limit,
    )
