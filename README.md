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
git clone <repository-url>
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

## Configuration

The server supports multiple authentication methods and transport options. Choose the setup that best fits your use case.

### Authentication Methods

The server supports API key authentication through multiple methods (in priority order):

1. **HTTP Authorization Header**: Automatically extracted from `Authorization: Bearer ...` header (for HTTP/SSE transport)
2. **Command-Line Argument**: Pass via `--api-key` flag (for subprocess transport)
3. **Environment Variable**: Set `DIXA_API_KEY` environment variable

**Note**: For remote HTTP/SSE servers, the API key is automatically extracted from the Authorization header sent by `mcp-remote`. You don't need to pass it as a tool parameter.

### Transport Options

#### Option 1: Subprocess Transport (Claude Desktop)

This is the default transport for Claude Desktop integration.

**Configuration File**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

##### Method A: Environment Variable (Recommended)

```json
{
    "mcpServers": {
        "dixa-local": {
            "command": "/path/to/venv/bin/python",
            "args": ["/path/to/dixa-mcp-public/server.py"],
            "env": {
                "DIXA_API_KEY": "your-dixa-api-key-here"
            }
        }
    }
}
```

##### Method B: Command-Line Arguments

```json
{
    "mcpServers": {
        "dixa-local": {
            "command": "/path/to/venv/bin/python",
            "args": [
                "/path/to/dixa-mcp-public/server.py",
                "--api-key",
                "your-dixa-api-key-here"
            ]
        }
    }
}
```

**Note**: Replace `/path/to/venv/bin/python` and `/path/to/dixa-mcp-public/server.py` with your actual paths.

#### Option 2: HTTP/SSE Transport (Remote Servers)

For remote access or when you want to use Bearer token authentication via HTTP headers.

##### Step 1: Start the HTTP Server

```bash
cd dixa-mcp-public
source venv/bin/activate
python server.py --http 8000
```

The server will start on `http://localhost:8000/mcp` (or your specified port).

For remote servers, use:
```bash
python server.py --http 8000 http
```

##### Step 2: Configure Claude Desktop

Claude Desktop uses `mcp-remote` to connect to remote MCP servers. Configure it in your `claude_desktop_config.json`:

**For Local Testing**:

```json
{
    "mcpServers": {
        "dixa-remote": {
            "command": "npx",
            "args": [
                "mcp-remote",
                "http://localhost:8000/mcp",
                "--header",
                "Authorization: Bearer your-dixa-api-key-here",
                "--allow-http"
            ]
        }
    }
}
```

**For Remote Servers** (e.g., FastMCP Cloud):

```json
{
    "mcpServers": {
        "dixa-remote": {
            "command": "npx",
            "args": [
                "mcp-remote",
                "https://your-server.fastmcp.app/mcp",
                "--header",
                "Authorization: Bearer your-dixa-api-key-here"
            ]
        }
    }
}
```

**Important Notes**:
- The `--header` flag passes the Authorization header to the server
- The `--allow-http` flag is required for local HTTP servers (not needed for HTTPS)
- The API key is automatically extracted from the Authorization header by the server
- Replace `your-dixa-api-key-here` with your actual Dixa API key
- For remote servers, replace the URL with your deployed server's URL

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

### `get_organization_info`

Retrieves organization information from the Dixa API.

**Parameters**: None (API key is automatically extracted from the Authorization header or configuration)

**Returns**: Dictionary containing organization information.

**Example Usage**:
```python
# API key is automatically extracted from:
# - Authorization header (for remote HTTP/SSE servers)
# - Command-line arguments (for local subprocess servers)
# - DIXA_API_KEY environment variable (fallback)
result = get_organization_info()
```

**Note**: For remote servers, ensure the Authorization header is configured in your Claude Desktop config as shown in the Configuration section.

### `greet`

A simple greeting tool for testing.

**Parameters**:
- `name` (required): Name to greet.

**Returns**: Greeting message.

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

[Add your license here]

## Support

For issues and questions:
- Check the troubleshooting section
- Review FastMCP documentation: https://gofastmcp.com
- Review MCP documentation: https://modelcontextprotocol.io

