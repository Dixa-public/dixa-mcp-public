"""
Analytics-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List
from requests.exceptions import RequestException, HTTPError


def get_analytics_filter_values(
    self,
    filter_attribute: str,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get possible values to be used with a given filter attribute.
    Filter attributes are not metric or record specific, so one filter attribute can be used with multiple metrics/records.
    When a filter value is not relevant for a specific metric/record, it is simply ignored.

    Args:
        filter_attribute: The filter attribute name (required).
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.

    Returns:
        Dictionary containing the possible filter values.

    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/analytics/filter/{filter_attribute}"
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit

    try:
        response = requests.get(url, headers=self.headers, params=params if params else None)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e


def get_analytics_metrics_catalogue(
    self,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all available metric IDs that can be used to fetch data in Get Metric Data.

    Args:
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.

    Returns:
        Dictionary containing the catalogue of metrics.

    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/analytics/metrics"
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit

    try:
        response = requests.get(url, headers=self.headers, params=params if params else None)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e


def get_analytics_metric_description(self, metric_id: str) -> Dict[str, Any]:
    """
    List all available properties of a metric to use for querying its data.

    Args:
        metric_id: The ID of the metric (required).

    Returns:
        Dictionary containing the metric properties including filters, aggregations, and field metadata.

    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/analytics/metrics/{metric_id}"
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e


def post_analytics_metric_data(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get data of a specific metric (aggregated).

    Args:
        request: The request body containing:
            - id (required): The metric ID
            - timezone (required): The timezone (e.g., "Europe/Copenhagen")
            - periodFilter (optional): Period filter object
            - csidFilter (optional): Array of conversation IDs to filter by
            - filters (optional): Array of filter objects
            - aggregations (optional): Array of aggregation strings

    Returns:
        Dictionary containing the metric data.

    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/analytics/metrics"
    headers = {"Content-Type": "application/json", **self.headers}
    try:
        response = requests.post(url, json=request, headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e


def get_analytics_records_catalogue(
    self,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all available metric record IDs that can be used to fetch unaggregated data.

    Args:
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.

    Returns:
        Dictionary containing the catalogue of metric records.

    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/analytics/records"
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit

    try:
        response = requests.get(url, headers=self.headers, params=params if params else None)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e


def get_analytics_record_description(self, record_id: str) -> Dict[str, Any]:
    """
    List all available properties of a metric record to use for querying its data.

    Args:
        record_id: The ID of the metric record (required).

    Returns:
        Dictionary containing the metric record properties including filters and field metadata.

    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/analytics/records/{record_id}"
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e


def post_analytics_metric_records_data(
    self,
    request: Dict[str, Any],
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get data of specific metric records (unaggregated).

    Args:
        request: The request body containing:
            - id (required): The metric record ID
            - timezone (required): The timezone (e.g., "Europe/Copenhagen")
            - periodFilter (optional): Period filter object
            - csidFilter (optional): Array of conversation IDs to filter by
            - filters (optional): Array of filter objects
        page_key: Optional pagination key for retrieving the next page of results.
            When provided, should be used as a query parameter with the same POST request and payload.
            Can be used together with page_limit to change the number of results.
        page_limit: Optional limit for the number of results per page.
            Can be used with or without page_key. When used with page_key, it overrides the page size encoded in the key.

    Returns:
        Dictionary containing the metric records data.

    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/analytics/records"
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit

    headers = {"Content-Type": "application/json", **self.headers}
    try:
        # Always use POST request, even when pageKey is provided
        # The pageKey is just a query parameter, but the same payload should be sent
        response = requests.post(url, json=request, headers=headers, params=params if params else None)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_msg = f"HTTP {response.status_code} error: {e}"
        try:
            error_detail = response.json()
            error_msg += f" - {error_detail}"
        except ValueError:
            error_msg += f" - {response.text}"
        raise HTTPError(error_msg, response=response) from e
    except RequestException as e:
        raise RequestException(f"Request failed: {e}") from e

