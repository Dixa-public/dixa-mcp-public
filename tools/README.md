# Tools Directory

This directory contains all MCP tools organized by Dixa API categories.

## Structure

```
tools/
├── __init__.py              # Main tools package init
├── base.py                  # Base utilities (API key extraction, DixaClient helpers)
├── organization/            # Organization-related tools
│   ├── __init__.py
│   └── get_organization_info.py
├── conversations/           # Conversation/ticket tools
│   └── __init__.py
├── users/                   # User/agent tools
│   └── __init__.py
├── teams/                   # Team management tools
│   └── __init__.py
├── analytics/               # Analytics and reporting tools
│   └── __init__.py
├── settings/                # Settings management tools
│   └── __init__.py
├── contacts/                # Contact management tools
│   └── __init__.py
└── integrations/            # Integration management tools
    └── __init__.py
```

## Adding New Tools

### Step 1: Create the Tool File

Create a new Python file in the appropriate category directory:

```python
# tools/conversations/get_conversation.py
from typing import Dict, Any
from tools.base import get_dixa_client

async def get_conversation(conversation_id: str) -> Dict[str, Any]:
    """
    Get a specific conversation by ID.
    
    Args:
        conversation_id: The ID of the conversation to retrieve.
    
    Returns:
        Dictionary containing conversation information.
    """
    client = get_dixa_client()
    # Add your API call here
    # Example: return client.get_conversation(conversation_id)
    pass
```

### Step 2: Update Category __init__.py

Add the import to the category's `__init__.py`:

```python
# tools/conversations/__init__.py
from tools.conversations.get_conversation import get_conversation

__all__ = ["get_conversation"]
```

### Step 3: Register in server.py

Add the tool to `server.py`:

```python
# server.py
from tools.conversations import get_conversation

@mcp.tool
async def get_conversation_tool(conversation_id: str) -> Dict[str, Any]:
    """Get a specific conversation by ID."""
    return await get_conversation(conversation_id)
```

### Step 4: Add API Method to DixaClient

If needed, add the corresponding method to `dixa_api.py`:

```python
# dixa_api.py
def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
    """Get a conversation by ID."""
    url = f"{self.base_url}/conversations/{conversation_id}"
    response = requests.get(url, headers=self.headers)
    response.raise_for_status()
    return response.json()
```

## Best Practices

1. **Use `get_dixa_client()`**: Always use the helper from `tools.base` to get a configured client
2. **Async Functions**: Make tool functions async for better performance
3. **Type Hints**: Always include type hints for parameters and return values
4. **Docstrings**: Include clear docstrings explaining what the tool does
5. **Error Handling**: Let DixaClient handle HTTP errors, but add context-specific error messages if needed
6. **Naming**: Use descriptive names that match the Dixa API endpoint names
7. **Creation/Modification Endpoints**: For POST, PATCH, PUT, DELETE endpoints:
   - Add a clear ⚠️ WARNING in the docstring that this modifies data
   - Explicitly state that the AI assistant MUST obtain user confirmation before execution
   - Include the warning at the top of the tool file as well

## Example: Complete Tool Implementation

### Read-Only Tool (GET)

```python
# tools/conversations/list_conversations.py
from typing import Dict, Any, List, Optional
from tools.base import get_dixa_client

async def list_conversations(
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    List conversations with optional filtering.
    
    Args:
        limit: Maximum number of conversations to return (default: 50)
        offset: Number of conversations to skip (default: 0)
        status: Filter by conversation status (optional)
    
    Returns:
        Dictionary containing a list of conversations and pagination info.
    """
    client = get_dixa_client()
    # Implementation would go here
    # return client.list_conversations(limit=limit, offset=offset, status=status)
    pass
```

### Creation/Modification Tool (POST/PATCH/PUT/DELETE)

```python
# tools/users/create_agent.py
"""
Tool for creating a new agent/admin in the Dixa API.

⚠️ WARNING: This is a CREATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

from typing import Dict, Any
from tools.base import get_dixa_client

async def create_agent(
    display_name: str,
    email: str
) -> Dict[str, Any]:
    """
    Create a new agent/admin in the organization.
    
    ⚠️ WARNING: This is a CREATION endpoint that will create a new agent in your Dixa organization.
    The AI assistant MUST obtain explicit user confirmation before executing this tool.
    
    Args:
        display_name: Display name for the agent (required).
        email: Email address for the agent (required).
    
    Returns:
        Dictionary containing the created agent information.
    """
    client = get_dixa_client()
    return client.create_agent(display_name=display_name, email=email)
```

