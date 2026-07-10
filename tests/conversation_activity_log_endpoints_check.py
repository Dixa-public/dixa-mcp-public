import unittest
from unittest.mock import Mock, patch

from dixa_api import DixaClient
from dixa_api import conversations


class ConversationActivityLogEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = DixaClient(api_key="test-api-key")

    def assert_activity_log_request(self, invoke, expected_url):
        payload = {"data": []}
        response = Mock()
        response.json.return_value = payload

        with patch.object(
            conversations.requests,
            "get",
            return_value=response,
        ) as request_get:
            result = invoke()

        request_get.assert_called_once_with(
            expected_url,
            headers={"Authorization": "test-api-key"},
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(payload, result)

    def test_conversation_activity_log_uses_activitylog_endpoint(self):
        self.assert_activity_log_request(
            lambda: self.client.get_conversation_activity_log("895868"),
            "https://dev.dixa.io/v1/conversations/895868/activitylog",
        )

    def test_organization_activity_log_uses_activitylog_endpoint(self):
        self.assert_activity_log_request(
            self.client.get_organization_activity_log,
            "https://dev.dixa.io/v1/conversations/activitylog",
        )


if __name__ == "__main__":
    unittest.main()
