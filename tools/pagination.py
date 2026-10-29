"""Bounded MCP page sizes for list and record operations."""
from typing_extensions import Annotated
from pydantic import Field

PageLimit = Annotated[int, Field(ge=1, le=100, description="Results per page, 1-100; default 50. Fetch another page only when needed.")]
