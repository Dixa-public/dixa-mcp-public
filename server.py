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
# We'll wrap the ASGI app to extract the Authorization header
def create_auth_middleware_wrapper(original_app):
    """Wrap the ASGI app with middleware to extract Authorization header."""
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
                    # Debug: log that we extracted the token (first 20 chars only for security)
                    import sys
                    print(f"[AuthMiddleware] Extracted API key: {token[:20]}...", file=sys.stderr, flush=True)
            
            response = await call_next(request)
            return response
    
    # Wrap the original app
    return AuthExtractionMiddleware(original_app)

# Monkey-patch FastMCP's run method to wrap the app with our middleware
_original_run = mcp.run
def run_with_auth(*args, **kwargs):
    """Wrap mcp.run to add auth middleware to the app."""
    # Check if this is HTTP/SSE transport
    transport = kwargs.get('transport') or (args[0] if args else None)
    is_http = transport in ('sse', 'http', 'http-sse')
    
    if is_http:
        # Store original run
        result = _original_run(*args, **kwargs)
        
        # Try to find and wrap the app
        try:
            # FastMCP might store the app in different places
            for obj in [mcp, getattr(mcp, '_transport', None), getattr(mcp, 'transport', None)]:
                if obj is None:
                    continue
                    
                # Try different attribute names
                for attr_name in ['_app', 'app', '_asgi_app', 'asgi_app', '_server', 'server']:
                    if hasattr(obj, attr_name):
                        app = getattr(obj, attr_name)
                        # Check if it's an ASGI app
                        if hasattr(app, '__call__') and not isinstance(app, type):
                            # Wrap it with our middleware
                            wrapped = create_auth_middleware_wrapper(app)
                            setattr(obj, attr_name, wrapped)
                            break
        except Exception:
            pass
        
        return result
    else:
        # For subprocess, just run normally
        return _original_run(*args, **kwargs)

# Replace the run method
mcp.run = run_with_auth

# For FastMCP Cloud, try to setup middleware immediately after module load
# FastMCP Cloud might initialize the app before mcp.run() is called
def try_setup_middleware_immediately():
    """Try to setup middleware immediately for FastMCP Cloud."""
    try:
        # Wait a bit for FastMCP to initialize
        import time
        time.sleep(0.1)
        
        # Try to find the app
        for obj in [mcp, getattr(mcp, '_transport', None), getattr(mcp, 'transport', None)]:
            if obj is None:
                continue
                
            for attr_name in ['_app', 'app', '_asgi_app', 'asgi_app', '_server', 'server']:
                if hasattr(obj, attr_name):
                    app = getattr(obj, attr_name)
                    if hasattr(app, '__call__') and not isinstance(app, type):
                        # Wrap it
                        wrapped = create_auth_middleware_wrapper(app)
                        setattr(obj, attr_name, wrapped)
                        import sys
                        print("[FastMCP Cloud] Successfully added auth middleware", file=sys.stderr, flush=True)
                        return
    except Exception as e:
        import sys
        print(f"[FastMCP Cloud] Could not setup middleware immediately: {e}", file=sys.stderr, flush=True)

# Try immediately (for FastMCP Cloud)
try_setup_middleware_immediately()

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
    
    # Debug: log which auth method was used
    import sys
    if final_api_key:
        auth_source = "parameter" if api_key else ("header" if _client_api_key.get() else ("cmdline" if _api_key else "env"))
        print(f"[get_organization_info] Using API key from: {auth_source}", file=sys.stderr, flush=True)
    else:
        print("[get_organization_info] No API key found in any source", file=sys.stderr, flush=True)
    
    if not final_api_key:
        raise ValueError(
            "API key is required. Please provide it as the 'api_key' parameter, "
            "or set DIXA_API_KEY environment variable. "
            f"(Context var: {_client_api_key.get() is not None})"
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
        # The middleware will be added automatically by our monkey-patched run method
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        # Run as subprocess (default for Claude Desktop)
        mcp.run()
