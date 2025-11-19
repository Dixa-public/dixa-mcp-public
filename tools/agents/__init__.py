"""
Agent-related tools for the Dixa MCP Server.

This module contains tools for interacting with Dixa agents/admins.
"""

from tools.agents.fetch_agent_by_id import fetch_agent_by_id
from tools.agents.list_agents import list_agents
from tools.agents.list_agents_presence import list_agents_presence
from tools.agents.list_agent_teams import list_agent_teams
from tools.agents.add_agent import add_agent
from tools.agents.modify_agent_partial import modify_agent_partial
from tools.agents.update_agent_full import update_agent_full
from tools.agents.set_agent_working_channel import set_agent_working_channel

__all__ = [
    "fetch_agent_by_id",
    "list_agents",
    "list_agents_presence",
    "list_agent_teams",
    "add_agent",
    "modify_agent_partial",
    "update_agent_full",
    "set_agent_working_channel",
]

