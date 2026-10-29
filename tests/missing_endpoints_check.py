"""Exercise added and corrected endpoints through MCP and real HTTP encoding."""
import importlib
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from urllib.parse import urlsplit, parse_qs

import requests
from fastmcp import Client
from fastmcp.exceptions import ToolError
from dixa_api import DixaClient


AGENT = "00000000-0000-4000-8000-000000000001"
USER = "00000000-0000-4000-8000-000000000002"
WEBHOOK = "00000000-0000-4000-8000-000000000003"
CURSOR = "opaque+/=:cursor"
CONTENT = {"_type": "Text", "value": "Approved test message"}
MESSAGE = {"_type": "Outbound", "content": CONTENT, "agentId": AGENT,
           "cc": [USER], "bcc": [], "attachments": [{"url": "https://example.com/test.pdf", "prettyName": "test.pdf"}]}
OFFER = {"userId": USER, "agentId": AGENT, "ratingType": "Csat"}
RESULT = {"ratingResult": {"_type": "Csat", "value": 5}, "comment": "Customer-provided", "userId": None}
FILTERS = {"Conversation": {"_type": "CombinedFilters", "strategy": "All", "conditions": [
    {"_type": "IsOneOf", "field": "QueueId", "values": ["queue-1"]}]}}
SUBSCRIPTION = {"name": "Test", "url": "https://example.com/webhook", "authorization": {"_type": "NoAuth"},
                "customHeaders": {}, "events": ["ConversationCreated"], "enabled": False, "filters": FILTERS}

# Independent documented wire expectations, rather than deriving from client code.
CASES = [
    ("agents.add_agents_bulk", {"agents": [{"displayName": "Test", "email": "test@example.com"}]}, "POST", "/agents/bulk", {"data": [{"displayName": "Test", "email": "test@example.com"}]}),
    ("agents.update_agents_bulk", {"agents": [{"id": AGENT, "displayName": "Updated", "additionalEmails": []}]}, "PUT", "/agents", [{"id": AGENT, "displayName": "Updated", "additionalEmails": []}]),
    ("agents.modify_agents_bulk", {"agents": [{"id": AGENT, "middleNames": []}]}, "PATCH", "/agents", [{"id": AGENT, "middleNames": []}]),
    ("agents.fetch_agent_presence", {"agent_id": AGENT}, "GET", f"/agents/{AGENT}/presence", None),
    ("agents.remove_agent", {"agent_id": AGENT}, "DELETE", f"/agents/{AGENT}", None),
    ("ai_agents.list_ai_agents", {}, "GET", "/ai-agents", None),
    ("conversations.add_conversation_message", {"conversation_id": 42, "message": MESSAGE}, "POST", "/conversations/42/messages", MESSAGE),
    ("conversations.create_conversation_rating_offer", {"conversation_id": 42, "offer": OFFER}, "POST", "/conversations/42/ratings/offer", OFFER),
    ("conversations.submit_conversation_rating_result", {"conversation_id": 42, "rating_id": "offer-1", "result": RESULT}, "POST", "/conversations/42/ratings/offer-1/submit", RESULT),
    ("conversations.list_conversation_ratings_legacy", {"conversation_id": 42}, "GET", "/conversations/42/rating", None),
    ("conversations.search_conversations_legacy", {"query": "refund", "exact_match": False, "page_key": CURSOR}, "GET", "/search/conversations", None),
    ("anonymization.fetch_anonymization_status", {"request_id": "request-1"}, "GET", "/anonymization/request/request-1", None),
    ("anonymization.anonymize_entity_legacy", {"request": {"entityId": USER, "_type": "User", "forceAnonymization": False}}, "POST", "/anonymization", {"entityId": USER, "_type": "User", "forceAnonymization": False}),
    ("templates.list_templates", {"template_type": "QuickResponse", "page_key": CURSOR}, "GET", "/templates", None),
    ("templates.remove_template", {"template_id": "template-1"}, "DELETE", "/templates/template-1", None),
    ("settings.fetch_business_hours_definition", {"schedule_id": "schedule-1"}, "GET", "/business-hours/schedules/schedule-1/definition", None),
    ("settings.fetch_upcoming_business_hours", {"schedule_id": "schedule-1", "days": 90}, "GET", "/business-hours/schedules/schedule-1/upcoming", None),
    ("knowledge.add_knowledge_collection", {"title": "Support", "description": "", "internal_kb_enabled": False}, "POST", "/knowledge/collections", {"title": "Support", "description": "", "internalKbEnabled": False}),
    ("webhooks.list_webhook_subscriptions", {}, "GET", "/webhooks", None),
    ("webhooks.fetch_webhook_subscription", {"webhook_id": WEBHOOK}, "GET", f"/webhooks/{WEBHOOK}", None),
    ("webhooks.add_webhook_subscription", {"subscription": SUBSCRIPTION}, "POST", "/webhooks", SUBSCRIPTION),
    ("webhooks.modify_webhook_subscription", {"webhook_id": WEBHOOK, "changes": {"enabled": False, "events": [], "filters": {}, "customHeaders": {}}}, "PATCH", f"/webhooks/{WEBHOOK}", {"enabled": False, "events": [], "filters": {}, "customHeaders": {}}),
    ("webhooks.remove_webhook_subscription", {"webhook_id": WEBHOOK}, "DELETE", f"/webhooks/{WEBHOOK}", None),
    ("webhooks.fetch_webhook_delivery_status", {"webhook_id": WEBHOOK}, "GET", f"/webhooks/{WEBHOOK}/delivery-status", None),
    ("webhooks.fetch_webhook_event_logs", {"webhook_id": WEBHOOK, "event": "ConversationCreated"}, "GET", f"/webhooks/{WEBHOOK}/delivery-status/logs/ConversationCreated", None),
    ("conversations.list_conversation_flows", {"channel": "Email"}, "GET", "/conversations/flows", None),
    ("queues.check_conversation_queue_position", {"conversation_id": 42}, "GET", "/queues/conversation-position/42", None),
    ("users.update_end_users_bulk", {"end_users": [{"id": USER, "displayName": "User"}]}, "PUT", "/endusers", {"data": [{"id": USER, "displayName": "User"}]}),
    ("users.modify_end_users_bulk", {"end_users": [{"id": USER, "displayName": "User"}]}, "PATCH", "/endusers", {"data": [{"id": USER, "displayName": "User"}]}),
    ("analytics.prepare_analytics_record_query", {}, "GET", "/analytics/records", None),
    ("analytics.prepare_analytics_record_query", {"record_id": "closed_conversations"}, "GET", "/analytics/records/closed_conversations", None),
    ("analytics.fetch_analytics_filter_values", {"filter_attribute": "queue_id", "page_key": CURSOR}, "GET", "/analytics/filter/queue_id", None),
    ("analytics.fetch_unaggregated_data", {"record_id": "closed_conversations", "timezone": "UTC", "csid_filter": [42], "page_key": CURSOR}, "POST", "/analytics/records", {"id": "closed_conversations", "timezone": "UTC", "csidFilter": [42], "filters": []}),
]


class MissingEndpointProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import server
        self.client = Client(server.mcp)
        await self.client.__aenter__()
        self.dixa_client = DixaClient(api_key="test-api-key")

    async def asyncTearDown(self):
        await self.client.__aexit__(None, None, None)

    async def invoke(self, module_name, arguments, response_data=None, status=200):
        module = importlib.import_module("tools." + module_name)
        captured = []
        response_data = {"data": {"id": "created-1"}} if response_data is None else response_data

        def send(_session, request, **kwargs):
            captured.append((request, kwargs))
            response = requests.Response()
            response.status_code = status
            response.request = request
            response._content = b"" if status == 204 else json.dumps(response_data).encode()
            response.headers["Content-Type"] = "application/json"
            return response

        with patch.object(module, "get_dixa_client", return_value=self.dixa_client), patch.object(
            requests.Session, "send", autospec=True, side_effect=send
        ):
            try:
                result = await self.client.call_tool(module_name.rsplit(".", 1)[1], arguments)
            finally:
                self.assertEqual(1, len(captured), "Must issue exactly one request, without automatic retries")
        return result.data, captured[0][0], captured[0][1]

    async def test_all_new_and_repaired_operations_reach_documented_routes(self):
        for module, args, method, path, payload in CASES:
            with self.subTest(tool=module, arguments=args):
                status = 204 if method == "DELETE" else 200
                result, request, options = await self.invoke(module, args, status=status)
                self.assertEqual({"success": True} if status == 204 else {"data": {"id": "created-1"}}, result)
                self.assertEqual(method, request.method)
                parsed = urlsplit(request.url)
                self.assertEqual("dev.dixa.io", parsed.netloc)
                self.assertEqual("/v1" + path, parsed.path)
                self.assertEqual("test-api-key", request.headers["Authorization"])
                if payload is None:
                    self.assertIsNone(request.body)
                else:
                    self.assertEqual(payload, json.loads(request.body))
                    self.assertEqual("application/json", request.headers["Content-Type"])
                if not module.startswith(("analytics.", "users.")):
                    self.assertEqual(30, options["timeout"])
                query = parse_qs(parsed.query)
                if "page_key" in args:
                    self.assertEqual([CURSOR], query["pageKey"])
                if module in {"templates.list_templates", "conversations.search_conversations_legacy", "analytics.fetch_unaggregated_data", "analytics.fetch_analytics_filter_values"} or (module == "analytics.prepare_analytics_record_query" and not args):
                    self.assertEqual(["50"], query["pageLimit"])
                if "exact_match" in args:
                    self.assertEqual(["False"], query["exactMatch"])
                if "template_type" in args:
                    self.assertEqual([args["template_type"]], query["type"])
                if "channel" in args:
                    self.assertEqual([args["channel"]], query["channel"])
                if "days" in args:
                    self.assertEqual([str(args["days"])], query["days"])

    async def test_union_discriminators_and_json_encoded_inputs_survive_mcp(self):
        variants = [
            ("conversations.add_conversation_message", "message", {"conversation_id": 42}, {"_type": "Inbound", "content": {"_type": "Html", "value": "<p>Hi</p>"}, "attachments": []}),
            ("conversations.add_conversation_message", "message", {"conversation_id": 42}, {**MESSAGE, "content": {"_type": "Markdown", "value": "**Hi**"}}),
            ("conversations.submit_conversation_rating_result", "result", {"conversation_id": 42, "rating_id": "offer-1"}, {"ratingResult": {"_type": "Nps", "value": 0}}),
            ("conversations.submit_conversation_rating_result", "result", {"conversation_id": 42, "rating_id": "offer-1"}, {"ratingResult": {"_type": "ThumbsUpOrDown", "value": 1}}),
            ("webhooks.add_webhook_subscription", "subscription", {}, {**SUBSCRIPTION, "authorization": {"_type": "BasicAuth", "username": "test-user", "password": "dummy-password"}}),
            ("webhooks.add_webhook_subscription", "subscription", {}, {**SUBSCRIPTION, "authorization": {"_type": "TokenAuth", "value": "dummy-token"}}),
        ]
        for module, field, args, payload in variants:
            with self.subTest(tool=module, payload=payload):
                _, request, _ = await self.invoke(module, {**args, field: json.dumps(payload)})
                self.assertEqual(payload, json.loads(request.body))

    async def test_bulk_partial_failures_and_pagination_are_not_discarded(self):
        partial = {"data": [{"_type": "BulkActionSuccess", "data": {"id": AGENT}}, {"_type": "BulkActionFailure", "error": {"message": "Duplicate"}}]}
        result, _, _ = await self.invoke("agents.add_agents_bulk", {"agents": [{"displayName": "Test", "email": "test@example.com"}]}, partial, 201)
        self.assertEqual(partial, result)
        paginated = {"data": [{"id": "row-1"}], "meta": {"nextPage": CURSOR}}
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            result, _, _ = await self.invoke("analytics.fetch_unaggregated_data", {"record_id": "closed_conversations", "timezone": "UTC", "csid_filter": [42], "page_limit": 1}, paginated)
        self.assertEqual(paginated, result)
        self.assertEqual("", stdout.getvalue())

    async def test_webhook_responses_redact_credentials_without_modifying_input(self):
        response = {"data": {"id": WEBHOOK, "authorization": {"_type": "TokenAuth", "value": "dummy-secret"}, "customHeaders": {"X-Key": "dummy-header"}, "enabled": False}}
        result, _, _ = await self.invoke("webhooks.fetch_webhook_subscription", {"webhook_id": WEBHOOK}, response)
        self.assertEqual({"_type": "TokenAuth", "value": "[REDACTED]"}, result["data"]["authorization"])
        self.assertEqual({"X-Key": "[REDACTED]"}, result["data"]["customHeaders"])
        self.assertEqual("dummy-secret", response["data"]["authorization"]["value"])
        self.assertFalse(result["data"]["enabled"])

    async def test_optional_collection_fields_are_omitted(self):
        _, request, _ = await self.invoke("knowledge.add_knowledge_collection", {"title": "Support"})
        self.assertEqual({"title": "Support"}, json.loads(request.body))

    async def test_invalid_payloads_and_page_sizes_never_reach_dixa(self):
        invalid = [
            ("agents.add_agents_bulk", {"agents": [{"displayName": "Missing email"}]}),
            ("agents.update_agents_bulk", {"agents": [{"id": AGENT}]}),
            ("agents.modify_agents_bulk", {"agents": [{"displayName": "Missing ID"}]}),
            ("conversations.add_conversation_message", {"conversation_id": 42, "message": {"_type": "Outbound", "content": CONTENT}}),
            ("conversations.add_conversation_message", {"conversation_id": 42, "message": {"_type": "Inbound", "content": {"value": "Missing type"}}}),
            ("conversations.submit_conversation_rating_result", {"conversation_id": 42, "rating_id": "offer-1", "result": {"ratingResult": {"_type": "Csat", "value": 6}}}),
            ("webhooks.add_webhook_subscription", {"subscription": {"name": "Missing URL and auth"}}),
            ("settings.fetch_upcoming_business_hours", {"schedule_id": "schedule-1", "days": 91}),
            ("templates.list_templates", {"page_limit": 101}),
            ("analytics.fetch_unaggregated_data", {"record_id": "x", "timezone": "UTC", "csid_filter": [42], "page_key": CURSOR, "page_limit": 101}),
            ("analytics.fetch_unaggregated_data", {"record_id": "x", "timezone": "UTC", "filters": [{"attribute": "queue_id", "values": []}]}),
        ]
        for module_name, args in invalid:
            with self.subTest(tool=module_name):
                module = importlib.import_module("tools." + module_name)
                with patch.object(module, "get_dixa_client") as get_client, patch.object(requests.Session, "send") as send:
                    with self.assertRaises(ToolError):
                        await self.client.call_tool(module_name.rsplit(".", 1)[1], args)
                    get_client.assert_not_called()
                    send.assert_not_called()

    async def test_new_http_errors_do_not_echo_credentials_or_retry(self):
        for status in (400, 401, 403, 404, 500):
            with self.subTest(status=status), self.assertRaises(ToolError) as error:
                await self.invoke("webhooks.add_webhook_subscription", {"subscription": SUBSCRIPTION}, {"message": "dummy-private-value"}, status)
            self.assertIn(f"HTTP {status}", str(error.exception))
            self.assertNotIn("dummy-private-value", str(error.exception))


class AdditionalTransportTests(unittest.TestCase):
    def test_timeout_is_not_retried_or_exposed_with_sensitive_details(self):
        from dixa_api.http import api_request
        client = DixaClient(api_key="test-api-key")
        with patch.object(requests.Session, "send", side_effect=requests.Timeout("dummy-private-value")) as send:
            with self.assertRaises(requests.RequestException) as error:
                api_request(client, "POST", "/webhooks", payload=SUBSCRIPTION)
            send.assert_called_once()
        self.assertIn("outcome may be unknown", str(error.exception))
        self.assertNotIn("dummy-private-value", str(error.exception))
