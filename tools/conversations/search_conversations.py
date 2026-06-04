"""
Tool for searching conversations with filters from the Dixa API.
"""

from typing import Dict, Any, Optional
from tools.base import get_dixa_client


async def search_conversations(
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None,
    filters: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Search for conversations containing a particular text or by filter or combine them both.
    
    Args:
        page_key: Base64 encoded form of pagination query parameters. Do not try to construct or change programmatically as the internal structure may change without notice (optional). May be passed raw or URL-encoded from a next/previous URL.
        page_limit: Maximum number of results per page. Must be less than or equal to 50. May be used in combination with pageKey to change the number of results in between page requests (optional).
        filters: Dictionary containing filter conditions to apply to the search (optional).
                Use the Dixa API JSON filter format, not the Dixa UI URL filter syntax.
                Documented filter field _type values are:
                AgentId, AssignedDate, Channel, ClosedDate, ContactId, ConversationId,
                CreationDate, CustomAttribute, Direction, Duration, LastActivity,
                LastMessage, QueueId, Status, and TagId.
                
                Common operators:
                - TagId: IncludesOne, IncludesAll, ExcludesOne, ExcludesAll, IsEmpty, IsNotEmpty
                - CustomAttribute: IsOneOf, IsNotOneOf, IsEmpty, IsNotEmpty.
                  Use _type "CustomAttribute" with attributeId, not "ConversationCustomAttribute".
                - Status: IsOneOf, IsNotOneOf with values open, closed, pending
                - AgentId/QueueId: IsOneOf, IsNotOneOf, IsEmpty, IsNotEmpty
                - ContactId/ConversationId/Channel/Direction: IsOneOf, IsNotOneOf
                - Timestamp fields (AssignedDate, CreationDate, ClosedDate,
                  LastActivity, LastMessage): Since, Until, Between
                
                Tag example: {
                    "strategy": "All",
                    "conditions": [
                        {
                            "field": {
                                "operator": {
                                    "values": ["tag-id-1", "tag-id-2"],
                                    "_type": "IncludesOne"
                                },
                                "_type": "TagId"
                            }
                        }
                    ]
                }
                
                Status example: {
                    "strategy": "All",
                    "conditions": [
                        {
                            "field": {
                                "operator": {
                                    "values": ["open"],
                                    "_type": "IsOneOf"
                                },
                                "_type": "Status"
                            }
                        }
                    ]
                }
                
                Conversation custom attribute example: {
                    "strategy": "All",
                    "conditions": [
                        {
                            "field": {
                                "operator": {
                                    "values": [["Brand X"]],
                                    "_type": "IsOneOf"
                                },
                                "attributeId": "custom-attribute-id",
                                "_type": "CustomAttribute"
                            }
                        }
                    ]
                }
        query: Dictionary containing query parameters for text search (optional).
    
    Returns:
        Dictionary containing the search results with the following structure:
        {
            "data": [
                {
                    "id": 1234,
                    "highlights": {}
                }
            ],
            "meta": {
                "next": "/<api-version>/search/conversations/?pageKey=..."
            }
        }
    """
    # Validate page_limit doesn't exceed API maximum
    if page_limit is not None and page_limit > 50:
        raise ValueError(f"page_limit must be less than or equal to 50, but got {page_limit}")
    
    client = get_dixa_client()
    return client.post_search_conversations(
        page_key=page_key,
        page_limit=page_limit,
        filters=filters,
        query=query
    )
