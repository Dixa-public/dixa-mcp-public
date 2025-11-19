"""
Knowledge-related API methods for DixaClient.
"""

import requests
from typing import Dict, Any, Optional, List, Literal
from requests.exceptions import RequestException, HTTPError

def get_knowledge_articles(
    self,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all knowledge articles.
        
    Args:
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.
        
    Returns:
        Dictionary containing the list of knowledge articles.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/knowledge/articles"
        
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers, params=params if params else None)
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
    


def get_knowledge_article(
    self,
    article_id: str
) -> Dict[str, Any]:
    """
    Get a knowledge article by ID.
        
    Args:
        article_id: The ID of the knowledge article to retrieve (required).
        
    Returns:
        Dictionary containing the knowledge article information.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/knowledge/articles/{article_id}"
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers)
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
    


def create_knowledge_article(
    self,
    title: str,
    content: str,
    category_id: Optional[str] = None,
    published: Optional[bool] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a knowledge article.
        
    Args:
        title: The title of the article (required).
        content: The content of the article (required).
        category_id: The ID of the category to assign the article to (optional).
        published: Whether the article should be published (optional).
        **kwargs: Additional article properties as per Dixa API specification.
        
    Returns:
        Dictionary containing the created knowledge article.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/knowledge/articles"
        
    payload = {
        "title": title,
        "content": content
    }
        
    if category_id:
        payload["categoryId"] = category_id
    if published is not None:
        payload["published"] = published
        
    # Add any additional kwargs
    payload.update(kwargs)
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.post(url, json=payload, headers=headers)
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
    


def patch_knowledge_article(
    self,
    article_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    category_id: Optional[str] = None,
    published: Optional[bool] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Update a knowledge article (partial update).
        
    Args:
        article_id: The ID of the article to update (required).
        title: The title of the article (optional).
        content: The content of the article (optional).
        category_id: The ID of the category to assign the article to (optional).
        published: Whether the article should be published (optional).
        **kwargs: Additional article properties as per Dixa API specification.
        
    Returns:
        Dictionary containing the updated knowledge article.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/knowledge/articles/{article_id}"
        
    payload = {}
        
    if title is not None:
        payload["title"] = title
    if content is not None:
        payload["content"] = content
    if category_id is not None:
        payload["categoryId"] = category_id
    if published is not None:
        payload["published"] = published
        
    # Add any additional kwargs
    payload.update(kwargs)
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.patch(url, json=payload, headers=headers)
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
    


def delete_knowledge_article(
    self,
    article_id: str
) -> Dict[str, Any]:
    """
    Delete a knowledge article.
        
    Args:
        article_id: The ID of the article to delete (required).
        
    Returns:
        Dictionary with success status. On success (204), returns {"success": True, "message": "Knowledge article deleted successfully"}.
        On error, returns the error response.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/knowledge/articles/{article_id}"
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True, "message": "Knowledge article deleted successfully"}
        if response.content:
            return response.json()
        return {"success": True}
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
    


def get_knowledge_categories(
    self,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all knowledge categories.
        
    Args:
        page_key: Optional pagination key for retrieving the next page of results.
        page_limit: Optional limit for the number of results per page.
        
    Returns:
        Dictionary containing the list of knowledge categories.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/knowledge/categories"
        
    params = {}
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit
        
    headers = {
        **self.headers
    }
        
    try:
        response = requests.get(url, headers=headers, params=params if params else None)
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
    


def create_knowledge_category(
    self,
    name: str,
    parent_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a knowledge category.
        
    Args:
        name: The name of the category (required).
        parent_id: The ID of the parent category (optional).
        **kwargs: Additional category properties as per Dixa API specification.
        
    Returns:
        Dictionary containing the created knowledge category.
        
    Raises:
        HTTPError: If the API returns an HTTP error status (4xx, 5xx).
        RequestException: If there's an error making the request.
    """
    url = f"{self.base_url}/knowledge/categories"
        
    payload = {
        "name": name
    }
        
    if parent_id:
        payload["parentId"] = parent_id
        
    # Add any additional kwargs
    payload.update(kwargs)
        
    headers = {
        "Content-Type": "application/json",
        **self.headers
    }
        
    try:
        response = requests.post(url, json=payload, headers=headers)
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

