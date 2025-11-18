import os
import sys
from fastmcp import FastMCP
from dixa_api import DixaClient
from typing import Optional, Dict, Any
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Context variable to store API key from client auth (for HTTP/SSE transport)
_client_api_key: ContextVar[Optional[str]] = ContextVar('client_api_key', default=None)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to extract Authorization header and store in context."""
    
    async def dispatch(self, request: Request, call_next):
        # Extract Authorization header
        auth_header = request.headers.get("Authorization", "")
        if auth_header:
            # Remove "Bearer " prefix if present
            token = auth_header.replace("Bearer ", "").strip()
            if token:
                _client_api_key.set(token)
        
        response = await call_next(request)
        return response

# Global variable to store API key from initialization (for subprocess transport)
_api_key: Optional[str] = None

# Check for API key in command line arguments (for auth config support)
# Format: python server.py --api-key YOUR_KEY
if len(sys.argv) > 1 and sys.argv[1] == "--api-key" and len(sys.argv) > 2:
    _api_key = sys.argv[2]
    # Remove the args so FastMCP doesn't see them
    sys.argv = [sys.argv[0]]

# For HTTP/SSE transport, we can use middleware to extract auth token
# FastMCP will handle this automatically if we configure it properly
mcp = FastMCP("Dixa MCP Server")

# Add middleware to extract Authorization header for HTTP/SSE transport
# This allows the API key to be passed from the client and used for Dixa API calls
mcp.add_middleware(AuthMiddleware)

# You can also add instructions for how to interact with the server
mcp_with_instructions = FastMCP(
    name="HelpfulAssistant",
    instructions="""
        This server provides insights into your Dixa organization.
    """,
)

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool
def get_organization_info(api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Get organization information from the Dixa API.
    
    Args:
        api_key: Optional API key. If not provided, uses API key from client auth (HTTP/SSE), 
                command-line args, or DIXA_API_KEY environment variable.
    
    Returns:
        Dictionary containing organization information from Dixa.
    """
    # Priority: provided api_key > client auth token (HTTP/SSE) > command-line arg > env var
    final_api_key = (
        api_key or 
        _client_api_key.get() or 
        _api_key or 
        os.getenv("DIXA_API_KEY")
    )
    client = DixaClient(api_key=final_api_key)
    return client.get_organization()


if __name__ == "__main__":
    # For HTTP/SSE transport, use mcp.run() with transport="sse"
    # For subprocess transport (default), just use mcp.run()
    # You can also specify host and port for HTTP server
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # Run as HTTP server on port 8000 (default)
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        # Run as subprocess (default for Claude Desktop)
        mcp.run()