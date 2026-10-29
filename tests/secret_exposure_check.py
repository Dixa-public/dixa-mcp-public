"""Offline security regressions through every published MCP tool; no real secrets/I/O."""
import ast
import copy
import importlib
import io
import json
import logging
import re
import socket
import traceback
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

import requests
from fastmcp import Client

from dixa_api import DixaClient
from dixa_api.safety import ITEM_ERROR_MESSAGE, raise_api_error, sanitize_diagnostics


ROOT = Path(__file__).resolve().parents[1]
MARKER = "SYNTHETIC_SECRET_CANARY_NEVER_A_REAL_CREDENTIAL"
UUID = "00000000-0000-4000-8000-000000000001"
CASES = json.loads((ROOT / "tests/fixtures/tool_security_cases.json").read_text())["cases"]


def model_text(result):
    return '\n'.join(getattr(c, 'text', '') for c in result.content) + json.dumps(result.structured_content)


class AllToolsSecretExposureTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import server
        self.client = Client(server.mcp)
        await self.client.__aenter__()
        self.output = io.StringIO()
        self.handler = logging.StreamHandler(self.output)
        self.logger = logging.getLogger('fastmcp')
        self.old_logging = (self.logger.handlers[:], self.logger.level, self.logger.propagate)
        self.logger.handlers = [self.handler]
        self.logger.setLevel(logging.ERROR)
        self.logger.propagate = False

    async def asyncTearDown(self):
        self.logger.handlers, level, self.logger.propagate = self.old_logging
        self.logger.setLevel(level)
        self.handler.close()
        await self.client.__aexit__(None, None, None)

    async def invoke(self, case, mode="success", payload=None):
        self.output.seek(0)
        self.output.truncate()
        calls = []
        def send(_session, request, **options):
            calls.append(request)
            if mode == "network":
                raise requests.ConnectionError("Synthetic diagnostic " + MARKER, request=request)
            response = requests.Response()
            response.request = request
            response.url = request.url + '?token=' + MARKER
            response.status_code = 500 if mode == "http500" else 400 if mode in {"json_error", "text_error"} else 200
            response.reason = MARKER
            response._content = (MARKER.encode() if mode in {"text_error", "invalid_json"}
                                 else json.dumps({'message': MARKER} if mode in {"json_error", "http500"}
                                                 else payload if payload is not None else [] if case['tool'] == 'list_agents_presence' else {'data': {}}).encode())
            return response
        module = importlib.import_module(case['module'])
        with patch.object(module, 'get_dixa_client', return_value=DixaClient(api_key=MARKER)), \
             patch.object(requests.Session, 'send', autospec=True, side_effect=send), \
             patch.object(socket, 'create_connection', side_effect=AssertionError('Live network prohibited')), \
             redirect_stdout(self.output), redirect_stderr(self.output):
            result = await self.client.call_tool(case['tool'], case['arguments'], raise_on_error=False)
        self.assertEqual(1, len(calls), 'Must reach HTTP once and never automatically retry')
        method, template = case['operation'].split(' ', 1)
        self.assertEqual(method, calls[0].method)
        route_pattern = re.sub(r'\\\{[^}]+\\\}', r'[^/]+', re.escape(template))
        self.assertIsNotNone(re.fullmatch(route_pattern, urlsplit(calls[0].url).path))
        self.assertNotIn(MARKER, self.output.getvalue(), 'Credential leaked into stdout, stderr or framework logs')
        self.assertNotIn(MARKER[:20], self.output.getvalue(), 'Credential prefix leaked into logs')
        return result

    async def test_all_124_tools_sanitize_errors_and_still_succeed(self):
        published = {t.name for t in await self.client.list_tools()}
        self.assertEqual(published, {c['tool'] for c in CASES})
        self.assertEqual(124, len(published))
        self.assertEqual(126, len({c['operation'] for c in CASES}))
        for case in CASES:
            for mode in ('json_error', 'text_error', 'http500', 'network', 'invalid_json', 'success'):
                with self.subTest(tool=case['tool'], operation=case['operation'], mode=mode):
                    result = await self.invoke(case, mode)
                    self.assertEqual(mode != 'success', result.is_error)
                    self.assertNotIn(MARKER, model_text(result))
                    if mode in {'json_error', 'text_error', 'http500'}:
                        self.assertIn('HTTP ' + ('500' if mode == 'http500' else '400'), model_text(result))
                    if mode in {'network', 'invalid_json'}:
                        self.assertIn('outcome may be unknown', model_text(result))

    async def test_all_partial_failure_and_webhook_diagnostic_paths(self):
        bulk = ['add_agents_bulk', 'add_conversation_notes_bulk', 'add_end_users_bulk',
                'assign_agents_to_queue', 'check_queue_availability', 'modify_agents_bulk',
                'modify_end_users_bulk', 'update_agents_bulk', 'update_end_users_bulk']
        errors = [{'message': MARKER, 'unrecognizedDiagnostic': MARKER}]
        fixtures = {name: {'data': [{'_type': 'BulkActionSuccess', 'data': {'id': UUID}},
                                   {'_type': 'BulkActionFailure', 'error': errors[0]}]}
                    for name in bulk}
        fixtures['import_conversations'] = {'data': {'partialErrors': errors}}
        for name in ('modify_knowledge_article_translations', 'upload_knowledge_article_attachments'):
            fixtures[name] = {'data': [], 'partialErrors': errors}
        detail = {'deliveryTimestamp': '2026-10-29T00:00:00Z', 'success': False,
                  'responseCode': 401, 'responseText': MARKER}
        fixtures['fetch_webhook_delivery_status'] = {'data': [{'event': 'ConversationCreated', 'deliveryStatus': detail}]}
        fixtures['fetch_webhook_event_logs'] = {'data': [{'deliveryDetail': detail, 'payload': MARKER}]}
        self.assertEqual(14, len(fixtures))
        for name, payload in fixtures.items():
            with self.subTest(tool=name):
                original = copy.deepcopy(payload)
                result = await self.invoke(next(c for c in CASES if c['tool'] == name), payload=payload)
                self.assertFalse(result.is_error)
                text = model_text(result)
                self.assertNotIn(MARKER, text)
                self.assertEqual(original, payload)
                if name in bulk:
                    self.assertIn('BulkActionSuccess', text)
                    self.assertIn('BulkActionFailure', text)
                    self.assertIn(UUID, text)
                elif name.startswith('fetch_webhook_'):
                    self.assertIn('401', text)
                    self.assertIn('2026-10-29T00:00:00Z', text)
                    self.assertIn('[REDACTED]', text)
                else:
                    self.assertIn('partialErrors', text)

    async def test_analytics_no_longer_prints_successful_payloads_or_responses(self):
        for name in ('prepare_analytics_metric_query', 'fetch_aggregated_data'):
            with self.subTest(tool=name):
                case = copy.deepcopy(next(c for c in CASES if c['tool'] == name))
                if name == 'fetch_aggregated_data':
                    case['arguments']['filters'] = [{'attribute': 'agent_id', 'values': [MARKER]}]
                result = await self.invoke(case, payload={'data': {'description': MARKER}})
                self.assertFalse(result.is_error)


class DiagnosticSafetyTests(unittest.TestCase):
    def test_partial_failures_preserve_metadata_without_mutating_input(self):
        payload = {'data': [{'data': {'id': UUID, 'message': 'Customer content'}},
                            {'error': {'_type': 'NotFound', 'id': UUID, 'message': MARKER, 'headers': MARKER}}],
                   'partialErrors': [{'message': MARKER, 'languageId': 'de', 'code': 500}],
                   'meta': {'nextPage': 'opaque-cursor'}}
        original = copy.deepcopy(payload)
        result = sanitize_diagnostics(payload)
        self.assertNotIn(MARKER, json.dumps(result))
        self.assertEqual(original, payload)
        self.assertEqual(payload['data'][0], result['data'][0])
        self.assertEqual({'message': ITEM_ERROR_MESSAGE, '_type': 'NotFound', 'id': UUID}, result['data'][1]['error'])
        self.assertEqual({'message': ITEM_ERROR_MESSAGE, 'languageId': 'de', 'code': 500}, result['partialErrors'][0])
        self.assertEqual(payload['meta'], result['meta'])

    def test_unexpected_error_shapes_and_unknown_metadata_fail_closed(self):
        for value in (MARKER, [MARKER], {'message': MARKER, '_type': MARKER, 'id': MARKER,
                                      'code': MARKER, 'languageId': MARKER}):
            with self.subTest(shape=type(value).__name__):
                result = sanitize_diagnostics({'data': [{'error': value}], 'partialErrors': value})
                self.assertNotIn(MARKER, json.dumps(result))
                self.assertIn(ITEM_ERROR_MESSAGE, json.dumps(result))
        self.assertEqual({'data': [{'error': None}], 'partialErrors': []},
                         sanitize_diagnostics({'data': [{'error': None}], 'partialErrors': []}))

    def test_customer_content_is_not_recursively_treated_as_diagnostics(self):
        payload = {'data': [{'content': {'message': 'Customer message', 'error': 'Quoted error'},
                             'customAttributes': {'error': 'Business data', 'partialErrors': 'Customer field'}}]}
        self.assertEqual(payload, sanitize_diagnostics(payload))

    def test_error_objects_and_formatted_tracebacks_withhold_request_details(self):
        request = requests.Request('POST', 'https://example.invalid/?token=' + MARKER,
                                   headers={'Authorization': MARKER}).prepare()
        response = requests.Response()
        response.status_code = 403
        response.request = request
        response._content = MARKER.encode()
        for original in (requests.HTTPError(MARKER, response=response, request=request),
                         requests.ConnectionError(MARKER, request=request)):
            try:
                try:
                    raise original
                except requests.RequestException as error:
                    raise_api_error(error)
            except requests.RequestException as safe:
                self.assertNotIn(MARKER, ''.join(traceback.format_exception(safe)))
                self.assertNotIn(MARKER, str(safe))
                self.assertIsNone(safe.response)
                self.assertIsNone(safe.request)
                self.assertTrue(safe.__suppress_context__)

    def test_authentication_sources_and_exceptions_are_quiet(self):
        import tools.base as base
        for headers, failure in (({'authorization': 'Bearer ' + MARKER}, None),
                                 ({}, RuntimeError(MARKER))):
            output = io.StringIO()
            token = base._client_api_key.set(None)
            try:
                with patch('fastmcp.server.dependencies.get_http_headers', return_value=headers, side_effect=failure), \
                     patch.object(base, '_api_key', None), patch.dict('os.environ', {'DIXA_API_KEY': MARKER}), \
                     redirect_stdout(output), redirect_stderr(output):
                    self.assertEqual(MARKER, base.get_api_key())
            finally:
                base._client_api_key.reset(token)
            self.assertEqual('', output.getvalue())

    def test_application_auth_and_analytics_paths_have_no_debug_output(self):
        for file in ('server.py', 'tools/base.py', 'tools/analytics/prepare_analytics_metric_query.py',
                     'tools/analytics/fetch_aggregated_data.py'):
            tree = ast.parse((ROOT / file).read_text())
            for call in (n for n in ast.walk(tree) if isinstance(n, ast.Call)):
                with self.subTest(file=file, line=call.lineno):
                    self.assertNotIn(ast.unparse(call.func), {'print', 'traceback.print_exc'})


if __name__ == '__main__':
    unittest.main()
