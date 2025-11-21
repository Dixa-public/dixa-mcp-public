"""
Tool for preparing analytics record queries by gathering all required information in one call.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def prepare_analytics_record_query(record_id: Optional[str] = None, page_key: Optional[str] = None, page_limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Prepare all information needed to build a valid payload for fetch_unaggregated_data.
    
    🚨 MANDATORY: You MUST first use `prepare_analytics_metric_query` and `fetch_aggregated_data` before using this tool.
    Aggregated data is faster, more efficient, and usually provides the insights you need.
    Only use this tool if you have already tried aggregated data and determined it's insufficient for your needs.
    
    🔄 When using `fetch_unaggregated_data`, remember to paginate through ALL pages to collect complete datasets.
    Check for "pageKey" in responses and continue making calls until all data is collected.
    
    This tool combines multiple prerequisite calls into a single operation:
    - If record_id is not provided: Lists all available records (replaces list_analytics_records)
    - If record_id is provided: Fetches record details (available filters and field metadata) and filter values
    
    Use this tool BEFORE calling fetch_unaggregated_data to get all required information
    needed to construct a valid request payload.
    
    Args:
        record_id: The record identifier (optional).
            If not provided, returns a list of all available records.
            If provided, returns detailed information for that specific record including filters.
            Examples: "ratings", "closed_conversations", "first_response_time".
        page_key: Optional pagination key (only used when record_id is not provided).
        page_limit: Optional limit for pagination (only used when record_id is not provided).
    
    Returns:
        If record_id is not provided: Dictionary containing list of all available records (same format as list_analytics_records).
        If record_id is provided: Dictionary containing all information needed to build a valid payload:
        {
            "record_id": "closed_conversations",
            "description": "Closed conversation data",
            "available_filters": [
                {
                    "attribute": "channel",
                    "description": "Used to filter by the channel",
                    "values": [
                        {"value": "EMAIL", "label": "Email"},
                        {"value": "CHAT", "label": "Chat"}
                    ]
                },
                {
                    "attribute": "queue_id",
                    "description": "Used to filter by the queue_id",
                    "values": [...]  # All valid values for this attribute
                }
            ],
            "fields_metadata": [
                {
                    "field": "closed_at",
                    "description": "Timestamp of when the conversation was closed",
                    "nullable": false
                }
            ],
            "related_metric_ids": ["closed_conversations"]
        }
    """
    client = get_dixa_client()
    
    # If no record_id provided, list all available records
    if record_id is None:
        return client.get_analytics_records_catalogue(
            page_key=page_key,
            page_limit=page_limit
        )
    
    # Step 1: Get record details
    record_details = client.get_analytics_record_description(record_id=record_id)
    
    # Step 2: Get filter values for all available filter attributes
    available_filters = []
    if "filters" in record_details.get("data", {}):
        for filter_info in record_details["data"]["filters"]:
            filter_attribute = filter_info.get("filterAttribute")
            if filter_attribute:
                try:
                    filter_values = client.get_analytics_filter_values(filter_attribute=filter_attribute)
                    available_filters.append({
                        "attribute": filter_attribute,
                        "description": filter_info.get("description", ""),
                        "values": filter_values.get("data", [])
                    })
                except Exception:
                    # If filter values can't be fetched, still include the attribute info
                    available_filters.append({
                        "attribute": filter_attribute,
                        "description": filter_info.get("description", ""),
                        "values": []
                    })
    
    # Build comprehensive response
    result = {
        "record_id": record_id,
        "description": record_details.get("data", {}).get("description", ""),
        "available_filters": available_filters,
        "fields_metadata": record_details.get("data", {}).get("fieldsMetadata", []),
        "related_metric_ids": record_details.get("data", {}).get("relatedMetricIds", [])
    }
    
    return result

