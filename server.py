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

# Add Starlette middleware directly to the HTTP/SSE apps
# FastMCP middleware runs at MCP protocol level, not HTTP level, so we need HTTP-level middleware
def setup_http_middleware():
    """Setup Starlette middleware to extract Authorization header from HTTP requests."""
    try:
        from starlette.middleware.base import BaseHTTPMiddleware
        from starlette.requests import Request
        from starlette.responses import Response
        from typing import Callable, Awaitable
        import sys
        
        class AuthExtractionMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
                # Log that middleware is running
                print(f"[StarletteMiddleware] Processing request: {request.method} {request.url.path}", file=sys.stderr, flush=True)
                
                # Extract Authorization header from HTTP request
                auth_header = request.headers.get("Authorization", "")
                if auth_header:
                    # Remove "Bearer " prefix if present
                    token = auth_header.replace("Bearer ", "").strip()
                    if token:
                        # Store in context variable for use in tools
                        _client_api_key.set(token)
                        print(f"[StarletteMiddleware] ✓ Extracted API key from header: {token[:20]}...", file=sys.stderr, flush=True)
                        print(f"[StarletteMiddleware] Context var set, value: {_client_api_key.get()[:20] if _client_api_key.get() else 'None'}...", file=sys.stderr, flush=True)
                    else:
                        print(f"[StarletteMiddleware] Authorization header present but empty after processing", file=sys.stderr, flush=True)
                else:
                    # Debug: show all headers to see what we're getting
                    all_headers = dict(request.headers)
                    print(f"[StarletteMiddleware] ✗ No Authorization header. All headers: {list(all_headers.keys())}", file=sys.stderr, flush=True)
                    # Show a few key headers for debugging
                    for key in ['authorization', 'Authorization', 'x-authorization', 'X-Authorization']:
                        if key in all_headers:
                            print(f"[StarletteMiddleware] Found {key}: {all_headers[key][:20]}...", file=sys.stderr, flush=True)
                
                response = await call_next(request)
                
                # Verify context var is still set after call
                if _client_api_key.get():
                    print(f"[StarletteMiddleware] Context var still set after call: {_client_api_key.get()[:20]}...", file=sys.stderr, flush=True)
                else:
                    print(f"[StarletteMiddleware] Context var lost after call", file=sys.stderr, flush=True)
                
                return response
        
        # Try to add middleware to FastMCP's HTTP/SSE apps
        # These are created when the server starts, so we need to hook into them
        apps_added = []
        # Try HTTP app first (preferred), then SSE, then streamable HTTP
        for app_attr in ['http_app', 'sse_app', 'streamable_http_app']:
            if hasattr(mcp, app_attr):
                app = getattr(mcp, app_attr)
                if app and hasattr(app, 'add_middleware'):
                    app.add_middleware(AuthExtractionMiddleware)
                    apps_added.append(app_attr)
                    print(f"[StarletteMiddleware] Added middleware to {app_attr}", file=sys.stderr, flush=True)
        
        if not apps_added:
            print("[StarletteMiddleware] Could not find app to add middleware to", file=sys.stderr, flush=True)
            # Try to access through transport after it's created
            return False
        return True
    except Exception as e:
        import sys
        print(f"[StarletteMiddleware] Failed to setup: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False

# Try to setup immediately (might work if apps are already created)
setup_http_middleware()

# Also try FastMCP middleware as a fallback (though it might not have HTTP header access)
try:
    from fastmcp.server.middleware import Middleware, MiddlewareContext
    
    class AuthExtractionMiddleware(Middleware):
        """Middleware to extract Authorization header - fallback if HTTP middleware doesn't work."""
        
        async def on_call_tool(self, context: MiddlewareContext, call_next):
            """Try to extract Authorization header from context."""
            import sys
            # Try to get the Authorization header from the request
            auth_header = None
            
            # Debug: log what's available in context
            print(f"[FastMCPMiddleware] Context attributes: {dir(context)}", file=sys.stderr, flush=True)
            
            # Try different ways to access headers
            if hasattr(context, 'headers'):
                auth_header = context.headers.get("Authorization", "")
                print(f"[FastMCPMiddleware] Found headers attribute", file=sys.stderr, flush=True)
            elif hasattr(context, 'request'):
                request = context.request
                if hasattr(request, 'headers'):
                    auth_header = request.headers.get("Authorization", "")
                    print(f"[FastMCPMiddleware] Found request.headers", file=sys.stderr, flush=True)
            elif hasattr(context, 'scope'):
                scope = context.scope
                if isinstance(scope, dict) and 'headers' in scope:
                    headers = {k.decode(): v.decode() for k, v in scope['headers']}
                    auth_header = headers.get("authorization", headers.get("Authorization", ""))
                    print(f"[FastMCPMiddleware] Found scope.headers: {list(headers.keys())[:5]}", file=sys.stderr, flush=True)
            
            # Try to access the current ASGI scope from contextvars or task context
            try:
                import contextvars
                # Try to get the current request scope
                for var in contextvars.copy_context():
                    if hasattr(var, 'scope') or (isinstance(var, dict) and 'headers' in var):
                        scope = var if isinstance(var, dict) else getattr(var, 'scope', {})
                        if isinstance(scope, dict) and 'headers' in scope:
                            headers = {k.decode(): v.decode() if isinstance(v, bytes) else v 
                                     for k, v in scope['headers']}
                            if 'authorization' in headers or 'Authorization' in headers:
                                auth_header = headers.get("authorization") or headers.get("Authorization")
                                print(f"[FastMCPMiddleware] Found header in context var", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"[FastMCPMiddleware] Error accessing context vars: {e}", file=sys.stderr, flush=True)
            
            if auth_header:
                token = auth_header.replace("Bearer ", "").strip()
                if token:
                    _client_api_key.set(token)
                    print(f"[FastMCPMiddleware] ✓ Extracted API key: {token[:20]}...", file=sys.stderr, flush=True)
            else:
                print(f"[FastMCPMiddleware] ✗ No Authorization header found", file=sys.stderr, flush=True)
            
            return await call_next(context)
    
    # Add the middleware to FastMCP
    mcp.add_middleware(AuthExtractionMiddleware())
    import sys
    print("[FastMCP] Added auth extraction middleware (fallback)", file=sys.stderr, flush=True)
except ImportError:
    # FastMCP middleware might not be available in all versions
    import sys
    print("[FastMCP] FastMCP middleware not available", file=sys.stderr, flush=True)
except Exception as e:
    import sys
    print(f"[FastMCP] Error setting up FastMCP middleware: {e}", file=sys.stderr, flush=True)

# Monkey-patch the http_app and sse_app properties to add middleware when they're first accessed
# This way we can intercept app creation even inside run()
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Awaitable

class AuthExtractionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        print(f"[HTTPMiddleware] Processing: {request.method} {request.url.path}", file=sys.stderr, flush=True)
        auth_header = request.headers.get("Authorization", "")
        if auth_header:
            token = auth_header.replace("Bearer ", "").strip()
            if token:
                _client_api_key.set(token)
                print(f"[HTTPMiddleware] ✓ Set API key: {token[:20]}...", file=sys.stderr, flush=True)
        else:
            all_headers = dict(request.headers)
            print(f"[HTTPMiddleware] ✗ No Auth header. Keys: {list(all_headers.keys())[:10]}", file=sys.stderr, flush=True)
        
        response = await call_next(request)
        return response

# Store original property getters
_original_http_app = None
_original_sse_app = None
_original_streamable_http_app = None

# Monkey-patch property getters to add middleware when apps are accessed
if hasattr(type(mcp), 'http_app'):
    _original_http_app = type(mcp).http_app
    def http_app_with_middleware(self):
        app = _original_http_app.__get__(self, type(self))
        if app and hasattr(app, 'add_middleware'):
            # Check if middleware already added
            if not hasattr(app, '_auth_middleware_added'):
                try:
                    app.add_middleware(AuthExtractionMiddleware)
                    app._auth_middleware_added = True
                    print("[MonkeyPatch] Added middleware to http_app", file=sys.stderr, flush=True)
                except Exception as e:
                    print(f"[MonkeyPatch] Failed to add middleware to http_app: {e}", file=sys.stderr, flush=True)
        return app
    type(mcp).http_app = property(http_app_with_middleware)

if hasattr(type(mcp), 'sse_app'):
    _original_sse_app = type(mcp).sse_app
    def sse_app_with_middleware(self):
        app = _original_sse_app.__get__(self, type(self))
        if app and hasattr(app, 'add_middleware'):
            if not hasattr(app, '_auth_middleware_added'):
                try:
                    app.add_middleware(AuthExtractionMiddleware)
                    app._auth_middleware_added = True
                    print("[MonkeyPatch] Added middleware to sse_app", file=sys.stderr, flush=True)
                except Exception as e:
                    print(f"[MonkeyPatch] Failed to add middleware to sse_app: {e}", file=sys.stderr, flush=True)
        return app
    type(mcp).sse_app = property(sse_app_with_middleware)

if hasattr(type(mcp), 'streamable_http_app'):
    _original_streamable_http_app = type(mcp).streamable_http_app
    def streamable_http_app_with_middleware(self):
        app = _original_streamable_http_app.__get__(self, type(self))
        if app and hasattr(app, 'add_middleware'):
            if not hasattr(app, '_auth_middleware_added'):
                try:
                    app.add_middleware(AuthExtractionMiddleware)
                    app._auth_middleware_added = True
                    print("[MonkeyPatch] Added middleware to streamable_http_app", file=sys.stderr, flush=True)
                except Exception as e:
                    print(f"[MonkeyPatch] Failed to add middleware to streamable_http_app: {e}", file=sys.stderr, flush=True)
        return app
    type(mcp).streamable_http_app = property(streamable_http_app_with_middleware)

print("[MonkeyPatch] Set up property interceptors for app middleware injection", file=sys.stderr, flush=True)

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
async def get_organization_info() -> Dict[str, Any]:
    """
    Get organization information from the Dixa API.
    
    The API key is automatically extracted from:
    - Authorization header (for remote HTTP/SSE servers)
    - Command-line arguments (for local subprocess servers)
    - DIXA_API_KEY environment variable (fallback)
    
    Returns:
        Dictionary containing organization information from Dixa.
    """
    # Try to get headers from the HTTP request using FastMCP's built-in function
    api_key_from_header = None
    try:
        from fastmcp.server.dependencies import get_http_headers
        headers = get_http_headers()
        if headers:
            # Headers are typically lowercase in HTTP
            auth_header = headers.get("authorization") or headers.get("Authorization", "")
            if auth_header:
                # Remove "Bearer " prefix if present
                api_key_from_header = auth_header.replace("Bearer ", "").strip()
                print(f"[get_organization_info] ✓ Extracted API key from HTTP headers: {api_key_from_header[:20]}...", file=sys.stderr, flush=True)
    except ImportError:
        print("[get_organization_info] get_http_headers not available, trying fallback methods", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[get_organization_info] Error getting HTTP headers: {e}", file=sys.stderr, flush=True)
    
    # Priority: HTTP header > context var (from middleware) > command-line arg > env var
    final_api_key = (
        api_key_from_header or
        _client_api_key.get() or 
        _api_key or 
        os.getenv("DIXA_API_KEY")
    )
    
    # Debug: log which auth method was used
    if final_api_key:
        if api_key_from_header:
            auth_source = "http_header"
        elif _client_api_key.get():
            auth_source = "context_var"
        elif _api_key:
            auth_source = "cmdline"
        else:
            auth_source = "env"
        print(f"[get_organization_info] Using API key from: {auth_source}", file=sys.stderr, flush=True)
    else:
        print("[get_organization_info] No API key found in any source", file=sys.stderr, flush=True)
        print(f"[get_organization_info] HTTP headers available: {headers if 'headers' in locals() else 'N/A'}", file=sys.stderr, flush=True)
    
    if not final_api_key:
        raise ValueError(
            "API key is required but not found. "
            "For remote servers, ensure the Authorization header is set in your Claude Desktop config. "
            "For local servers, set DIXA_API_KEY environment variable or use --api-key command-line argument."
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
        # Try HTTP transport first (preferred), fallback to SSE if needed
        transport_type = sys.argv[3] if len(sys.argv) > 3 else "http"
        # The middleware will be added automatically by our monkey-patched run method
        mcp.run(transport=transport_type, host="0.0.0.0", port=port)
    else:
        # Run as subprocess (default for Claude Desktop)
        mcp.run()
