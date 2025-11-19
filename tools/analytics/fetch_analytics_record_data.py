"""
Tool for getting metric records data (unaggregated) from the Dixa Analytics API.
"""

import json
from typing import Dict, Any, Optional, List, Union
from tools.base import get_dixa_client


async def fetch_analytics_record_data(
    record_id: str,
    timezone: str,
    period_filter: Optional[Union[Dict[str, Any], str]] = None,
    csid_filter: Optional[Union[List[int], str]] = None,
    filters: Optional[Union[List[Dict[str, Any]], str]] = None,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get unaggregated metric record data from the Dixa Analytics API.
    
    This tool fetches individual (unaggregated) records for a specific metric. Use this when you need
    detailed, row-level data rather than summary statistics. Each record represents a single data point
    (e.g., an individual conversation, rating, or event).
    
    ⚠️ REQUIRED PREREQUISITES - You MUST call these tools FIRST to build a valid payload:
    
    SIMPLIFIED APPROACH (RECOMMENDED):
    1. Call `prepare_analytics_record_query` without record_id to discover available record IDs (e.g., "ratings", "closed_conversations")
    2. Call `prepare_analytics_record_query` with your chosen record_id - this single call returns:
       - Available filter attributes with all their valid values
       - Field metadata for the records
       - All information needed to build a valid payload
    
    Without calling these prerequisite tools first, you cannot build a valid payload for this tool.
    
    IMPORTANT - Filter Selection (Discriminated Union):
    The API uses a discriminated union pattern. You can use:
    - period_filter (RECOMMENDED): For time-based queries. When used, csidFilter is NOT included, but filters IS REQUIRED.
    - csid_filter: For specific conversation IDs. When used, periodFilter is NOT included, and filters is optional.
    - filters only: Can be used alone without period_filter or csid_filter.
    
    These combinations are mutually exclusive in the request:
    - period_filter + filters (required) → csidFilter NOT included
    - csid_filter + filters (optional) → periodFilter NOT included  
    - filters only → periodFilter and csidFilter NOT included
    
    Args:
        record_id: The record identifier (required).
            You MUST call `prepare_analytics_record_query` without record_id first to discover available record IDs.
            Then call `prepare_analytics_record_query` with the record_id to get all required information.
            Examples: "ratings", "closed_conversations", "first_response_time".
        timezone: IANA timezone name (required). Examples: "Europe/Copenhagen", "America/New_York", "UTC".
        
        period_filter: Time period filter (PREFERRED - use this for most queries). Optional.
            MUST be passed as a dictionary/object, NOT as a JSON string.
            Preset format: {"_type": "Preset", "value": {"_type": "PreviousWeek"}}
            Custom format: {"_type": "Custom", "value": {"from": "2023-01-01T00:00:00Z", "to": "2023-01-31T23:59:59Z"}}
            Common preset values: "PreviousWeek", "PreviousMonth", "PreviousQuarter", "PreviousYear", "Today", "Yesterday"
            IMPORTANT: 
            - If provided, csid_filter will be ignored and NOT included in the request (discriminated union).
            - When using period_filter, the filters parameter is REQUIRED and must contain at least one filter.
            - At least one of period_filter, csid_filter, or filters must be provided.
            This is the recommended approach for time-based queries.
            Example: {"_type": "Preset", "value": {"_type": "PreviousWeek"}} (as object, not string)
        
        csid_filter: Array of specific conversation IDs to filter by (integers).
            Only use when you need to analyze specific conversations and period_filter is not suitable.
            Must contain at least one conversation ID.
            IMPORTANT: Only used if period_filter is not provided. If period_filter is provided, this parameter is ignored.
            When using csid_filter, periodFilter is NOT included in the request (discriminated union).
            Example: [12345, 12346, 12347]
        
        filters: Additional filters to apply. MUST be passed as an array of objects, NOT as a JSON string.
            Each filter must have a non-empty values array.
            Format: [{"attribute": "channel", "values": ["email", "chat"]}, {"attribute": "queue_id", "values": ["queue-123"]}]
            Common attributes: "channel", "queue_id", "agent_id", "tag_id", "initial_direction", "contact_point"
            IMPORTANT: 
            - When using period_filter: filters is REQUIRED and must contain at least one filter.
            - When using csid_filter: filters is optional.
            - Can be used alone (without period_filter or csid_filter) - must contain at least one filter.
            - Each filter's "values" must be a non-empty array. Filters with null or empty values are automatically removed.
            - At least one of period_filter, csid_filter, or filters must be provided.
            You MUST call `prepare_analytics_record_query` with your record_id first to build valid filters.
            This tool returns all available filter attributes with their valid values.
            Example: [{"attribute": "channel", "values": ["email"]}] (as array, not string)
        
        page_key: Pagination key from a previous response to retrieve the next page (optional).
            Use the "pageKey" from the response to get subsequent pages.
        
        page_limit: Maximum number of records per page (optional, default varies by API).
            Use this to control the size of each page. Combine with page_key for pagination.
    
    Returns:
        Dictionary containing unaggregated record data:
        {
            "data": [
                {
                    "primaryTimestampField": {
                        "name": "created_at",
                        "timestamp": "2023-04-21T10:23:14.293Z"
                    },
                    "fields": [
                        {
                            "name": "csid",
                            "field": {
                                "value": 184472,
                                "_type": "LongField"
                            }
                        },
                        {
                            "name": "initial_direction",
                            "field": {
                                "value": "INBOUND",
                                "label": "Inbound",
                                "_type": "StringField"
                            }
                        }
                    ]
                }
            ],
            "pageKey": "base64-encoded-pagination-key"  // Present if more pages available
        }
    
    Example Usage:
        # Get all closed conversation records for last week (filters required when using period_filter)
        fetch_analytics_record_data(
            record_id="closed_conversations",
            timezone="Europe/Copenhagen",
            period_filter={"_type": "Preset", "value": {"_type": "PreviousWeek"}},
            filters=[{"attribute": "channel", "values": ["email", "chat"]}],  # Required when using period_filter
            page_limit=100
        )
        
        # Get rating records for email channel in custom date range
        fetch_analytics_record_data(
            record_id="ratings",
            timezone="America/New_York",
            period_filter={"_type": "Custom", "value": {"from": "2024-01-01T00:00:00Z", "to": "2024-01-31T23:59:59Z"}},
            filters=[{"attribute": "channel", "values": ["email"]}],  # Required when using period_filter
            page_limit=50
        )
        
        # Get records using filters only (no period_filter or csid_filter)
        fetch_analytics_record_data(
            record_id="closed_conversations",
            timezone="Europe/Copenhagen",
            filters=[{"attribute": "channel", "values": ["email"]}],
            page_limit=100
        )
        
        # Get records for specific conversations (filters optional when using csid_filter)
        fetch_analytics_record_data(
            record_id="closed_conversations",
            timezone="UTC",
            csid_filter=[12345, 12346, 12347],
            filters=[{"attribute": "channel", "values": ["email"]}]  # Optional when using csid_filter
        )
    """
    # Parse JSON strings if provided as strings
    if period_filter and isinstance(period_filter, str):
        period_filter = json.loads(period_filter)
    
    # Parse and validate csid_filter
    if csid_filter and isinstance(csid_filter, str):
        csid_filter = json.loads(csid_filter)
    if csid_filter and not isinstance(csid_filter, list):
        csid_filter = None
    
    # Parse and validate filters
    if filters and isinstance(filters, str):
        filters = json.loads(filters)
    if filters and not isinstance(filters, list):
        filters = None
    
    # Validate and clean filters - ensure each filter has valid values array
    if filters and isinstance(filters, list):
        validated_filters = []
        for filter_obj in filters:
            if isinstance(filter_obj, dict) and "attribute" in filter_obj:
                values = filter_obj.get("values")
                # Only include filter if values is a non-empty array
                if isinstance(values, list) and len(values) > 0:
                    validated_filters.append(filter_obj)
        filters = validated_filters if validated_filters else None
    
    # Validate that at least one of period_filter, csid_filter, or filters is provided
    has_valid_csid = csid_filter and isinstance(csid_filter, list) and len(csid_filter) > 0
    has_valid_period = period_filter is not None
    has_valid_filters = filters and isinstance(filters, list) and len(filters) > 0
    
    if not has_valid_period and not has_valid_csid and not has_valid_filters:
        raise ValueError("At least one of period_filter, csid_filter, or filters must be provided. period_filter is the preferred option.")
    
    # Validate that when using periodFilter, at least one filter is required
    if has_valid_period and not has_valid_filters:
        raise ValueError("When using period_filter, at least one filter in the filters array is required. Use prepare_analytics_record_query to discover available filter attributes and values.")
    
    # The API uses a discriminated union with three possible structures:
    # Structure 1: With periodFilter (preferred) - filters REQUIRED
    #   {
    #     "id": "closed_conversations",
    #     "periodFilter": {"_type": "Preset", "value": {"_type": "PreviousWeek"}},
    #     "filters": [{"attribute": "channel", "values": ["email"]}],
    #     "timezone": "Europe/Copenhagen"
    #   }
    # Structure 2: With csidFilter - filters optional
    #   {
    #     "id": "closed_conversations",
    #     "csidFilter": [42, 43, 44],
    #     "filters": [{"attribute": "initial_direction", "values": ["INBOUND"]}],
    #     "timezone": "Europe/Copenhagen"
    #   }
    # Structure 3: Filters only (no periodFilter, no csidFilter)
    #   {
    #     "id": "closed_conversations",
    #     "filters": [{"attribute": "channel", "values": ["email"]}],
    #     "timezone": "Europe/Copenhagen"
    #   }
    request = {
        "id": record_id,
        "timezone": timezone
    }
    
    # Build request based on provided parameters (discriminated union)
    if has_valid_period:
        # Use GetMetricRecordsDataInputPeriodFilter - include periodFilter, exclude csidFilter (preferred)
        # When using periodFilter, at least one filter is REQUIRED
        request["periodFilter"] = period_filter
        # Do NOT include csidFilter when using periodFilter (discriminated union)
        # Filters are required when using periodFilter (validated above)
        request["filters"] = filters
    elif has_valid_csid:
        # Use GetMetricRecordsDataInputCsidFilter - include csidFilter, exclude periodFilter
        request["csidFilter"] = csid_filter
        # filters can be included with csidFilter approach (optional)
        if has_valid_filters:
            request["filters"] = filters
    elif has_valid_filters:
        # Use filters only (no periodFilter, no csidFilter)
        request["filters"] = filters
    
    # Log the exact payload being sent
    payload_json = json.dumps(request, indent=2)
    print(f"[fetch_analytics_record_data] Request payload:\n{payload_json}")
    
    client = get_dixa_client()
    return client.post_analytics_metric_records_data(
        request=request,
        page_key=page_key,
        page_limit=page_limit
    )

