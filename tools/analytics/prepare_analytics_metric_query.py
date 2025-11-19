"""
Tool for preparing analytics metric queries by gathering all required information in one call.
"""

import json
from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def prepare_analytics_metric_query(metric_id: Optional[str] = None, page_key: Optional[str] = None, page_limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Prepare all information needed to build a valid payload for fetch_analytics_metric_data.
    
    This tool combines multiple prerequisite calls into a single operation:
    - If metric_id is not provided: Lists all available metrics (replaces list_analytics_metrics)
    - If metric_id is provided: Fetches metric details (available filters and aggregations) and filter values
    
    Use this tool BEFORE calling fetch_analytics_metric_data to get all required information
    needed to construct a valid request payload.
    
    Args:
        metric_id: The metric identifier (optional). 
            If not provided, returns a list of all available metrics.
            If provided, returns detailed information for that specific metric including filters and aggregations.
            Examples: "csat", "closed_conversations", "first_response_time".
        page_key: Optional pagination key (only used when metric_id is not provided).
        page_limit: Optional limit for pagination (only used when metric_id is not provided).
    
    Returns:
        If metric_id is not provided: Dictionary containing list of all available metrics (same format as list_analytics_metrics).
        If metric_id is provided: Dictionary containing all information needed to build a valid payload:
        {
            "metric_id": "closed_conversations",
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
            "available_aggregations": [
                {"measure": "Count", "description": "Conversation closed count"},
                {"measure": "Percentage", "description": "Calculated Percentage"}
            ],
            "related_record_ids": ["closed_conversations"]
        }
    """
    client = get_dixa_client()
    
    # If no metric_id provided, list all available metrics
    if metric_id is None:
        result = client.get_analytics_metrics_catalogue(
            page_key=page_key,
            page_limit=page_limit
        )
        print(f"[prepare_analytics_metric_query] Response (listing all metrics):\n{json.dumps(result, indent=2)}")
        return result
    
    # Step 1: Get metric details
    metric_details = client.get_analytics_metric_description(metric_id=metric_id)
    
    # Step 2: Get filter values for all available filter attributes
    available_filters = []
    if "filters" in metric_details.get("data", {}):
        for filter_info in metric_details["data"]["filters"]:
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
        "metric_id": metric_id,
        "description": metric_details.get("data", {}).get("description", ""),
        "available_filters": available_filters,
        "available_aggregations": metric_details.get("data", {}).get("aggregations", []),
        "related_record_ids": metric_details.get("data", {}).get("relatedRecordIds", [])
    }
    
    print(f"[prepare_analytics_metric_query] Response (metric_id={metric_id}):\n{json.dumps(result, indent=2)}")
    return result

