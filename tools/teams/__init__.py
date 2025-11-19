"""
Team-related tools for the Dixa MCP Server.

This module contains tools for interacting with Dixa teams.
"""

from tools.teams.list_teams import list_teams
from tools.teams.fetch_team_by_id import fetch_team_by_id
from tools.teams.list_team_agents import list_team_agents
from tools.teams.list_team_presence import list_team_presence
from tools.teams.add_team import add_team
from tools.teams.add_agents_to_team import add_agents_to_team
from tools.teams.remove_agents_from_team import remove_agents_from_team
from tools.teams.remove_team import remove_team

__all__ = [
    "list_teams",
    "fetch_team_by_id",
    "list_team_agents",
    "list_team_presence",
    "add_team",
    "add_agents_to_team",
    "remove_agents_from_team",
    "remove_team",
]
