"""Offline coverage audit against the pinned published operation inventory."""
import ast
import json
import re
import unittest
from pathlib import Path
from fastmcp import Client
from dixa_api import DixaClient
from tools.workflows import TOOL_PREREQUISITES

ROOT = Path(__file__).resolve().parents[1]


def normalize(path):
    return re.sub(r"\{[^}]+\}", "{}", path)


def render_path(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(
            part.value if isinstance(part, ast.Constant) else
            "/v1" if isinstance(part.value, ast.Attribute) and part.value.attr == "base_url" else "{}"
            for part in node.values
        )
    raise AssertionError("Unrecognized endpoint path expression")


def inventory():
    methods = {}
    for path in (ROOT / "dixa_api").glob("*.py"):
        for function in ast.parse(path.read_text()).body:
            if not isinstance(function, ast.FunctionDef) or function.name.startswith("_"):
                continue
            urls = [render_path(node.value) for node in ast.walk(function)
                    if isinstance(node, ast.Assign) and any(
                        isinstance(target, ast.Name) and target.id == "url" for target in node.targets)]
            routes = set()
            for node in ast.walk(function):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "requests" and func.attr in {"get", "post", "put", "patch", "delete"}:
                    assert len(urls) == 1
                    routes.add((func.attr.upper(), normalize(urls[0])))
                elif isinstance(func, ast.Name) and func.id in {"_knowledge_request", "api_request"}:
                    routes.add((node.args[1].value, normalize("/v1" + render_path(node.args[2]))))
            if routes:
                methods[function.name] = routes
    registered = {node.args[0].id for node in ast.walk(ast.parse((ROOT / "server.py").read_text()))
                  if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                  and isinstance(node.func.value, ast.Name) and node.func.value.id == "mcp"
                  and node.func.attr == "tool" and node.args and isinstance(node.args[0], ast.Name)}
    tool_routes = {}
    for path in (ROOT / "tools").rglob("*.py"):
        for function in ast.parse(path.read_text()).body:
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)) or function.name not in registered:
                continue
            calls = {node.func.attr for node in ast.walk(function)
                     if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                     and node.func.attr in methods}
            for name in calls:
                assert callable(getattr(DixaClient, name)), name
            tool_routes[function.name] = set().union(*(methods[name] for name in calls))
    return registered, tool_routes


class EndpointCoverageTests(unittest.IsolatedAsyncioTestCase):
    async def test_all_126_documented_operations_have_registered_tools(self):
        import server
        registered, tool_routes = inventory()
        fixture = json.loads((ROOT / "tests/fixtures/dixa_v1_operations.json").read_text())
        expected = {(row["method"], normalize(row["path"])) for row in fixture["operations"]}
        actual = set().union(*tool_routes.values())
        self.assertEqual(126, len(expected))
        self.assertEqual(expected, actual, "Missing or undocumented active HTTP routes")
        self.assertEqual(registered, set(tool_routes))
        self.assertTrue(all(tool_routes.values()))
        async with Client(server.mcp) as client:
            published = {tool.name: tool for tool in await client.list_tools()}
        self.assertEqual(registered, set(published))
        self.assertEqual(124, len(published))
        self.assertEqual(registered, set(TOOL_PREREQUISITES))
        for name, tool in published.items():
            with self.subTest(tool=name):
                self.assertIn("Prerequisite tools:", tool.description)
                self.assertIn(TOOL_PREREQUISITES[name], tool.description)
                references = set(re.findall(r"\b(?:list|fetch|add|modify|remove|create|prepare|search|anonymize|submit)_[a-z_]+\b", TOOL_PREREQUISITES[name]))
                self.assertTrue(references <= registered, references - registered)
        for name in ("add_conversation_message", "add_webhook_subscription", "modify_webhook_subscription"):
            self.assertIn("approval", published[name].description)
        for name in ("list_conversation_ratings_legacy", "search_conversations_legacy", "anonymize_entity_legacy"):
            self.assertIn("Deprecated", published[name].description)
