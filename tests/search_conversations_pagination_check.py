import unittest
import importlib.util
import sys
import types
from pathlib import Path
from unittest.mock import Mock, patch


def load_conversations_module():
    original_requests = sys.modules.get("requests")
    original_requests_exceptions = sys.modules.get("requests.exceptions")

    requests_module = types.ModuleType("requests")
    requests_module.post = Mock()
    requests_exceptions = types.ModuleType("requests.exceptions")
    requests_exceptions.RequestException = Exception
    requests_exceptions.HTTPError = Exception
    requests_module.exceptions = requests_exceptions

    sys.modules["requests"] = requests_module
    sys.modules["requests.exceptions"] = requests_exceptions

    try:
        module_path = Path(__file__).resolve().parents[1] / "dixa_api" / "conversations.py"
        spec = importlib.util.spec_from_file_location(
            "dixa_api_conversations_under_test",
            module_path,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if original_requests is None:
            sys.modules.pop("requests", None)
        else:
            sys.modules["requests"] = original_requests

        if original_requests_exceptions is None:
            sys.modules.pop("requests.exceptions", None)
        else:
            sys.modules["requests.exceptions"] = original_requests_exceptions


conversations_module = load_conversations_module()


class SearchConversationsPaginationTests(unittest.TestCase):
    def test_page_key_is_decoded_before_request_params_are_encoded(self):
        client = Mock()
        client.base_url = "https://dev.dixa.io/v1"
        client.headers = {"Authorization": "Bearer test-token"}

        response = Mock()
        response.json.return_value = {"data": []}
        response.raise_for_status.return_value = None

        encoded_page_key = "cGFnZUxpbWl0PTUwJnBhZ2U9MQ%3D%3D:"

        with patch.object(conversations_module.requests, "post", return_value=response) as post:
            conversations_module.post_search_conversations(
                client,
                page_key=encoded_page_key,
                page_limit=20,
            )

        _, kwargs = post.call_args
        self.assertEqual(
            "cGFnZUxpbWl0PTUwJnBhZ2U9MQ==:",
            kwargs["params"]["pageKey"],
        )
        self.assertEqual(20, kwargs["params"]["pageLimit"])


if __name__ == "__main__":
    unittest.main()
