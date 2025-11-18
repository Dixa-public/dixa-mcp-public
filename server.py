import os
import sys
from fastmcp import FastMCP
from dixa_api import DixaClient
from typing import Optional, Dict, Any
from contextvars import ContextVar

# Context variable to store API key from client auth (for HTTP/SSE transport)
_client_api_key: ContextVar[Optional[str]] = ContextVar('client_api_key', default=None)

# Global variable to store API key from initialization (for subprocess transport)
_api_key: Optional[str] = None

# Check for API key in command line arguments (for auth config support)
# Format: python server.py --api-key YOUR_KEY
if len(sys.argv) > 1 and sys.argv[1] == "--api-key" and len(sys.argv) > 2:
    _api_key = sys.argv[2]
    # Remove the args so FastMCP doesn't see them
    sys.argv = [sys.argv[0]]

# For HTTP/SSE transport, we need to extract Authorization header from requests
mcp = FastMCP("Dixa MCP Server")

# Add middleware to extract Authorization header
# We'll try to access the app after FastMCP initializes it
def add_auth_middleware():
    """Add middleware to extract Authorization header from requests."""
    try:
        from starlette.middleware.base import BaseHTTPMiddleware
        from starlette.requests import Request
        from starlette.responses import Response
        from typing import Callable, Awaitable
        
        class AuthExtractionMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
                # Extract Authorization header
                auth_header = request.headers.get("Authorization", "")
                if auth_header:
                    # Remove "Bearer " prefix if present
                    token = auth_header.replace("Bearer ", "").strip()
                    if token:
                        # Store in context variable for use in tools
                        _client_api_key.set(token)
                
                response = await call_next(request)
                return response
        
        # Try to find and access the FastMCP app
        # FastMCP may expose it through different attributes
        app = None
        for attr in ['_app', 'app', '_server', 'server']:
            if hasattr(mcp, attr):
                candidate = getattr(mcp, attr)
                # Check if it's an ASGI app (has __call__ method)
                if hasattr(candidate, '__call__'):
                    app = candidate
                    break
        
        # Also try to get it from transport
        if app is None:
            transport = getattr(mcp, '_transport', None) or getattr(mcp, 'transport', None)
            if transport:
                for attr in ['_app', 'app', '_server', 'server']:
                    if hasattr(transport, attr):
                        candidate = getattr(transport, attr)
                        if hasattr(candidate, '__call__'):
                            app = candidate
                            break
        
        if app:
            # Add middleware to the app
            app.add_middleware(AuthExtractionMiddleware)
    except Exception as e:
        # If middleware setup fails, tools will fall back to other auth methods
        # This is expected for subprocess transport
        pass

# Try to setup middleware immediately (for FastMCP Cloud)
# For local HTTP servers, it will be set up in the __main__ block
add_auth_middleware()

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
        api_key: Dixa API key. For remote servers (HTTP/SSE), this should be provided.
                 For local servers, can use DIXA_API_KEY environment variable or command-line args.
    
    Returns:
        Dictionary containing organization information from Dixa.
    
    Note:
        For remote MCP servers deployed on FastMCP Cloud, you must provide the api_key parameter
        or set DIXA_API_KEY as an environment variable in FastMCP Cloud settings.
    """
    # Priority: provided api_key > client auth token from Authorization header > command-line arg > env var
    # For remote servers, the Authorization header should contain the API key
    final_api_key = (
        api_key or 
        _client_api_key.get() or 
        _api_key or 
        os.getenv("DIXA_API_KEY")
    )
    
    if not final_api_key:
        raise ValueError(
            "API key is required. Please provide it as the 'api_key' parameter, "
            "or set DIXA_API_KEY environment variable."
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
        # Setup middleware before running (app will be initialized by mcp.run)
        # We'll try again after run() in case the app wasn't accessible before
        mcp.run(transport="sse", host="0.0.0.0", port=port)
        # Try to setup middleware again after app initialization
        add_auth_middleware()
    else:
        # Run as subprocess (default for Claude Desktop)
        mcp.run()
