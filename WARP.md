# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This is a Model Context Protocol (MCP) server that provides access to the Dixa API. It's built using FastMCP and supports multiple transport methods (subprocess and HTTP/SSE) with flexible authentication options.

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
# OR
pip install fastmcp requests
```

### Running the Server
```bash
# Subprocess mode (default, for Claude Desktop)
source .venv/bin/activate
python server.py

# HTTP/SSE mode (for remote access)
python server.py --http 8000

# With command-line API key
python server.py --api-key YOUR_KEY
```

### Testing
```bash
# Test the Dixa API client directly
python -c "from dixa_api import DixaClient; import os; os.environ['DIXA_API_KEY']='key'; client = DixaClient(); print(client.get_organization())"

# Test HTTP server (after starting it)
curl http://localhost:8000/mcp

# Test with authentication
curl -H "Authorization: Bearer YOUR_KEY" http://localhost:8000/mcp
```

### Linting and Type Checking
This project does not currently have configured linting or type checking. When adding these, update this section.

## Architecture

### Core Components

**server.py** - FastMCP server entry point
- Defines MCP tools (`greet`, `get_organization_info`)
- Handles authentication priority: tool parameter > client auth token (HTTP/SSE) > command-line arg > environment variable
- Supports two transport modes controlled by command-line args:
  - Subprocess (default): `mcp.run()` - for Claude Desktop integration
  - HTTP/SSE: `mcp.run(transport="sse", host="0.0.0.0", port=port)` - for remote access

**dixa_api.py** - Dixa API client wrapper
- `DixaClient` class provides abstracted access to Dixa API endpoints
- Base URL: `https://dev.dixa.io/v1`
- Authentication via Bearer token in headers
- Comprehensive error handling with detailed HTTP error messages

### Authentication Flow

The server implements a cascading authentication strategy:

1. **Tool parameter**: Explicit `api_key` passed to tool functions
2. **Client auth token**: Extracted from HTTP/SSE transport authentication (Bearer token)
3. **Command-line argument**: `--api-key` flag when starting server
4. **Environment variable**: `DIXA_API_KEY`

This allows flexibility for different deployment scenarios (local development, Claude Desktop, remote HTTP server).

### Transport Architecture

**Subprocess Transport**: 
- Uses stdin/stdout for JSON-RPC communication
- Configured in Claude Desktop's `claude_desktop_config.json`
- API key provided via environment variables or command-line args in config

**HTTP/SSE Transport**:
- Runs HTTP server with Server-Sent Events for streaming
- Authentication via Bearer token in Authorization header
- Supports remote access and multiple concurrent clients

## Adding New Features

### Adding a New Tool

Add tools to `server.py`:

```python
@mcp.tool
def my_new_tool(param: str) -> Dict[str, Any]:
    """Tool description for AI assistants."""
    # Use DixaClient for API calls
    client = DixaClient()  # Automatically uses configured API key
    # Implementation
    return result
```

### Adding a New Dixa API Endpoint

Extend `DixaClient` in `dixa_api.py`:

```python
def get_new_endpoint(self, param: str) -> Dict[str, Any]:
    """Get data from new endpoint."""
    url = f"{self.base_url}/new-endpoint"
    response = requests.get(url, headers=self.headers, params={"param": param})
    response.raise_for_status()
    return response.json()
```

### Authentication Considerations

When adding tools that require authentication:
- Accept optional `api_key` parameter for flexibility
- Use the authentication priority chain from `get_organization_info` as a template
- Always use `DixaClient` for API calls to centralize authentication logic

## Key Configuration Files

- **pyproject.toml**: Python dependencies (fastmcp, requests)
- **server.py**: Parses `--http` and `--api-key` command-line arguments
- **Claude Desktop config** (external): `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

## Important Notes

- Never commit API keys - use environment variables or secure configuration
- Virtual environment is `.venv` (not `venv`) - this is the active one
- The `venv/` directory also exists but appears to be a duplicate - use `.venv` for consistency
- Python 3.8+ is required
- When modifying authentication, update all four priority levels in the chain
- FastMCP automatically handles JSON-RPC protocol details
