import os
import sys
from fastmcp import FastMCP
from typing import Dict, Any

# Import shared variables - these are the same instances used in tools.base
from tools.shared import _client_api_key, _api_key

# Check for API key in command line arguments (for auth config support)
# Format: python server.py --api-key YOUR_KEY
if len(sys.argv) > 1 and sys.argv[1] == "--api-key" and len(sys.argv) > 2:
    # Set the shared _api_key variable
    import tools.shared
    tools.shared._api_key = sys.argv[2]
    # Remove the args so FastMCP doesn't see them
    sys.argv = [sys.argv[0]]

# For HTTP/SSE transport, we need to extract Authorization header from requests
mcp = FastMCP(
    "Dixa MCP Server",
    instructions="""
        This MCP server provides access to the Dixa API, allowing you to interact with your Dixa organization.
        
        About Dixa:
        Dixa is a customer service platform that enables organizations to manage customer interactions across multiple channels (email, chat, phone, SMS, social media, etc.) in a unified conversational interface. Dixa helps customer service teams deliver personalized, efficient support by centralizing all customer conversations, automating workflows, and providing tools for agents to resolve issues effectively.
        
        Key Terms and Definitions:
        - End Users (Customers): The customers or end users who contact your organization for support. They are the people who initiate conversations through various channels (email, chat, phone, etc.). End users are managed separately from agents and have their own profiles, custom attributes, and conversation history.
        - Agents (Customer Service Agents): Customer service representatives who handle and resolve customer inquiries. Agents work within the Dixa platform to respond to conversations, manage customer relationships, and provide support across all channels. Agents can be assigned to conversations, work in teams, and have presence status indicating their availability.
        - Admins (Administrators): Agents with administrative privileges who manage the Dixa organization. Admins configure settings, manage agents and teams, set up queues, configure business hours, manage contact endpoints, and oversee analytics and performance. In the Dixa API, both agents and admins are represented under the "agents" entity.
        
        Available tool categories:
        - Organization: Get organization information
        - Agents: Manage agents/admins (get, list, create, update, patch, manage presence and teams)
        - End Users: Manage end users/customers (get, list, create, update, patch, delete, anonymize, list conversations)
        - Settings: Manage contact endpoints, business hours schedules and status
        - Conversations: Manage conversations (get, create, add notes, tag, claim, close, anonymize, search, etc.)
        - Custom Attributes: Manage custom attributes for conversations and end users
        - Analytics: Get analytics data (metrics, records, filter values) - requires discovering available metrics/records first
        
        Important notes:
        - All modification endpoints (create, update, patch, delete) require explicit user confirmation before execution
        - The API key is automatically extracted from the Authorization header or configuration
        - Read-only endpoints (get, list) do not require confirmation
        - Anonymization endpoints are typically irreversible and used for GDPR compliance
        
        Common Workflow Patterns:
        Many tools require IDs from other entities, which must be obtained first. Follow these patterns:
        
        1. Tag Operations:
           - To tag a conversation: First use `list_tags` to list all tags and find the tag ID by name, or use `add_tag` if the tag doesn't exist yet. Then use `tag_conversation` with the conversation_id and tag_id.
           - To remove a tag: Use `list_conversation_tags` to see tags on a conversation, or `list_tags` to find the tag ID, then use `remove_tag_from_conversation`.
           - To activate/deactivate/delete a tag: First use `list_tags` to find the tag ID, then use `activate_tag`, `deactivate_tag`, or `remove_tag`.
        
        2. Conversation Operations:
           - Most conversation operations require a conversation_id. First use `fetch_conversation_by_id` (if you know the ID) or `search_conversations` to find conversations, then use the conversation_id in subsequent operations.
           - To create a conversation: You need a requester_id (end user). Use `list_end_users` to find an existing end user, or `add_end_user` if they don't exist. For outbound messages, you also need an agent_id from `list_agents`.
           - To claim a conversation: You need both conversation_id (from search/fetch) and agent_id (from `list_agents`). Use `assign_conversation_to_agent`.
           - To link conversations: You need both conversation_id and parent_conversation_id, both obtained from `fetch_conversation_by_id` or search. Use `link_conversation_to_parent`.
        
        3. Agent Assignment Operations:
           - To assign agents to teams: First use `list_agents` to find agent IDs, then use `list_teams` to find the team_id, then use `add_agents_to_team`.
           - To assign agents to queues: First use `list_agents` to find agent IDs, then use `list_queues` to find the queue_id, then use `assign_agents_to_queue`.
           - To claim a conversation: First use `list_agents` to find the agent_id, then use `assign_conversation_to_agent`.
        
        4. Team Operations:
           - Most team operations require a team_id. First use `list_teams` to list all teams and find the team ID, then use it in operations like `list_team_agents`, `add_agents_to_team`, or `remove_agents_from_team`.
        
        5. Queue Operations:
           - Most queue operations require a queue_id. First use `list_queues` to list all queues and find the queue ID, then use it in operations like `fetch_queue_by_id`, `list_queue_agents`, `assign_agents_to_queue`, etc.
        
        6. Knowledge Base Operations:
           - To create an article in a category: First use `list_knowledge_categories` to find the category_id (optional), then use `add_knowledge_article`.
           - To update an article: First use `list_knowledge_articles` to find the article_id, then use `modify_knowledge_article`.
        
        7. Custom Attributes Operations:
           - To update custom attributes: First use `list_custom_attributes` to get the list of custom attribute definitions and their IDs. The custom_attributes parameter requires a dictionary mapping custom attribute IDs (UUIDs) to values. Then use `update_conversation_custom_attributes` or `update_end_user_custom_attributes`.
        
        8. Analytics Operations:
           - 🚨 MANDATORY WORKFLOW: Use aggregated data for all analytics queries. Aggregated data provides summary statistics (counts, percentages, averages) that answer most analytics questions.
           - Step 1 - Aggregated Data (MANDATORY FIRST): First call `prepare_analytics_metric_query` without metric_id to discover available metrics. Then call `prepare_analytics_metric_query` with a metric_id to get all information needed (filters, aggregations, filter values) in one call. Finally, use `fetch_aggregated_data` to fetch the aggregated metric data. Review these results first.
           - Understanding Aggregation Results: For nested/pre-aggregated metrics (e.g., "conversation_assignments_per_agent"), data is first grouped (e.g., by agent) then aggregated. "Count" refers to the number of groups/entries matching filters, NOT the total count of underlying items. "Sum" refers to the total sum across all groups. Example: Count=22 and Sum=1171 for "conversation_assignments_per_agent" means 22 agents have assignments (Count = number of agent groups) and 1171 total assignments across those agents (Sum = total assignments). To get per-agent details, you would need separate calls filtering by individual agent_id for each agent.
           - NOTE: Unaggregated data tools are currently disabled to prevent conversation length errors. Use aggregated data only.
           # NOTE: Unaggregated data tools are commented out to prevent conversation length errors
           # - Step 2 - Unaggregated Data (ONLY IF NEEDED): Only if aggregated data is insufficient, then proceed to unaggregated records. First call `prepare_analytics_record_query` without record_id to discover available records. Then call `prepare_analytics_record_query` with a record_id to get all information needed (filters, filter values) in one call. Finally, use `fetch_unaggregated_data` to fetch the detailed record data.
           - Important: Analytics endpoints require a discovery workflow. Always start by calling the prepare tools without IDs to find available metrics/records, then call them again with specific IDs to get all information, and finally query the data.
           # - Pagination for unaggregated data: When using `fetch_unaggregated_data`, you MUST collect ALL available data by paginating through all pages. Use page_limit of 100-300 (maximum 300) for the first request. Check if the response contains a "pageKey" field - if it does, make another call with the same payload but using page_key (page_limit not needed). Continue this process until no "pageKey" is returned, indicating you've collected all available data. Always combine data from all pages for complete analysis.
           # - Context Management for Large Responses: When processing large unaggregated data responses (especially with multiple pages), you MUST optimize context usage:
           #   * Extract only relevant information based on the query context - don't store everything
           #   * Summarize large datasets when possible (e.g., "Found 500 records with average value X" instead of storing all 500 records)
           #   * Store only essential fields needed to answer the question (IDs, timestamps, key values)
           #   * Ignore verbose metadata like "_type" fields and nested structures unless specifically needed
           #   * Focus on field "value" and "name" properties which contain the actual data
           #   * Consider using aggregated data summaries when available instead of storing all unaggregated records
           #   * Let the user's question guide what to extract - if they ask for a count, store the count, not all records
           #   * The full response data is always available in tool responses, so you don't need to store everything in context
        
        General Pattern: When a tool requires an ID parameter (tag_id, conversation_id, agent_id, team_id, queue_id, etc.), you must first use the corresponding "list" or "fetch" tool to find that ID. Always check if the entity exists before trying to use it, or add it first if it doesn't exist.
    """
)

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

# Import and register tools from the tools package
from tools.organization import fetch_organization_details
from tools.agents import fetch_agent_by_id, list_agents, list_agents_presence, list_agent_teams, add_agent, modify_agent_partial, update_agent_full, set_agent_working_channel
from tools.settings import list_contact_endpoints, fetch_contact_endpoint_by_id, check_business_hours_status, list_business_hours_schedules
from tools.conversations import fetch_conversation_by_id, list_conversation_flows, list_conversation_activity_log, list_conversation_notes, list_linked_conversations, list_conversation_messages, list_organization_activity_log, list_conversation_ratings, search_conversations, start_conversation, import_conversations, add_conversation_note, add_conversation_notes_bulk, anonymize_conversation, anonymize_conversation_message, tag_conversation_bulk, assign_conversation_to_agent, close_conversation, link_conversation_to_parent, set_conversation_followup_status, reopen_conversation, tag_conversation, remove_tag_from_conversation
from tools.custom_attributes import fetch_custom_attribute_by_id, list_custom_attributes, update_conversation_custom_attributes, update_end_user_custom_attributes
from tools.users import list_end_users, fetch_end_user_by_id, add_end_user, add_end_users_bulk, modify_end_user_partial, modify_end_users_bulk, update_end_user_full, update_end_users_bulk, list_end_user_conversations, anonymize_end_user
from tools.knowledge import list_knowledge_articles, fetch_knowledge_article_by_id, add_knowledge_article, modify_knowledge_article, remove_knowledge_article, list_knowledge_categories, add_knowledge_category
from tools.queues import list_queues, fetch_queue_by_id, check_queue_availability, check_conversation_queue_position, list_queue_agents, add_queue, assign_agents_to_queue, remove_agents_from_queue
from tools.tags import list_tags, fetch_tag_by_id, list_conversation_tags, add_tag, activate_tag, deactivate_tag, remove_tag
from tools.teams import list_teams, fetch_team_by_id, list_team_agents, list_team_presence, add_team, add_agents_to_team, remove_agents_from_team, remove_team
from tools.analytics import fetch_aggregated_data, prepare_analytics_metric_query, prepare_analytics_record_query
# NOTE: fetch_unaggregated_data is commented out to prevent conversation length errors
# from tools.analytics import fetch_unaggregated_data

# Register tools with FastMCP
mcp.tool(fetch_organization_details)
mcp.tool(fetch_agent_by_id)
mcp.tool(list_agents)
mcp.tool(list_agents_presence)
mcp.tool(list_agent_teams)
mcp.tool(add_agent)
mcp.tool(modify_agent_partial)
mcp.tool(update_agent_full)
mcp.tool(set_agent_working_channel)
mcp.tool(check_business_hours_status)
mcp.tool(list_business_hours_schedules)
mcp.tool(list_contact_endpoints)
mcp.tool(fetch_contact_endpoint_by_id)
mcp.tool(fetch_conversation_by_id)
mcp.tool(list_conversation_flows)
mcp.tool(list_conversation_activity_log)
mcp.tool(list_conversation_notes)
mcp.tool(list_linked_conversations)
mcp.tool(list_conversation_messages)
mcp.tool(list_organization_activity_log)
mcp.tool(list_conversation_ratings)
mcp.tool(search_conversations)
mcp.tool(start_conversation)
mcp.tool(import_conversations)
mcp.tool(add_conversation_note)
mcp.tool(add_conversation_notes_bulk)
mcp.tool(anonymize_conversation)
mcp.tool(anonymize_conversation_message)
mcp.tool(update_conversation_custom_attributes)
mcp.tool(tag_conversation_bulk)
mcp.tool(assign_conversation_to_agent)
mcp.tool(close_conversation)
mcp.tool(link_conversation_to_parent)
mcp.tool(set_conversation_followup_status)
mcp.tool(reopen_conversation)
mcp.tool(tag_conversation)
mcp.tool(remove_tag_from_conversation)
mcp.tool(fetch_custom_attribute_by_id)
mcp.tool(list_custom_attributes)
mcp.tool(update_end_user_custom_attributes)
mcp.tool(list_end_users)
mcp.tool(fetch_end_user_by_id)
mcp.tool(add_end_user)
mcp.tool(add_end_users_bulk)
mcp.tool(modify_end_user_partial)
mcp.tool(modify_end_users_bulk)
mcp.tool(update_end_user_full)
mcp.tool(update_end_users_bulk)
mcp.tool(list_end_user_conversations)
mcp.tool(anonymize_end_user)
mcp.tool(list_knowledge_articles)
mcp.tool(fetch_knowledge_article_by_id)
mcp.tool(add_knowledge_article)
mcp.tool(modify_knowledge_article)
mcp.tool(remove_knowledge_article)
mcp.tool(list_knowledge_categories)
mcp.tool(add_knowledge_category)
mcp.tool(list_queues)
mcp.tool(fetch_queue_by_id)
mcp.tool(check_queue_availability)
mcp.tool(check_conversation_queue_position)
mcp.tool(list_queue_agents)
mcp.tool(add_queue)
mcp.tool(assign_agents_to_queue)
mcp.tool(remove_agents_from_queue)
mcp.tool(list_tags)
mcp.tool(fetch_tag_by_id)
mcp.tool(list_conversation_tags)
mcp.tool(add_tag)
mcp.tool(activate_tag)
mcp.tool(deactivate_tag)
mcp.tool(remove_tag)
mcp.tool(list_teams)
mcp.tool(fetch_team_by_id)
mcp.tool(list_team_agents)
mcp.tool(list_team_presence)
mcp.tool(add_team)
mcp.tool(add_agents_to_team)
mcp.tool(remove_agents_from_team)
mcp.tool(remove_team)
mcp.tool(prepare_analytics_metric_query)
mcp.tool(fetch_aggregated_data)
mcp.tool(prepare_analytics_record_query)
# NOTE: fetch_unaggregated_data is commented out to prevent conversation length errors
# mcp.tool(fetch_unaggregated_data)


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
