"""
Tools package for Dixa MCP Server.

This package contains all MCP tools organized by Dixa API categories.
Each category has its own subdirectory with related tools.
"""

# Import all tools to make them available
from tools.organization import fetch_organization_details

__all__ = [
    "fetch_organization_details",
]

