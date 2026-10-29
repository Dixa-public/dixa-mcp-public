import ast
import base64
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from fastmcp import Client
from fastmcp.exceptions import ToolError
from requests.exceptions import HTTPError, RequestException

from dixa_api import DixaClient
from dixa_api import knowledge
from dixa_api.safety import ITEM_ERROR_MESSAGE
from tools import knowledge as knowledge_tools


REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TOOL_NAMES = [
    "list_knowledge_collections",
    "fetch_knowledge_collection_by_id",
    "fetch_knowledge_collection_catalog",
    "fetch_knowledge_category_by_id",
    "fetch_knowledge_category_translations",
    "fetch_knowledge_article_by_id",
    "fetch_knowledge_article_translations",
    "add_knowledge_category",
    "add_knowledge_article",
    "modify_knowledge_article",
    "remove_knowledge_article",
    "modify_knowledge_article_translations",
    "remove_knowledge_article_translation",
    "publish_knowledge_article_translation",
    "unpublish_knowledge_article_translation",
    "publish_knowledge_article",
    "unpublish_knowledge_article",
    "move_knowledge_article",
    "remove_knowledge_article_parent",
    "upload_knowledge_article_attachments",
    "add_knowledge_collection",
]

EXPECTED_CLIENT_METHOD_NAMES = {
    "get_knowledge_collections",
    "get_knowledge_collection",
    "get_knowledge_collection_catalog",
    "get_knowledge_category",
    "get_knowledge_category_translations",
    "get_knowledge_article",
    "get_knowledge_article_translations",
    "create_knowledge_collection",
    "create_knowledge_category",
    "create_knowledge_article",
    "patch_knowledge_article",
    "delete_knowledge_article",
    "patch_knowledge_article_translations",
    "delete_knowledge_article_translation",
    "publish_knowledge_article_translation",
    "unpublish_knowledge_article_translation",
    "publish_knowledge_article",
    "unpublish_knowledge_article",
    "move_knowledge_article",
    "delete_knowledge_article_parent",
    "upload_knowledge_article_attachments",
}

LEGACY_TOOL_NAMES = {
    "list_knowledge_articles",
    "list_knowledge_categories",
}

_UNSET = object()


def _resolve_schema_ref(root_schema, schema):
    """Resolve a local JSON Schema reference while preserving inline schemas."""
    while "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/"):
            raise AssertionError("Unexpected non-local schema reference: {}".format(reference))
        resolved = root_schema
        for part in reference[2:].split("/"):
            resolved = resolved[part.replace("~1", "/").replace("~0", "~")]
        schema = resolved
    return schema


def _schema_option(root_schema, schema, expected_type):
    """Return a typed branch from either a direct or nullable schema."""
    options = schema.get("anyOf", [schema])
    for option in options:
        resolved = _resolve_schema_ref(root_schema, option)
        if resolved.get("type") == expected_type:
            return resolved
    raise AssertionError("No {} schema branch found in {!r}".format(expected_type, schema))


class FakeResponse:
    def __init__(
        self,
        status_code=200,
        json_data=_UNSET,
        text="",
        json_raises=False,
    ):
        self.status_code = status_code
        self.json_data = {"data": "ok"} if json_data is _UNSET else json_data
        self.text = text
        self.json_raises = json_raises
        self.content = b"" if status_code == 204 else b"response"

    def raise_for_status(self):
        if self.status_code >= 400:
            raise HTTPError(
                "{} response".format(self.status_code),
                response=self,
            )

    def json(self):
        if self.json_raises:
            raise ValueError("response is not JSON")
        return self.json_data


class KnowledgeClientTests(unittest.TestCase):
    def setUp(self):
        self.client = DixaClient(api_key="test-api-key")
        self.responses = []
        self.request_error = None
        self.request_patcher = patch.object(
            knowledge.requests,
            "request",
            side_effect=self._dispatch_request,
        )
        self.request_mock = self.request_patcher.start()
        self.addCleanup(self.request_patcher.stop)

    def _dispatch_request(self, method, url, **kwargs):
        if self.request_error is not None:
            raise self.request_error
        if self.responses:
            return self.responses.pop(0)
        return FakeResponse()

    def assert_last_request(self, method, path, **expected_kwargs):
        args, kwargs = self.request_mock.call_args
        self.assertEqual(
            (method, "https://dev.dixa.io/v1{}".format(path)),
            args,
        )
        expected = {
            "headers": {"Authorization": "test-api-key"},
        }
        expected.update(expected_kwargs)
        self.assertEqual(expected, kwargs)
        self.request_mock.reset_mock()

    def test_all_seven_read_endpoint_mappings(self):
        read_cases = [
            (
                lambda: self.client.get_knowledge_collections(
                    page_key="opaque+/=",
                    page_limit=25,
                ),
                "/knowledge/collections",
                {"params": {"pageKey": "opaque+/=", "pageLimit": 25}},
            ),
            (
                lambda: self.client.get_knowledge_collection("collection-1"),
                "/knowledge/collections/collection-1",
                {},
            ),
            (
                lambda: self.client.get_knowledge_collection_catalog(
                    "collection-1",
                    language="da",
                ),
                "/knowledge/collections/collection-1/catalog",
                {"params": {"language": "da"}},
            ),
            (
                lambda: self.client.get_knowledge_category(
                    "category-1",
                    language="de",
                ),
                "/knowledge/categories/category-1",
                {"params": {"language": "de"}},
            ),
            (
                lambda: self.client.get_knowledge_category_translations(
                    "category-1"
                ),
                "/knowledge/categories/category-1/translations",
                {},
            ),
            (
                lambda: self.client.get_knowledge_article(
                    "article-1",
                    language="en",
                ),
                "/knowledge/articles/article-1",
                {"params": {"language": "en"}},
            ),
            (
                lambda: self.client.get_knowledge_article_translations(
                    "article-1"
                ),
                "/knowledge/articles/article-1/translations",
                {},
            ),
        ]

        for invoke, path, expected_kwargs in read_cases:
            with self.subTest(path=path):
                self.assertEqual({"data": "ok"}, invoke())
                self.assert_last_request("GET", path, **expected_kwargs)

    def test_none_query_parameters_are_omitted(self):
        cases = [
            (
                lambda: self.client.get_knowledge_collections(),
                "/knowledge/collections",
            ),
            (
                lambda: self.client.get_knowledge_collection_catalog("collection-1"),
                "/knowledge/collections/collection-1/catalog",
            ),
            (
                lambda: self.client.get_knowledge_category("category-1"),
                "/knowledge/categories/category-1",
            ),
            (
                lambda: self.client.get_knowledge_article("article-1"),
                "/knowledge/articles/article-1",
            ),
        ]

        for invoke, path in cases:
            with self.subTest(path=path):
                invoke()
                self.assert_last_request("GET", path)

    def test_empty_page_key_and_zero_limit_are_preserved(self):
        self.client.get_knowledge_collections(page_key="", page_limit=0)

        self.assert_last_request(
            "GET",
            "/knowledge/collections",
            params={"pageKey": "", "pageLimit": 0},
        )

    def test_create_article_mapping_and_nested_translation_payload(self):
        translations = [
            {
                "languageId": "en",
                "title": "Getting started",
                "content": "",
            }
        ]

        self.client.create_knowledge_article(
            translations=translations,
            parent_id="category-1",
            tags=["tag-1"],
            pre_release=False,
        )

        self.assert_last_request(
            "POST",
            "/knowledge/articles",
            headers={
                "Authorization": "test-api-key",
                "Content-Type": "application/json",
            },
            json={
                "translations": translations,
                "parentId": "category-1",
                "tags": ["tag-1"],
                "preRelease": False,
            },
        )

    def test_pre_release_creation_requires_parent_before_http_request(self):
        for parent_id in (None, "", "   "):
            with self.subTest(parent_id=parent_id):
                with self.assertRaisesRegex(ValueError, "parent_id is required"):
                    self.client.create_knowledge_article(
                        parent_id=parent_id, pre_release=True
                    )
        self.request_mock.assert_not_called()

    def test_patch_article_mapping_and_empty_tag_operations(self):
        tags = {"add": [], "remove": []}

        self.client.patch_knowledge_article(
            "article-1",
            owned_by="",
            tags=tags,
            pre_release=False,
        )

        self.assert_last_request(
            "PATCH",
            "/knowledge/articles/article-1",
            headers={
                "Authorization": "test-api-key",
                "Content-Type": "application/json",
            },
            json={
                "ownedBy": "",
                "tags": tags,
                "preRelease": False,
            },
        )

    def test_patch_translations_mapping_preserves_partial_success_response(self):
        translations = [
            {
                "languageId": "da",
                "title": "Kom godt i gang",
                "content": "<p>Hej</p>",
            }
        ]
        api_result = {
            "data": [{"language": "da", "title": "Kom godt i gang"}],
            "partialErrors": [
                {"languageId": "de", "message": "Translation rejected"}
            ],
        }
        self.responses.append(FakeResponse(json_data=api_result))

        result = self.client.patch_knowledge_article_translations(
            "article-1",
            translations=translations,
        )

        self.assertEqual(api_result["data"], result["data"])
        self.assertEqual([{"languageId": "de", "message": ITEM_ERROR_MESSAGE}], result["partialErrors"])
        self.assertEqual("Translation rejected", api_result["partialErrors"][0]["message"])
        self.assert_last_request(
            "PATCH",
            "/knowledge/articles/article-1/translations",
            headers={
                "Authorization": "test-api-key",
                "Content-Type": "application/json",
            },
            json={"translations": translations},
        )

    def test_none_payload_properties_are_omitted_but_empty_lists_are_kept(self):
        payload_cases = [
            (
                lambda: self.client.create_knowledge_article(),
                "POST",
                "/knowledge/articles",
                {},
            ),
            (
                lambda: self.client.patch_knowledge_article("article-1"),
                "PATCH",
                "/knowledge/articles/article-1",
                {},
            ),
            (
                lambda: self.client.patch_knowledge_article_translations(
                    "article-1"
                ),
                "PATCH",
                "/knowledge/articles/article-1/translations",
                {},
            ),
            (
                lambda: self.client.patch_knowledge_article_translations(
                    "article-1",
                    translations=[],
                ),
                "PATCH",
                "/knowledge/articles/article-1/translations",
                {"translations": []},
            ),
        ]

        for invoke, method, path, payload in payload_cases:
            with self.subTest(method=method, path=path, payload=payload):
                invoke()
                self.assert_last_request(
                    method,
                    path,
                    headers={
                        "Authorization": "test-api-key",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

    def test_all_eight_action_mappings_normalize_204(self):
        action_cases = [
            (
                lambda: self.client.delete_knowledge_article("article-1"),
                "DELETE",
                "/knowledge/articles/article-1",
            ),
            (
                lambda: self.client.delete_knowledge_article_translation(
                    "article-1",
                    "da",
                ),
                "DELETE",
                "/knowledge/articles/article-1/translations/da",
            ),
            (
                lambda: self.client.publish_knowledge_article_translation(
                    "article-1",
                    "da",
                ),
                "POST",
                "/knowledge/articles/article-1/translations/da/publish",
            ),
            (
                lambda: self.client.unpublish_knowledge_article_translation(
                    "article-1",
                    "da",
                ),
                "POST",
                "/knowledge/articles/article-1/translations/da/unpublish",
            ),
            (
                lambda: self.client.publish_knowledge_article("article-1"),
                "POST",
                "/knowledge/articles/article-1/publish",
            ),
            (
                lambda: self.client.unpublish_knowledge_article("article-1"),
                "POST",
                "/knowledge/articles/article-1/unpublish",
            ),
            (
                lambda: self.client.move_knowledge_article(
                    "article-1",
                    "category-2",
                ),
                "PATCH",
                "/knowledge/articles/article-1/parent/category-2",
            ),
            (
                lambda: self.client.delete_knowledge_article_parent("article-1"),
                "DELETE",
                "/knowledge/articles/article-1/parent",
            ),
        ]

        for invoke, method, path in action_cases:
            with self.subTest(method=method, path=path):
                self.responses.append(FakeResponse(status_code=204))
                self.assertEqual({"success": True}, invoke())
                self.assert_last_request(method, path)

    def test_attachment_mapping_uses_repeated_parts_and_preserves_response(self):
        files = [
            {
                "filename": "logo.png",
                "media_type": "image/png",
                "content": b"\x89PNG",
            },
            {
                "filename": "banner.jpg",
                "media_type": "image/jpeg",
                "content": b"\xff\xd8\xff",
            },
        ]
        api_result = {
            "data": [
                {
                    "originalFilename": "logo.png",
                    "url": "https://cdn.example/logo.png",
                }
            ],
            "partialErrors": [
                {
                    "originalFilename": "banner.jpg",
                    "message": "Upload failed",
                    "code": 500,
                }
            ],
        }
        self.responses.append(FakeResponse(json_data=api_result))

        result = self.client.upload_knowledge_article_attachments(files=files)

        self.assertEqual(api_result["data"], result["data"])
        self.assertEqual([{"code": 500, "message": ITEM_ERROR_MESSAGE}], result["partialErrors"])
        self.assertEqual("Upload failed", api_result["partialErrors"][0]["message"])
        self.assert_last_request(
            "POST",
            "/knowledge/articles/attachments",
            files=[
                ("files", ("logo.png", b"\x89PNG", "image/png")),
                ("files", ("banner.jpg", b"\xff\xd8\xff", "image/jpeg")),
            ],
        )

    def test_json_http_error_withholds_details_and_response(self):
        response = FakeResponse(
            status_code=400,
            json_data={"message": "Invalid knowledge request"},
        )
        self.responses.append(response)

        with self.assertRaises(HTTPError) as raised:
            self.client.get_knowledge_collection("invalid")

        self.assertIsNone(raised.exception.response)
        self.assertEqual("Dixa API returned HTTP 400", str(raised.exception))
        self.assertNotIn("Invalid knowledge request", str(raised.exception))

    def test_plain_text_http_error_withholds_details(self):
        response = FakeResponse(
            status_code=502,
            text="upstream unavailable",
            json_raises=True,
        )
        self.responses.append(response)

        with self.assertRaises(HTTPError) as raised:
            self.client.get_knowledge_collection("collection-1")

        self.assertEqual("Dixa API returned HTTP 502", str(raised.exception))
        self.assertNotIn("upstream unavailable", str(raised.exception))

    def test_network_error_is_wrapped_as_request_failure(self):
        original = RequestException("connection closed")
        self.request_error = original

        with self.assertRaises(RequestException) as raised:
            self.client.get_knowledge_collection("collection-1")

        self.assertIn("outcome may be unknown", str(raised.exception))
        self.assertNotIn("connection closed", str(raised.exception))
        self.assertIsNone(raised.exception.__cause__)
        self.assertTrue(raised.exception.__suppress_context__)


class KnowledgeMultipartEncodingTests(unittest.TestCase):
    def test_requests_generates_multipart_boundary_for_repeated_file_parts(self):
        client = DixaClient(api_key="test-api-key")
        captured = {}

        def capture_prepared_request(_session, request, **_kwargs):
            captured["request"] = request
            return FakeResponse(json_data={"data": [], "partialErrors": []})

        with patch.object(
            knowledge.requests.sessions.Session,
            "send",
            autospec=True,
            side_effect=capture_prepared_request,
        ):
            result = client.upload_knowledge_article_attachments(
                files=[
                    {
                        "filename": "logo.png",
                        "media_type": "image/png",
                        "content": b"PNG",
                    },
                    {
                        "filename": "banner.jpg",
                        "media_type": "image/jpeg",
                        "content": b"JPEG",
                    },
                ]
            )

        self.assertEqual({"data": [], "partialErrors": []}, result)
        prepared = captured["request"]
        content_type = prepared.headers["Content-Type"]
        self.assertTrue(content_type.startswith("multipart/form-data; boundary="))
        self.assertEqual("test-api-key", prepared.headers["Authorization"])
        self.assertEqual(2, prepared.body.count(b'name="files"'))
        self.assertIn(b'filename="logo.png"', prepared.body)
        self.assertIn(b"Content-Type: image/png", prepared.body)
        self.assertIn(b'filename="banner.jpg"', prepared.body)
        self.assertIn(b"Content-Type: image/jpeg", prepared.body)


class CapturingClient:
    def __init__(self):
        self.calls = []

    def __getattr__(self, method_name):
        def capture(*args, **kwargs):
            self.calls.append((method_name, args, kwargs))
            return {"delegated_to": method_name}

        return capture


class KnowledgeWrapperTests(unittest.IsolatedAsyncioTestCase):
    async def _assert_delegates(
        self,
        tool_name,
        tool_kwargs,
        client_method_name,
        expected_client_kwargs,
    ):
        tool = getattr(knowledge_tools, tool_name)
        module = sys.modules[tool.__module__]
        client = CapturingClient()

        with patch.object(module, "get_dixa_client", return_value=client):
            result = await tool(**tool_kwargs)

        self.assertEqual({"delegated_to": client_method_name}, result)
        self.assertEqual(
            [(client_method_name, (), expected_client_kwargs)],
            client.calls,
        )

    async def test_all_twenty_one_wrappers_delegate_with_api_shaped_arguments(self):
        translations = [
            {
                "languageId": "en",
                "title": "Getting started",
                "content": "<p>Hello</p>",
            }
        ]
        tag_updates = {"add": ["tag-1"], "remove": []}
        encoded_content = base64.b64encode(b"image bytes").decode("ascii")
        cases = [
            (
                "add_knowledge_collection",
                {"title": "Support", "description": "", "internal_kb_enabled": False},
                "create_knowledge_collection",
                {"title": "Support", "description": "", "internal_kb_enabled": False},
            ),
            (
                "list_knowledge_collections",
                {"page_key": "opaque==", "page_limit": 50},
                "get_knowledge_collections",
                {"page_key": "opaque==", "page_limit": 50},
            ),
            (
                "fetch_knowledge_collection_by_id",
                {"collection_id": "collection-1"},
                "get_knowledge_collection",
                {"collection_id": "collection-1"},
            ),
            (
                "fetch_knowledge_collection_catalog",
                {"collection_id": "collection-1", "language": "da"},
                "get_knowledge_collection_catalog",
                {"collection_id": "collection-1", "language": "da"},
            ),
            (
                "fetch_knowledge_category_by_id",
                {"category_id": "category-1", "language": "de"},
                "get_knowledge_category",
                {"category_id": "category-1", "language": "de"},
            ),
            (
                "fetch_knowledge_category_translations",
                {"category_id": "category-1"},
                "get_knowledge_category_translations",
                {"category_id": "category-1"},
            ),
            (
                "fetch_knowledge_article_by_id",
                {"article_id": "article-1", "language": "en"},
                "get_knowledge_article",
                {"article_id": "article-1", "language": "en"},
            ),
            (
                "fetch_knowledge_article_translations",
                {"article_id": "article-1"},
                "get_knowledge_article_translations",
                {"article_id": "article-1"},
            ),
            (
                "add_knowledge_category",
                {
                    "parent_id": "collection-1",
                    "translations": [{"languageId": "en", "title": "Getting started"}],
                },
                "create_knowledge_category",
                {
                    "parent_id": "collection-1",
                    "translations": [{"languageId": "en", "title": "Getting started"}],
                },
            ),
            (
                "add_knowledge_article",
                {
                    "translations": translations,
                    "parent_id": "category-1",
                    "tags": [],
                    "pre_release": False,
                },
                "create_knowledge_article",
                {
                    "translations": translations,
                    "parent_id": "category-1",
                    "tags": [],
                    "pre_release": False,
                },
            ),
            (
                "modify_knowledge_article",
                {
                    "article_id": "article-1",
                    "owned_by": "agent-1",
                    "tags": tag_updates,
                    "pre_release": False,
                },
                "patch_knowledge_article",
                {
                    "article_id": "article-1",
                    "owned_by": "agent-1",
                    "tags": tag_updates,
                    "pre_release": False,
                },
            ),
            (
                "remove_knowledge_article",
                {"article_id": "article-1"},
                "delete_knowledge_article",
                {"article_id": "article-1"},
            ),
            (
                "modify_knowledge_article_translations",
                {"article_id": "article-1", "translations": translations},
                "patch_knowledge_article_translations",
                {"article_id": "article-1", "translations": translations},
            ),
            (
                "remove_knowledge_article_translation",
                {"article_id": "article-1", "language_id": "da"},
                "delete_knowledge_article_translation",
                {"article_id": "article-1", "language_id": "da"},
            ),
            (
                "publish_knowledge_article_translation",
                {"article_id": "article-1", "language_id": "da"},
                "publish_knowledge_article_translation",
                {"article_id": "article-1", "language_id": "da"},
            ),
            (
                "unpublish_knowledge_article_translation",
                {"article_id": "article-1", "language_id": "da"},
                "unpublish_knowledge_article_translation",
                {"article_id": "article-1", "language_id": "da"},
            ),
            (
                "publish_knowledge_article",
                {"article_id": "article-1"},
                "publish_knowledge_article",
                {"article_id": "article-1"},
            ),
            (
                "unpublish_knowledge_article",
                {"article_id": "article-1"},
                "unpublish_knowledge_article",
                {"article_id": "article-1"},
            ),
            (
                "move_knowledge_article",
                {"article_id": "article-1", "parent_id": "category-2"},
                "move_knowledge_article",
                {"article_id": "article-1", "parent_id": "category-2"},
            ),
            (
                "remove_knowledge_article_parent",
                {"article_id": "article-1"},
                "delete_knowledge_article_parent",
                {"article_id": "article-1"},
            ),
            (
                "upload_knowledge_article_attachments",
                {
                    "files": [
                        {
                            "filename": "logo.png",
                            "media_type": "image/png",
                            "content_base64": encoded_content,
                        }
                    ]
                },
                "upload_knowledge_article_attachments",
                {
                    "files": [
                        {
                            "filename": "logo.png",
                            "media_type": "image/png",
                            "content": b"image bytes",
                        }
                    ]
                },
            ),
        ]

        self.assertEqual(21, len(cases))
        for case in cases:
            with self.subTest(tool=case[0]):
                await self._assert_delegates(*case)

    async def test_attachment_wrapper_rejects_invalid_count_shape_and_base64(self):
        tool = knowledge_tools.upload_knowledge_article_attachments
        module = sys.modules[tool.__module__]
        valid = {
            "filename": "logo.png",
            "media_type": "image/png",
            "content_base64": base64.b64encode(b"logo").decode("ascii"),
        }
        invalid_cases = [
            None,
            [],
            [valid] * 6,
            ["not-an-object"],
            [{"filename": "logo.png", "media_type": "image/png"}],
            [
                {
                    "filename": "logo.png",
                    "media_type": "image/png",
                    "content_base64": 123,
                }
            ],
            [
                {
                    "filename": "logo.png",
                    "media_type": "image/png",
                    "content_base64": "%%%not-base64%%%",
                }
            ],
        ]

        for files in invalid_cases:
            with self.subTest(files=files):
                with patch.object(module, "get_dixa_client") as get_client:
                    with self.assertRaises(ValueError):
                        await tool(files=files)
                    get_client.assert_not_called()


class KnowledgeSurfaceTests(unittest.TestCase):
    def test_package_exports_exactly_the_twenty_one_official_tools(self):
        self.assertEqual(EXPECTED_TOOL_NAMES, knowledge_tools.__all__)
        self.assertEqual(21, len(set(knowledge_tools.__all__)))
        for name in EXPECTED_TOOL_NAMES:
            self.assertTrue(callable(getattr(knowledge_tools, name)))
        self.assertTrue(LEGACY_TOOL_NAMES.isdisjoint(knowledge_tools.__all__))

    def test_dixa_client_has_exactly_the_twenty_one_knowledge_bindings(self):
        actual = {
            name
            for name in vars(DixaClient)
            if "knowledge" in name
        }

        self.assertEqual(EXPECTED_CLIENT_METHOD_NAMES, actual)

    def test_server_imports_and_registers_exactly_the_official_tools(self):
        server_tree = ast.parse(
            (REPO_ROOT / "server.py").read_text(encoding="utf-8")
        )
        imported = []
        registered = []

        for node in ast.walk(server_tree):
            if isinstance(node, ast.ImportFrom) and node.module == "tools.knowledge":
                imported.extend(alias.name for alias in node.names)
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Attribute):
                continue
            if not isinstance(node.func.value, ast.Name):
                continue
            if node.func.value.id != "mcp" or node.func.attr != "tool":
                continue
            if len(node.args) == 1 and isinstance(node.args[0], ast.Name):
                registered.append(node.args[0].id)

        self.assertEqual(set(EXPECTED_TOOL_NAMES), set(imported))
        for name in EXPECTED_TOOL_NAMES:
            self.assertEqual(1, registered.count(name), name)
        for name in LEGACY_TOOL_NAMES:
            self.assertNotIn(name, registered)


class KnowledgeCategoryProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_category_creation_from_mcp_to_http_preserves_payload_and_response(self):
        import server

        module = sys.modules[knowledge_tools.add_knowledge_category.__module__]
        dixa_client = DixaClient(api_key="test-api-key")
        translations = [
            {"languageId": "en", "title": "Getting Started"},
            {"languageId": "da", "title": "Kom godt i gang"},
        ]
        cases = [
            ("collection-1", {}, {}),
            ("category-1", {"translations": None}, {}),
            ("collection-1", {"translations": []}, {"translations": []}),
            ("collection-1", {"translations": translations}, {"translations": translations}),
            ("category-1", {"translations": json.dumps(translations)}, {"translations": translations}),
        ]

        async with Client(server.mcp) as client:
            for parent_id, arguments, payload in cases:
                with self.subTest(parent_id=parent_id, arguments=arguments):
                    api_result = {
                        "data": {
                            "id": "created-category",
                            "isLocked": False,
                            "restrictions": {"isRestricted": False},
                            "parentCollections": ["collection-1"],
                        }
                    }
                    with patch.object(module, "get_dixa_client", return_value=dixa_client), patch.object(
                        knowledge.requests, "request", return_value=FakeResponse(json_data=api_result)
                    ) as request:
                        result = await client.call_tool(
                            "add_knowledge_category",
                            {"parent_id": parent_id, **arguments},
                        )

                    self.assertEqual(api_result, result.data)
                    request.assert_called_once_with(
                        "POST",
                        "https://dev.dixa.io/v1/knowledge/categories",
                        headers={
                            "Authorization": "test-api-key",
                            "Content-Type": "application/json",
                        },
                        json={"parentId": parent_id, **payload},
                    )

    async def test_invalid_category_arguments_fail_before_creating_a_client(self):
        import server

        module = sys.modules[knowledge_tools.add_knowledge_category.__module__]
        invalid_arguments = [
            {},
            {"parent_id": None},
            {"parent_id": "collection-1", "translations": [{"title": "Getting Started"}]},
            {"parent_id": "collection-1", "translations": [{"languageId": "en"}]},
            {"parent_id": "collection-1", "translations": "not-json"},
            {"parent_id": "collection-1", "translations": "{}"},
        ]

        async with Client(server.mcp) as client:
            for arguments in invalid_arguments:
                with self.subTest(arguments=arguments), patch.object(module, "get_dixa_client") as get_client:
                    with self.assertRaises(ToolError):
                        await client.call_tool("add_knowledge_category", arguments)
                    get_client.assert_not_called()

    async def test_category_http_errors_are_reported_without_retrying_creation(self):
        import server

        module = sys.modules[knowledge_tools.add_knowledge_category.__module__]
        dixa_client = DixaClient(api_key="test-api-key")

        async with Client(server.mcp) as client:
            for status_code in (400, 404, 500):
                with self.subTest(status_code=status_code), patch.object(
                    module, "get_dixa_client", return_value=dixa_client
                ), patch.object(
                    knowledge.requests,
                    "request",
                    return_value=FakeResponse(
                        status_code=status_code,
                        json_data={"message": "Category creation failed"},
                    ),
                ) as request:
                    with self.assertRaisesRegex(ToolError, "HTTP {}".format(status_code)):
                        await client.call_tool("add_knowledge_category", {"parent_id": "collection-1"})
                    request.assert_called_once()


class KnowledgeProtocolMetadataTests(unittest.IsolatedAsyncioTestCase):
    async def test_article_creation_handles_empty_tags_through_mcp(self):
        import server

        real_client = DixaClient(api_key="test-api-key")
        add_module = sys.modules[knowledge_tools.add_knowledge_article.__module__]
        translation = {"languageId": "en", "title": "Disposable regression test"}
        with patch.object(add_module, "get_dixa_client", return_value=real_client):
            with patch.object(knowledge.requests, "request") as request:
                request.return_value.status_code = 200
                request.return_value.json.return_value = {"data": {"id": "article-1"}}
                async with Client(server.mcp) as client:
                    for tags in ([], "[]", ["tag-1"]):
                        await client.call_tool("add_knowledge_article", {
                            "translations": [translation], "parent_id": "category-1",
                            "pre_release": True, "tags": tags,
                        })
                        payload = request.call_args.kwargs["json"]
                        self.assertEqual("category-1", payload["parentId"])
                        self.assertIs(True, payload["preRelease"])
                        self.assertEqual([translation], payload["translations"])
                        if tags == ["tag-1"]:
                            self.assertEqual(["tag-1"], payload["tags"])
                        else:
                            self.assertNotIn("tags", payload)

                    request.reset_mock()
                    with self.assertRaisesRegex(ToolError, "fetch_knowledge_collection_catalog"):
                        await client.call_tool("add_knowledge_article", {
                            "translations": [translation], "pre_release": True,
                        })
                    request.assert_not_called()

    async def test_protocol_coerces_claude_json_encoded_structured_arguments(self):
        import server

        capturing_client = CapturingClient()
        translations_json = (
            '[{"languageId":"en","title":"ZZZ Tool Test - DELETE ME",'
            '"content":"<p>Test content for tool verification.</p>"}]'
        )

        async with Client(server.mcp) as client:
            add_module = sys.modules[knowledge_tools.add_knowledge_article.__module__]
            with patch.object(
                add_module,
                "get_dixa_client",
                return_value=capturing_client,
            ):
                await client.call_tool(
                    "add_knowledge_article",
                    {
                        "translations": translations_json,
                        "parent_id": "5d84a378-5a3e-11ef-9fc5-d3e1ed238c4c",
                        "tags": "[]",
                        "pre_release": "false",
                    },
                )

            modify_module = sys.modules[
                knowledge_tools.modify_knowledge_article.__module__
            ]
            with patch.object(
                modify_module,
                "get_dixa_client",
                return_value=capturing_client,
            ):
                await client.call_tool(
                    "modify_knowledge_article",
                    {
                        "article_id": "article-1",
                        "tags": '{"add":["tag-1"],"remove":[]}',
                        "pre_release": "true",
                    },
                )

            translations_module = sys.modules[
                knowledge_tools.modify_knowledge_article_translations.__module__
            ]
            with patch.object(
                translations_module,
                "get_dixa_client",
                return_value=capturing_client,
            ):
                await client.call_tool(
                    "modify_knowledge_article_translations",
                    {
                        "article_id": "article-1",
                        "translations": translations_json,
                    },
                )

            attachment_module = sys.modules[
                knowledge_tools.upload_knowledge_article_attachments.__module__
            ]
            with patch.object(
                attachment_module,
                "get_dixa_client",
                return_value=capturing_client,
            ):
                await client.call_tool(
                    "upload_knowledge_article_attachments",
                    {
                        "files": (
                            '[{"filename":"test.png","media_type":"image/png",'
                            '"content_base64":"aW1hZ2U="}]'
                        ),
                    },
                )

        expected_translation = {
            "languageId": "en",
            "title": "ZZZ Tool Test - DELETE ME",
            "content": "<p>Test content for tool verification.</p>",
        }
        self.assertEqual(
            [
                (
                    "create_knowledge_article",
                    (),
                    {
                        "translations": [expected_translation],
                        "parent_id": "5d84a378-5a3e-11ef-9fc5-d3e1ed238c4c",
                        "tags": [],
                        "pre_release": False,
                    },
                ),
                (
                    "patch_knowledge_article",
                    (),
                    {
                        "article_id": "article-1",
                        "owned_by": None,
                        "tags": {"add": ["tag-1"], "remove": []},
                        "pre_release": True,
                    },
                ),
                (
                    "patch_knowledge_article_translations",
                    (),
                    {
                        "article_id": "article-1",
                        "translations": [expected_translation],
                    },
                ),
                (
                    "upload_knowledge_article_attachments",
                    (),
                    {
                        "files": [
                            {
                                "filename": "test.png",
                                "media_type": "image/png",
                                "content": b"image",
                            }
                        ]
                    },
                ),
            ],
            capturing_client.calls,
        )

    async def test_protocol_exposes_descriptions_schemas_annotations_and_instructions(self):
        import server

        read_only_names = set(EXPECTED_TOOL_NAMES[:7])
        additive_names = {
            "add_knowledge_collection",
            "add_knowledge_category",
            "add_knowledge_article",
            "upload_knowledge_article_attachments",
        }
        non_idempotent_names = additive_names | {
            "publish_knowledge_article",
            "publish_knowledge_article_translation",
        }
        destructive_names = set(EXPECTED_TOOL_NAMES) - read_only_names - additive_names

        async with Client(server.mcp) as client:
            protocol_tools = {
                tool.name: tool
                for tool in await client.list_tools()
                if "knowledge" in tool.name
            }
            instructions = client.initialize_result.instructions

        self.assertEqual(set(EXPECTED_TOOL_NAMES), set(protocol_tools))
        self.assertEqual(
            "Add Knowledge Article",
            protocol_tools["add_knowledge_article"].title,
        )

        for name, tool in protocol_tools.items():
            with self.subTest(tool=name):
                self.assertTrue(tool.title)
                self.assertTrue(tool.description)
                self.assertTrue(tool.annotations.openWorldHint)
                self.assertEqual(name in read_only_names, tool.annotations.readOnlyHint)
                self.assertEqual(name in destructive_names, tool.annotations.destructiveHint)
                self.assertEqual(name not in non_idempotent_names, tool.annotations.idempotentHint)
                if name not in read_only_names:
                    self.assertRegex(
                        " ".join(tool.description.split()),
                        r"MUST obtain explicit (?:user )?confirmation",
                    )

        category_tool = protocol_tools["add_knowledge_category"]
        self.assertEqual("Add Knowledge Category", category_tool.title)
        category_schema = category_tool.inputSchema
        self.assertEqual(["parent_id"], category_schema["required"])
        self.assertEqual({"parent_id", "translations"}, set(category_schema["properties"]))
        category_translations = _schema_option(
            category_schema, category_schema["properties"]["translations"], "array"
        )
        category_translation = _resolve_schema_ref(category_schema, category_translations["items"])
        self.assertEqual(["languageId", "title"], category_translation["required"])
        self.assertEqual({"languageId", "title"}, set(category_translation["properties"]))
        self.assertIn("collection ID", category_tool.description)
        self.assertIn("subcategory", category_tool.description)
        self.assertIn("knowledge.content:w", category_tool.description)
        self.assertIn("Create categories: `add_knowledge_category`", instructions)
        self.assertNotIn("category-creation endpoint", instructions)

        create_schema = protocol_tools["add_knowledge_article"].inputSchema
        translation_argument_schema = create_schema["properties"]["translations"]
        translation_array_schema = _schema_option(
            create_schema,
            translation_argument_schema,
            "array",
        )
        translation_schema = _resolve_schema_ref(
            create_schema,
            translation_array_schema["items"],
        )
        self.assertFalse(
            any(
                _resolve_schema_ref(create_schema, option).get("type") == "string"
                for option in translation_argument_schema.get(
                    "anyOf", [translation_argument_schema]
                )
            )
        )
        self.assertEqual(["languageId", "title"], translation_schema["required"])
        self.assertEqual(
            {"languageId", "title", "content"},
            set(translation_schema["properties"]),
        )
        self.assertIn(
            "ISO language code",
            translation_schema["properties"]["languageId"]["description"],
        )
        self.assertIn(
            "HTML article body",
            translation_schema["properties"]["content"]["description"],
        )

        update_schema = protocol_tools["modify_knowledge_article"].inputSchema
        tag_schema = _schema_option(
            update_schema,
            update_schema["properties"]["tags"],
            "object",
        )
        self.assertEqual({"add", "remove"}, set(tag_schema["properties"]))
        self.assertIn("Tag IDs to add", tag_schema["properties"]["add"]["description"])

        upload_schema = protocol_tools[
            "upload_knowledge_article_attachments"
        ].inputSchema
        upload_array_schema = _schema_option(
            upload_schema,
            upload_schema["properties"]["files"],
            "array",
        )
        attachment_schema = _resolve_schema_ref(
            upload_schema,
            upload_array_schema["items"],
        )
        self.assertEqual(
            ["filename", "media_type", "content_base64"],
            attachment_schema["required"],
        )
        self.assertIn(
            "data-URL prefixes",
            attachment_schema["properties"]["content_base64"]["description"],
        )

        self.assertIn(
            "replaces the removed global article/category listing tools",
            protocol_tools["fetch_knowledge_collection_catalog"].description,
        )
        self.assertIn(
            "every version of one article language",
            protocol_tools["remove_knowledge_article_translation"].description,
        )
        self.assertIn(
            "new version of every translation",
            protocol_tools["publish_knowledge_article"].description,
        )
        single_publish_description = protocol_tools[
            "publish_knowledge_article_translation"
        ].description
        self.assertIn("preRelease=true", single_publish_description)
        self.assertIn("multilingual", single_publish_description)
        self.assertIn("publish_knowledge_article", single_publish_description)
        self.assertIn("Never disable", single_publish_description)
        bulk_publish_description = protocol_tools[
            "publish_knowledge_article"
        ].description
        self.assertIn("required", bulk_publish_description)
        self.assertIn("preRelease=true", bulk_publish_description)
        self.assertIn(
            "return public URLs",
            protocol_tools["upload_knowledge_article_attachments"].description,
        )

        self.assertIn("Knowledge Base Operations (MANDATORY WORKFLOW)", instructions)
        self.assertIn("no global article list", instructions)
        self.assertIn("partialErrors", instructions)
        self.assertIn("strict base64", instructions)
        self.assertIn("list_knowledge_articles", instructions)
        self.assertIn("preRelease=true", instructions)
        self.assertIn("Never disable `pre_release`", instructions)


if __name__ == "__main__":
    unittest.main()
