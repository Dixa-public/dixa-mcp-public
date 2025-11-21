"""
Tool for getting metric records data (unaggregated) from the Dixa Analytics API.
"""

import json
from typing import Dict, Any, Optional, List, Union
from tools.base import get_dixa_client


async def fetch_unaggregated_data(
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
    
    🚨 MANDATORY WORKFLOW - YOU MUST START WITH AGGREGATED DATA FIRST:
    Before using this tool, you MUST ALWAYS first call `fetch_aggregated_data` to get summary statistics.
    Only proceed to this unaggregated tool if:
    1. You have already called `fetch_aggregated_data` and reviewed the aggregated results
    2. The aggregated data is insufficient for your needs
    3. You specifically require detailed, row-level individual records for analysis
    
    This tool fetches individual (unaggregated) records for a specific metric. Use this ONLY when you need
    detailed, row-level data rather than summary statistics. Each record represents a single data point
    (e.g., an individual conversation, rating, or event).
    
    Why aggregated data first is mandatory:
    - It's faster and more efficient
    - Provides summary statistics (counts, percentages, averages) that are usually sufficient
    - Doesn't require pagination for large datasets
    - Uses less API resources
    - Most analytics questions can be answered with aggregated data alone
    
    ⚠️ DO NOT use this tool unless you have already tried `fetch_aggregated_data` and determined it's insufficient.
    
    🔄 PAGINATION - COLLECT ALL AVAILABLE DATA:
    When using this tool, ALWAYS paginate through ALL available pages to collect complete datasets.
    The response includes a "pageKey" field when more data is available. You MUST:
    1. Make the first request with page_limit (100-300 recommended)
    2. Check if the response contains a "pageKey" field
    3. If "pageKey" exists, make another call with the same payload but using page_key (page_limit not needed)
    4. Repeat steps 2-3 until no "pageKey" is returned, indicating you've collected all available data
    5. Combine all collected data from all pages for complete analysis
    
    This ensures you have the full dataset rather than just the first page of results.
    
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
        record_id: The record identifier (required when page_key is not provided).
            When page_key is provided, this parameter is not needed as it's encoded in the key.
            You MUST call `prepare_analytics_record_query` without record_id first to discover available record IDs.
            Then call `prepare_analytics_record_query` with the record_id to get all required information.
            Examples: "ratings", "closed_conversations", "first_response_time".
        timezone: IANA timezone name (required when page_key is not provided).
            When page_key is provided, this parameter is not needed as it's encoded in the key.
            Examples: "Europe/Copenhagen", "America/New_York", "UTC".
        
        period_filter: Time period filter (PREFERRED - use this for most queries). Optional.
            MUST be passed as a dictionary/object, NOT as a JSON string.
            Preset format: {"_type": "Preset", "value": {"_type": "PreviousWeek"}}
            Custom interval format: {"_type": "Interval", "start": "2025-05-19T00:00:00Z", "end": "2025-11-19T23:59:59Z"}
            Common preset values: "PreviousWeek", "PreviousMonth", "PreviousQuarter", "PreviousYear", "Today", "Yesterday"
            IMPORTANT: 
            - If provided, csid_filter will be ignored and NOT included in the request (discriminated union).
            - When using period_filter, the filters parameter is REQUIRED and must contain at least one filter.
            - At least one of period_filter, csid_filter, or filters must be provided.
            This is the recommended approach for time-based queries.
            Example (preset): {"_type": "Preset", "value": {"_type": "PreviousWeek"}}
            Example (custom interval): {"_type": "Interval", "start": "2025-05-19T00:00:00Z", "end": "2025-11-19T23:59:59Z"}
        
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
            IMPORTANT: When page_key is provided, you should still provide the same payload (record_id, timezone, filters, etc.)
            as the original request. The page_key is just a query parameter, but the API expects the same POST request with the same payload.
                    When page_key is provided, page_limit is optional and not required.
        
        page_limit: Maximum number of records per page (optional, default varies by API).
                    MUST be between 1 and 300 (inclusive) when page_key is not provided. Recommended: 100-300 for first request.
                    When page_key is provided, page_limit is optional and can be omitted (the page size is encoded in the key).
                    Use this to control the size of each page. For large datasets, use page_limit on the first request, then iterate through pages using page_key.
    
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
        
        Field Usage Guidance:
        - MOST USEFUL: Extract field "value" and "name" from each field entry - these contain the actual data
        - USEFUL: Extract "timestamp" from primaryTimestampField for time-based analysis
        - OPTIONAL: Extract "label" if human-readable names are needed
        - CAN IGNORE: "_type" fields are verbose metadata that can be ignored unless specifically needed
        - CAN IGNORE: Nested field structures can be flattened - focus on the actual values
        - For large datasets: Consider extracting only fields relevant to the user's query rather than all fields
    
    Example Usage:
        # Get all closed conversation records for last week (filters required when using period_filter)
        fetch_unaggregated_data(
            record_id="closed_conversations",
            timezone="Europe/Copenhagen",
            period_filter={"_type": "Preset", "value": {"_type": "PreviousWeek"}},
            filters=[{"attribute": "channel", "values": ["email", "chat"]}],  # Required when using period_filter
            page_limit=300
        )
        
        # Get rating records for email channel in custom date range
        fetch_unaggregated_data(
            record_id="ratings",
            timezone="America/New_York",
            period_filter={"_type": "Interval", "start": "2024-01-01T00:00:00Z", "end": "2024-01-31T23:59:59Z"},
            filters=[{"attribute": "channel", "values": ["email"]}],  # Required when using period_filter
            page_limit=300
        )
        
        # Get records using filters only (no period_filter or csid_filter)
        fetch_unaggregated_data(
            record_id="closed_conversations",
            timezone="Europe/Copenhagen",
            filters=[{"attribute": "channel", "values": ["email"]}],
            page_limit=300
        )
        
        # Get records for specific conversations (filters optional when using csid_filter)
        fetch_unaggregated_data(
            record_id="closed_conversations",
            timezone="UTC",
            csid_filter=[12345, 12346, 12347],
            filters=[{"attribute": "channel", "values": ["email"]}]  # Optional when using csid_filter
        )
        
        # Pagination example: Collect ALL available data by iterating through all pages
        # First page:
        all_data = []
        response = fetch_unaggregated_data(
            record_id="closed_conversations",
            timezone="Europe/Copenhagen",
            period_filter={"_type": "Preset", "value": {"_type": "PreviousMonth"}},
            filters=[{"attribute": "channel", "values": ["email"]}],
            page_limit=300  # Use 100-300 for first request
        )
        all_data.extend(response.get("data", []))
        
        # Continue paginating until all data is collected
        while "pageKey" in response:
            response = fetch_unaggregated_data(
                record_id="closed_conversations",
                timezone="Europe/Copenhagen",
                period_filter={"_type": "Preset", "value": {"_type": "PreviousMonth"}},
                filters=[{"attribute": "channel", "values": ["email"]}],
                page_key=response.get("pageKey")  # page_limit not needed when using page_key
            )
            all_data.extend(response.get("data", []))
        
        # Now all_data contains all records from all pages
    
    📋 CONTEXT MANAGEMENT INSTRUCTIONS - IMPORTANT FOR LARGE RESPONSES:
    When processing responses from this tool, especially with large datasets (multiple pages, 100-300 records per page):
    
    1. EXTRACT ONLY RELEVANT INFORMATION:
       - Extract only fields that are relevant to answering the user's specific question
       - Focus on field "value" and "name" properties - these contain the actual data
       - Extract timestamps when time-based analysis is needed
       - Ignore verbose metadata like "_type" fields unless specifically required
    
    2. SUMMARIZE LARGE DATASETS:
       - For large datasets, create summaries rather than storing all raw data
       - Examples: "Found 500 records with average value X", "Total count: Y", "Date range: A to B"
       - Calculate key metrics (counts, averages, min/max) and store those instead of all records
       - Only store individual record details if the user specifically needs them
    
    3. STORE ESSENTIAL FIELDS ONLY:
       - Store only essential fields needed to answer the question (IDs, timestamps, key values)
       - Don't store verbose nested structures unless necessary
       - Consider flattening data structures to reduce context usage
    
    4. USE AGGREGATED DATA WHEN POSSIBLE:
       - If aggregated data is available, prefer using those summaries instead of storing all unaggregated records
       - Aggregated data provides the same insights with much less context usage
    
    5. QUERY-CONTEXT AWARENESS:
       - Let the user's question guide what information to extract and store
       - If the question asks for a count, store the count, not all records
       - If the question asks for specific records, extract only those relevant fields
       - Don't store information that doesn't contribute to answering the question
    
    Remember: The full response data is always available in the tool response. You don't need to store everything in context - extract and summarize what's needed to answer the user's question efficiently.
    """
    client = get_dixa_client()
    
    # Validate page_limit if provided (only when page_key is not provided)
    # When page_key is provided, page_limit is optional and not validated strictly
    if page_limit is not None and page_key is None:
        if page_limit < 1:
            raise ValueError(f"page_limit must be at least 1, but got {page_limit}")
        if page_limit > 300:
            raise ValueError(f"page_limit must be at most 300, but got {page_limit}. For large datasets, use pagination with page_key instead of requesting large page sizes.")
    
    # Build full payload - API expects the same payload even when page_key is provided
    # The page_key is just a query parameter, but the same POST request with payload should be sent
    # When page_key is provided, validation is less strict since the key encodes the query info
    
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
    # Skip validation if page_key is provided (the key encodes the query info)
    has_valid_csid = csid_filter and isinstance(csid_filter, list) and len(csid_filter) > 0
    has_valid_period = period_filter is not None
    has_valid_filters = filters and isinstance(filters, list) and len(filters) > 0
    
    if not page_key:
        # Only validate when page_key is not provided
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
    #   OR for custom intervals:
    #   {
    #     "id": "closed_conversations",
    #     "periodFilter": {"_type": "Interval", "start": "2025-05-19T00:00:00Z", "end": "2025-11-19T23:59:59Z"},
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
    if page_key:
        print(f"[fetch_unaggregated_data] Using page_key for pagination (POST request with same payload + pageKey query param)")
    else:
        print(f"[fetch_unaggregated_data] Request payload:\n{payload_json}")
    
    result = client.post_analytics_metric_records_data(
        request=request,
        page_key=page_key,
        page_limit=page_limit
    )
    
    # Log the response
    response_json = json.dumps(result, indent=2)
    print(f"[fetch_unaggregated_data] Response:\n{response_json}")
    
    return result

