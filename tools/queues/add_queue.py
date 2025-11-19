"""
Tool for creating a queue from the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any, Optional, List
from tools.base import get_dixa_client


async def add_queue(
    name: str,
    call_functionality: Optional[bool] = None,
    is_default: Optional[bool] = None,
    queue_thresholds: Optional[Dict[str, Any]] = None,
    offer_timeout: Optional[int] = None,
    offer_algorithm: Optional[str] = None,
    wrapup_timeout: Optional[int] = None,
    priority: Optional[int] = None,
    offer_abandoned_conversations: Optional[bool] = None,
    do_not_offer_timeouts: Optional[Dict[str, Any]] = None,
    is_do_not_offer_enabled: Optional[bool] = None,
    preferred_agent_timeouts: Optional[Dict[str, Any]] = None,
    is_preferred_agent_enabled: Optional[bool] = None,
    preferred_agent_offline_timeout: Optional[int] = None,
    personal_agent_offline_timeout: Optional[int] = None,
    is_restricted: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Create a queue.
    
    ⚠️ WARNING: This is a MODIFICATION endpoint that will create a queue in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        name: The name of the queue (required).
        call_functionality: Whether the queue has call functionality (optional).
        is_default: Whether this is the default queue (optional).
        queue_thresholds: Dictionary of queue thresholds (optional).
        offer_timeout: Offer timeout in seconds (optional).
        offer_algorithm: The offering algorithm (e.g., "AllAtOnce", "OneAtATimeRandom") (optional).
        wrapup_timeout: Wrap-up timeout in seconds (optional).
        priority: Queue priority (optional).
        offer_abandoned_conversations: Whether to offer abandoned conversations (optional).
        do_not_offer_timeouts: Dictionary of do-not-offer timeouts by channel (optional).
        is_do_not_offer_enabled: Whether do-not-offer is enabled (optional).
        preferred_agent_timeouts: Dictionary of preferred agent timeouts by channel (optional).
        is_preferred_agent_enabled: Whether preferred agent is enabled (optional).
        preferred_agent_offline_timeout: Preferred agent offline timeout (optional).
        personal_agent_offline_timeout: Personal agent offline timeout (optional).
        is_restricted: Whether the queue is restricted (optional).
    
    Returns:
        Dictionary containing the created queue.
    """
    client = get_dixa_client()
    return client.create_queue(
        name=name,
        call_functionality=call_functionality,
        is_default=is_default,
        queue_thresholds=queue_thresholds,
        offer_timeout=offer_timeout,
        offer_algorithm=offer_algorithm,
        wrapup_timeout=wrapup_timeout,
        priority=priority,
        offer_abandoned_conversations=offer_abandoned_conversations,
        do_not_offer_timeouts=do_not_offer_timeouts,
        is_do_not_offer_enabled=is_do_not_offer_enabled,
        preferred_agent_timeouts=preferred_agent_timeouts,
        is_preferred_agent_enabled=is_preferred_agent_enabled,
        preferred_agent_offline_timeout=preferred_agent_offline_timeout,
        personal_agent_offline_timeout=personal_agent_offline_timeout,
        is_restricted=is_restricted
    )

