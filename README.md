# Dixa MCP Server

A Model Context Protocol (MCP) server that provides access to the Dixa API, allowing AI assistants to interact with Dixa organization data and services.

## Features

- **Organization Information**: Retrieve organization details from the Dixa API
- **Flexible Authentication**: Multiple ways to provide API keys (environment variables, command-line args, client auth)
- **Multiple Transport Options**: Supports both subprocess (for Claude Desktop) and HTTP/SSE transports
- **Error Handling**: Comprehensive error handling with detailed error messages

## Prerequisites

- Python 3.8 or higher
- A Dixa API key
- (Optional) Claude Desktop for MCP client integration

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Dixa-public/dixa-mcp-public.git
cd dixa-mcp-public
```

Or using SSH:

```bash
git clone git@github.com:Dixa-public/dixa-mcp-public.git
cd dixa-mcp-public
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install fastmcp requests
```

Or install from the project:

```bash
pip install -e .
```

## Running Locally

### Start the Server

After installation, you can run the server locally:

#### Subprocess Mode (Default for Claude Desktop)

```bash
source venv/bin/activate
python server.py
```

Or with API key via command line:

```bash
source venv/bin/activate
python server.py --api-key your-dixa-api-key-here
```

#### HTTP/SSE Mode (For Remote Access)

Start the HTTP server on a specific port:

```bash
source venv/bin/activate
python server.py --http 8000
```

The server will be available at `http://localhost:8000/mcp`.

**Note**: For local HTTP servers, you'll need to use `mcp-remote` with the `--allow-http` flag when configuring Claude Desktop.

## Claude Desktop Configuration

The Dixa MCP server can be configured in Claude Desktop in three ways:

### 1. dixa-local (Local Subprocess)

Runs the project locally as a subprocess. This is the simplest setup for local development.

**Configuration File**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "dixa-local": {
      "command": "<path-to-venv-python>/python",
      "args": [
        "<path-to-repo>/dixa-mcp-public/server.py",
        "--api-key",
        "<your-api-key>"
      ]
    }
  }
}
```

**Example** (macOS):
```json
{
  "mcpServers": {
    "dixa-local": {
      "command": "/Users/username/dixa-mcp-public/venv/bin/python",
      "args": [
        "/Users/username/dixa-mcp-public/server.py",
        "--api-key",
        "your-dixa-api-key-here"
      ]
    }
  }
}
```

**Alternative**: You can also use environment variables instead of command-line args:

```json
{
  "mcpServers": {
    "dixa-local": {
      "command": "/Users/username/dixa-mcp-public/venv/bin/python",
      "args": [
        "/Users/username/dixa-mcp-public/server.py"
      ],
      "env": {
        "DIXA_API_KEY": "your-dixa-api-key-here"
      }
    }
  }
}
```

### 2. dixa-local-remote (Local HTTP Server)

Replicates a remote setup locally. The server runs as an HTTP server on your machine, and Claude Desktop connects via `mcp-remote`.

**Step 1**: Start the HTTP server locally:

```bash
cd dixa-mcp-public
source venv/bin/activate
python server.py --http 8000
```

**Step 2**: Configure Claude Desktop:

```json
{
  "mcpServers": {
    "dixa-local-remote": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp",
        "--header",
        "Authorization: Bearer <your-api-key>",
        "--allow-http"
      ]
    }
  }
}
```

**Note**: The `--allow-http` flag is required for local HTTP servers (not needed for HTTPS).

### 3. dixa-remote (Live Remote Setup)

Connects to a live remote server (e.g., deployed on FastMCP Cloud or your own server).

```json
{
  "mcpServers": {
    "dixa-remote": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://dixa-mcp-public.fastmcp.app/mcp",
        "--header",
        "Authorization: Bearer <your-api-key>"
      ]
    }
  }
}
```

**Note**: If you run the MCP server on your own server, replace `https://dixa-mcp-public.fastmcp.app/mcp` with your actual remote server URL.

### Configuration Summary

| Method | Use Case | Server Command | Notes |
|-------|----------|----------------|-------|
| `dixa-local` | Local development | `python server.py --api-key <key>` | Simplest setup, runs as subprocess |
| `dixa-local-remote` | Testing remote setup locally | `python server.py --http 8000` | Requires `--allow-http` flag |
| `dixa-remote` | Production/remote deployment | Server runs remotely | No local server needed |

### Authentication Methods

The server supports API key authentication through multiple methods (in priority order):

1. **HTTP Authorization Header**: Automatically extracted from `Authorization: Bearer ...` header (for HTTP/SSE transport)
2. **Command-Line Argument**: Pass via `--api-key` flag (for subprocess transport)
3. **Environment Variable**: Set `DIXA_API_KEY` environment variable

**Note**: For remote HTTP/SSE servers, the API key is automatically extracted from the Authorization header sent by `mcp-remote`. You don't need to pass it as a tool parameter.

## Running the Server

### Subprocess Mode (Default)

For Claude Desktop or other subprocess-based MCP clients:

```bash
source venv/bin/activate
python server.py
```

### HTTP/SSE Mode

For HTTP-based clients:

```bash
source venv/bin/activate
python server.py --http [port]
```

Default port is 8000 if not specified.

### With Command-Line API Key

```bash
source venv/bin/activate
python server.py --api-key your-dixa-api-key-here
```

## Available Tools

The Dixa MCP server provides comprehensive access to the Dixa API through organized tool categories. All tools automatically extract the API key from the Authorization header or configuration.

### Organization Tools

- **`fetch_organization_details`**: Retrieves organization information from the Dixa API.

### Agent Tools

- **`fetch_agent_by_id`**: Get a specific agent/admin by ID.
- **`list_agents`**: List all agents/admins in the organization.
- **`list_agents_presence`**: List presence status for all agents.
- **`list_agent_teams`**: List teams that an agent belongs to.
- **`add_agent`**: Create a new agent/admin.
- **`modify_agent_partial`**: Partially update an agent (PATCH).
- **`update_agent_full`**: Fully update an agent (PUT).
- **`set_agent_working_channel`**: Set the working channel for an agent.

### End User Tools

- **`list_end_users`**: List all end users (customers) in the organization.
- **`fetch_end_user_by_id`**: Get a specific end user by ID.
- **`add_end_user`**: Create a new end user.
- **`add_end_users_bulk`**: Create multiple end users in bulk.
- **`modify_end_user_partial`**: Partially update an end user (PATCH).
- **`modify_end_users_bulk`**: Partially update multiple end users in bulk.
- **`update_end_user_full`**: Fully update an end user (PUT).
- **`update_end_users_bulk`**: Fully update multiple end users in bulk.
- **`list_end_user_conversations`**: List all conversations for a specific end user.
- **`anonymize_end_user`**: Anonymize an end user (GDPR compliance, typically irreversible).

### Conversation Tools

- **`fetch_conversation_by_id`**: Get a specific conversation by ID.
- **`search_conversations`**: Search conversations with filters (strategy, conditions, pagination).
- **`list_conversation_flows`**: List conversation flows for a conversation.
- **`list_conversation_activity_log`**: List activity log entries for a conversation.
- **`list_conversation_notes`**: List notes for a conversation.
- **`list_linked_conversations`**: List conversations linked to a parent conversation.
- **`list_conversation_messages`**: List messages in a conversation.
- **`list_organization_activity_log`**: List activity log entries across the organization.
- **`list_conversation_ratings`**: List ratings for a conversation.
- **`start_conversation`**: Create a new conversation.
- **`import_conversations`**: Import conversations in bulk.
- **`add_conversation_note`**: Add a note to a conversation.
- **`add_conversation_notes_bulk`**: Add multiple notes to conversations in bulk.
- **`tag_conversation`**: Add a tag to a conversation.
- **`tag_conversation_bulk`**: Add tags to multiple conversations in bulk.
- **`remove_tag_from_conversation`**: Remove a tag from a conversation.
- **`assign_conversation_to_agent`**: Assign/claim a conversation to an agent.
- **`close_conversation`**: Close a conversation.
- **`reopen_conversation`**: Reopen a closed conversation.
- **`link_conversation_to_parent`**: Link a conversation to a parent conversation.
- **`set_conversation_followup_status`**: Set follow-up status for a conversation.
- **`anonymize_conversation`**: Anonymize a conversation (GDPR compliance, typically irreversible).
- **`anonymize_conversation_message`**: Anonymize a specific message in a conversation (GDPR compliance, typically irreversible).

### Custom Attributes Tools

- **`list_custom_attributes`**: List all custom attribute definitions.
- **`fetch_custom_attribute_by_id`**: Get a specific custom attribute definition by ID.
- **`update_conversation_custom_attributes`**: Update custom attributes for a conversation.
- **`update_end_user_custom_attributes`**: Update custom attributes for an end user.

### Tag Tools

- **`list_tags`**: List all tags in the organization.
- **`fetch_tag_by_id`**: Get a specific tag by ID.
- **`list_conversation_tags`**: List tags on a specific conversation.
- **`add_tag`**: Create a new tag.
- **`activate_tag`**: Activate a tag.
- **`deactivate_tag`**: Deactivate a tag.
- **`remove_tag`**: Delete a tag.

### Team Tools

- **`list_teams`**: List all teams in the organization.
- **`fetch_team_by_id`**: Get a specific team by ID.
- **`list_team_agents`**: List agents in a team.
- **`list_team_presence`**: List presence status for agents in a team.
- **`add_team`**: Create a new team.
- **`add_agents_to_team`**: Add agents to a team.
- **`remove_agents_from_team`**: Remove agents from a team.
- **`remove_team`**: Delete a team.

### Queue Tools

- **`list_queues`**: List all queues in the organization.
- **`fetch_queue_by_id`**: Get a specific queue by ID.
- **`check_queue_availability`**: Check if a queue is available.
- **`check_conversation_queue_position`**: Check the position of a conversation in a queue.
- **`list_queue_agents`**: List agents assigned to a queue.
- **`add_queue`**: Create a new queue.
- **`assign_agents_to_queue`**: Assign agents to a queue.
- **`remove_agents_from_queue`**: Remove agents from a queue.

### Knowledge Base Tools

- **`list_knowledge_articles`**: List all knowledge base articles.
- **`fetch_knowledge_article_by_id`**: Get a specific knowledge base article by ID.
- **`list_knowledge_categories`**: List all knowledge base categories.
- **`add_knowledge_article`**: Create a new knowledge base article.
- **`modify_knowledge_article`**: Update a knowledge base article.
- **`remove_knowledge_article`**: Delete a knowledge base article.
- **`add_knowledge_category`**: Create a new knowledge base category.

### Settings Tools

- **`list_contact_endpoints`**: List all contact endpoints (channels).
- **`fetch_contact_endpoint_by_id`**: Get a specific contact endpoint by ID.
- **`check_business_hours_status`**: Check if business hours are currently active.
- **`list_business_hours_schedules`**: List all business hours schedules.

### Analytics Tools

- **`prepare_analytics_metric_query`**: Prepare analytics metric queries by discovering available metrics, filters, aggregations, and filter values. Use this before calling `fetch_aggregated_data`.
- **`fetch_aggregated_data`**: Fetch aggregated (summary) analytics data for metrics. Provides summary statistics like counts, percentages, averages. **Always start with this tool** before considering unaggregated data.

**Note**: Unaggregated data tools (`prepare_analytics_record_query` and `fetch_unaggregated_data`) are currently disabled to prevent conversation length errors. Use aggregated data tools only.

### Tool Categories Summary

| Category | Read-Only Tools | Modification Tools | Total |
|----------|----------------|-------------------|-------|
| Organization | 1 | 0 | 1 |
| Agents | 4 | 4 | 8 |
| End Users | 3 | 7 | 10 |
| Conversations | 9 | 11 | 20 |
| Custom Attributes | 2 | 2 | 4 |
| Tags | 3 | 4 | 7 |
| Teams | 4 | 4 | 8 |
| Queues | 5 | 3 | 8 |
| Knowledge Base | 3 | 4 | 7 |
| Settings | 4 | 0 | 4 |
| Analytics | 2 | 0 | 2 |
| **Total** | **40** | **39** | **79** |

### Important Notes

- **Modification Tools**: All modification tools (create, update, delete operations) modify data and require explicit user confirmation before execution.
- **API Key**: All tools automatically extract the API key from the Authorization header (for HTTP/SSE) or configuration (for subprocess).
- **ID Requirements**: Most tools require entity IDs (conversation_id, agent_id, etc.) which must be obtained first using the corresponding "list" or "fetch" tools.
- **Analytics Workflow**: Always start with `prepare_analytics_metric_query` to discover available metrics, then use `fetch_aggregated_data` for summary statistics.

## Local Testing

### Test 1: Direct Python Testing

Test the API wrapper directly:

```python
from dixa_api import DixaClient
import os

# Set API key
os.environ["DIXA_API_KEY"] = "your-api-key-here"

# Create client and test
client = DixaClient()
org_info = client.get_organization()
print(org_info)
```

### Test 2: Test Server Tools

```python
import os
os.environ["DIXA_API_KEY"] = "your-api-key-here"

from server import get_organization_info

# Test the tool
result = get_organization_info()
print(result)
```

### Test 3: Test Server as Subprocess

Create a test script `test_server.py`:

```python
import subprocess
import json
import sys

# Test with environment variable
env = os.environ.copy()
env["DIXA_API_KEY"] = "your-api-key-here"

result = subprocess.run(
    [sys.executable, "server.py"],
    env=env,
    capture_output=True,
    text=True
)
print(result.stdout)
print(result.stderr)
```

### Test 4: Test HTTP Server

1. Start the server:
```bash
python server.py --http 8000
```

2. In another terminal, test with curl:

```bash
# Test the MCP endpoint
curl http://localhost:8000/mcp
```

3. Or use a Python client:

```python
import requests

response = requests.get(
    "http://localhost:8000/mcp",
    headers={"Authorization": "Bearer your-api-key-here"}
)
print(response.json())
```

### Test 5: Test with MCP Inspector

You can use the MCP Inspector tool to test your server:

```bash
# Install MCP Inspector (if available)
npm install -g @modelcontextprotocol/inspector

# Test subprocess server
mcp-inspector python server.py

# Test HTTP server (after starting it)
mcp-inspector --url http://localhost:8000/mcp
```

## Project Structure

```
dixa-mcp-public/
├── server.py          # FastMCP server with tools
├── dixa_api.py        # Dixa API client wrapper
├── pyproject.toml     # Project dependencies
├── venv/              # Virtual environment (not in git)
└── README.md          # This file
```

## API Wrapper

The `DixaClient` class in `dixa_api.py` provides a clean interface to the Dixa API:

```python
from dixa_api import DixaClient

# Initialize with API key
client = DixaClient(api_key="your-key")

# Or use environment variable
client = DixaClient()  # Uses DIXA_API_KEY env var

# Get organization info
org_info = client.get_organization()
```

### Error Handling

The client provides detailed error messages:

- **HTTPError**: For HTTP 4xx/5xx errors with response details
- **RequestException**: For network/request errors
- **ValueError**: If API key is missing

## Troubleshooting

### ModuleNotFoundError: No module named 'fastmcp'

Make sure you've activated the virtual environment and installed dependencies:

```bash
source venv/bin/activate
pip install fastmcp requests
```

### API Key Not Found

Ensure your API key is provided through one of the supported methods:

**For Subprocess Transport (Local)**:
1. Environment variable: `export DIXA_API_KEY="your-key"` (set in Claude Desktop config `env` section)
2. Command-line: `python server.py --api-key your-key` (set in Claude Desktop config `args` section)

**For HTTP/SSE Transport (Remote)**:
1. Authorization header: Configure in Claude Desktop config using `--header "Authorization: Bearer your-key"` in the `mcp-remote` args
2. The server automatically extracts the API key from the Authorization header using FastMCP's `get_http_headers()` function

**Note**: For remote servers, environment variables are not passed by Claude Desktop, so you must use the Authorization header method.

### Server Won't Start

- Check that Python 3.8+ is installed: `python3 --version`
- Verify virtual environment is activated
- Check that all dependencies are installed: `pip list`
- Review error messages in the console

### Connection Issues (HTTP/SSE)

- Ensure the server is running: `python server.py --http 8000` (or `python server.py --http 8000 http` for HTTP transport)
- Check the URL in your client config matches the server URL (should end with `/mcp`)
- Verify the Authorization header is correctly formatted: `Authorization: Bearer your-api-key-here`
- For local HTTP servers, ensure `--allow-http` flag is included in `mcp-remote` args
- Verify firewall settings allow connections to the port
- Check server logs for authentication errors (look for `[get_organization_info]` messages)
- Ensure `npx` is installed and can run `mcp-remote`

## Development

### Adding New Tools

1. Add your tool function in `server.py`:

```python
@mcp.tool
def my_new_tool(param: str) -> str:
    """Tool description."""
    # Your implementation
    return result
```

2. Use `DixaClient` for API calls:

```python
from dixa_api import DixaClient

@mcp.tool
def my_tool() -> Dict[str, Any]:
    client = DixaClient()  # Uses configured API key
    # Make API calls
    return result
```

### Adding New API Endpoints

Extend `DixaClient` in `dixa_api.py`:

```python
def get_new_endpoint(self, param: str) -> Dict[str, Any]:
    """Get data from new endpoint."""
    url = f"{self.base_url}/new-endpoint"
    response = requests.get(url, headers=self.headers, params={"param": param})
    response.raise_for_status()
    return response.json()
```

## Security Notes

- **Never commit API keys** to version control
- Use environment variables or secure configuration management
- For production, use secure authentication methods
- Consider using secret management services for API keys

## License

This project uses the following dependencies and services:

### FastMCP

This project is built using [FastMCP](https://gofastmcp.com), a framework for building Model Context Protocol servers.

- **Website**: https://gofastmcp.com
- **License**: Please refer to the [FastMCP license](https://github.com/jlowin/fastmcp) for license information

### FastMCP Cloud

For remote deployments, this project can be hosted on [FastMCP Cloud](https://fastmcp.app).

- **Website**: https://fastmcp.app
- **Service**: FastMCP Cloud provides hosting for MCP servers

### Dixa API

This project integrates with the Dixa API to provide access to Dixa organization data and services.

- **API Documentation**: https://docs.dixa.io/docs/
- **License**: Please refer to the Dixa API documentation for API-specific licensing and terms

## Support

For issues and questions:
- Check the troubleshooting section
- Review [Dixa API documentation](https://docs.dixa.io/docs/)
- Review FastMCP documentation: https://gofastmcp.com
- Review MCP documentation: https://modelcontextprotocol.io

