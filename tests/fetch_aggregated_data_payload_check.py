import importlib.util
import sys
import types
import unittest
from pathlib import Path


def load_tool_module(filename, module_name):
    original_tools = sys.modules.get("tools")
    original_tools_analytics = sys.modules.get("tools.analytics")
    original_period_filter = sys.modules.get("tools.analytics.period_filter")
    original_tools_base = sys.modules.get("tools.base")

    tools_package = types.ModuleType("tools")
    tools_package.__path__ = [str(Path(__file__).resolve().parents[1] / "tools")]
    analytics_package = types.ModuleType("tools.analytics")
    analytics_package.__path__ = []
    tools_base = types.ModuleType("tools.base")
    tools_base.get_dixa_client = lambda: None

    sys.modules["tools"] = tools_package
    sys.modules["tools.analytics"] = analytics_package
    sys.modules["tools.base"] = tools_base

    try:
        period_filter_path = (
            Path(__file__).resolve().parents[1]
            / "tools"
            / "analytics"
            / "period_filter.py"
        )
        period_filter_spec = importlib.util.spec_from_file_location(
            "tools.analytics.period_filter",
            period_filter_path,
        )
        period_filter_module = importlib.util.module_from_spec(period_filter_spec)
        sys.modules["tools.analytics.period_filter"] = period_filter_module
        period_filter_spec.loader.exec_module(period_filter_module)

        module_path = (
            Path(__file__).resolve().parents[1]
            / "tools"
            / "analytics"
            / filename
        )
        spec = importlib.util.spec_from_file_location(
            module_name,
            module_path,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if original_tools is None:
            sys.modules.pop("tools", None)
        else:
            sys.modules["tools"] = original_tools

        if original_tools_analytics is None:
            sys.modules.pop("tools.analytics", None)
        else:
            sys.modules["tools.analytics"] = original_tools_analytics

        if original_period_filter is None:
            sys.modules.pop("tools.analytics.period_filter", None)
        else:
            sys.modules["tools.analytics.period_filter"] = original_period_filter

        if original_tools_base is None:
            sys.modules.pop("tools.base", None)
        else:
            sys.modules["tools.base"] = original_tools_base


fetch_module = load_tool_module(
    "fetch_aggregated_data.py",
    "fetch_aggregated_data_under_test",
)
records_module = load_tool_module(
    "fetch_unaggregated_data.py",
    "fetch_unaggregated_data_under_test",
)


class CapturingClient:
    def __init__(self):
        self.request = None

    def post_analytics_metric_data(self, request):
        self.request = request
        return {"data": {"id": request["id"]}}

    def post_analytics_metric_records_data(self, request, page_key=None, page_limit=None):
        self.request = request
        self.page_key = page_key
        self.page_limit = page_limit
        return {"data": []}


class FetchAggregatedDataTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = CapturingClient()
        self.original_get_dixa_client = fetch_module.get_dixa_client
        fetch_module.get_dixa_client = lambda: self.client

    async def asyncTearDown(self):
        fetch_module.get_dixa_client = self.original_get_dixa_client

    async def test_period_filter_normalizes_shorthand_and_omits_csid_filter(self):
        await fetch_module.fetch_aggregated_data(
            metric_id="closed_conversations",
            timezone="Europe/Copenhagen",
            period_filter={"start": "2026-01-01", "end": "2026-01-31"},
            aggregations=["Count"],
        )

        self.assertNotIn("csidFilter", self.client.request)
        self.assertEqual([], self.client.request["filters"])
        self.assertEqual(
            {
                "_type": "Interval",
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-31T00:00:00Z",
            },
            self.client.request["periodFilter"],
        )

    async def test_csid_filter_serializes_provided_ids(self):
        await fetch_module.fetch_aggregated_data(
            metric_id="closed_conversations",
            timezone="Europe/Copenhagen",
            csid_filter=[12345, 12346],
        )

        self.assertEqual([12345, 12346], self.client.request["csidFilter"])
        self.assertEqual([], self.client.request["filters"])
        self.assertNotIn("periodFilter", self.client.request)

    async def test_filters_only_omits_csid_filter(self):
        await fetch_module.fetch_aggregated_data(
            metric_id="closed_conversations",
            timezone="Europe/Copenhagen",
            filters=[{"attribute": "channel", "values": ["email"]}],
        )

        self.assertNotIn("csidFilter", self.client.request)
        self.assertNotIn("periodFilter", self.client.request)


class FetchUnaggregatedDataTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = CapturingClient()
        self.original_get_dixa_client = records_module.get_dixa_client
        records_module.get_dixa_client = lambda: self.client

    async def asyncTearDown(self):
        records_module.get_dixa_client = self.original_get_dixa_client

    async def test_period_filter_normalizes_shorthand_and_omits_csid_filter(self):
        await records_module.fetch_unaggregated_data(
            record_id="conversations_transferred_to_queue",
            timezone="UTC",
            period_filter={"start": "2026-01-01", "end": "2026-06-05"},
        )

        self.assertNotIn("csidFilter", self.client.request)
        self.assertEqual([], self.client.request["filters"])
        self.assertEqual(
            {
                "_type": "Interval",
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-06-05T00:00:00Z",
            },
            self.client.request["periodFilter"],
        )

    async def test_csid_filter_serializes_empty_filters(self):
        await records_module.fetch_unaggregated_data(
            record_id="conversations_transferred_to_queue",
            timezone="UTC",
            csid_filter=[12345],
        )

        self.assertEqual([12345], self.client.request["csidFilter"])
        self.assertEqual([], self.client.request["filters"])
        self.assertNotIn("periodFilter", self.client.request)


if __name__ == "__main__":
    unittest.main()
