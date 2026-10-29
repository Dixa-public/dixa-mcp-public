"""Knowledge-related API methods for :class:`DixaClient`."""

from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.exceptions import HTTPError, RequestException
from dixa_api.http import api_request


MultipartFile = Tuple[str, Tuple[str, bytes, str]]


def _knowledge_request(
    self,
    method: str,
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json_payload: Optional[Dict[str, Any]] = None,
    files: Optional[List[MultipartFile]] = None,
) -> Dict[str, Any]:
    """Send a Knowledge API request and apply consistent response handling."""
    url = f"{self.base_url}{path}"
    headers = {**self.headers}
    request_kwargs: Dict[str, Any] = {"headers": headers}

    if params:
        request_kwargs["params"] = params
    if json_payload is not None:
        headers["Content-Type"] = "application/json"
        request_kwargs["json"] = json_payload
    if files is not None:
        request_kwargs["files"] = files

    try:
        response = requests.request(method, url, **request_kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return {"success": True}
        return response.json()
    except HTTPError as exc:
        error_message = f"HTTP {response.status_code} error: {exc}"
        try:
            error_message += f" - {response.json()}"
        except ValueError:
            error_message += f" - {response.text}"
        raise HTTPError(error_message, response=response) from exc
    except RequestException as exc:
        raise RequestException(f"Request failed: {exc}") from exc


def get_knowledge_collections(
    self,
    page_key: Optional[str] = None,
    page_limit: Optional[int] = None,
) -> Dict[str, Any]:
    """List knowledge collections."""
    params: Dict[str, Any] = {}
    if page_key is not None:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = page_limit
    return _knowledge_request(
        self,
        "GET",
        "/knowledge/collections",
        params=params,
    )


def get_knowledge_collection(
    self,
    collection_id: str,
) -> Dict[str, Any]:
    """Get a knowledge collection by ID."""
    return _knowledge_request(
        self,
        "GET",
        f"/knowledge/collections/{collection_id}",
    )


def get_knowledge_collection_catalog(
    self,
    collection_id: str,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the category and article catalog for a knowledge collection."""
    params = {"language": language} if language is not None else None
    return _knowledge_request(
        self,
        "GET",
        f"/knowledge/collections/{collection_id}/catalog",
        params=params,
    )


def get_knowledge_category(
    self,
    category_id: str,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a knowledge category by ID."""
    params = {"language": language} if language is not None else None
    return _knowledge_request(
        self,
        "GET",
        f"/knowledge/categories/{category_id}",
        params=params,
    )


def get_knowledge_category_translations(
    self,
    category_id: str,
) -> Dict[str, Any]:
    """Get all translations for a knowledge category."""
    return _knowledge_request(
        self,
        "GET",
        f"/knowledge/categories/{category_id}/translations",
    )


def get_knowledge_article(
    self,
    article_id: str,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a knowledge article by ID."""
    params = {"language": language} if language is not None else None
    return _knowledge_request(
        self,
        "GET",
        f"/knowledge/articles/{article_id}",
        params=params,
    )


def get_knowledge_article_translations(
    self,
    article_id: str,
) -> Dict[str, Any]:
    """Get all translations for a knowledge article."""
    return _knowledge_request(
        self,
        "GET",
        f"/knowledge/articles/{article_id}/translations",
    )


def create_knowledge_category(
    self,
    parent_id: str,
    translations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Create a knowledge category under a collection or another category."""
    payload: Dict[str, Any] = {"parentId": parent_id}
    if translations is not None:
        payload["translations"] = translations
    return _knowledge_request(
        self,
        "POST",
        "/knowledge/categories",
        json_payload=payload,
    )


def create_knowledge_article(
    self,
    translations: Optional[List[Dict[str, Any]]] = None,
    parent_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    pre_release: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a knowledge article, applying Dixa's creation constraints."""
    if pre_release is True and (not parent_id or not parent_id.strip()):
        raise ValueError(
            "parent_id is required when pre_release=True. Call "
            "list_knowledge_collections, then fetch_knowledge_collection_catalog "
            "to select a parent category. Keep the requested pre_release setting."
        )
    payload: Dict[str, Any] = {}
    if translations is not None:
        payload["translations"] = translations
    if parent_id is not None:
        payload["parentId"] = parent_id
    # Dixa rejects an explicit empty tag list; omission creates an untagged article.
    if tags:
        payload["tags"] = tags
    if pre_release is not None:
        payload["preRelease"] = pre_release
    return _knowledge_request(
        self,
        "POST",
        "/knowledge/articles",
        json_payload=payload,
    )


def patch_knowledge_article(
    self,
    article_id: str,
    owned_by: Optional[str] = None,
    tags: Optional[Dict[str, List[str]]] = None,
    pre_release: Optional[bool] = None,
) -> Dict[str, Any]:
    """Partially update a knowledge article."""
    payload: Dict[str, Any] = {}
    if owned_by is not None:
        payload["ownedBy"] = owned_by
    if tags is not None:
        payload["tags"] = tags
    if pre_release is not None:
        payload["preRelease"] = pre_release
    return _knowledge_request(
        self,
        "PATCH",
        f"/knowledge/articles/{article_id}",
        json_payload=payload,
    )


def delete_knowledge_article(
    self,
    article_id: str,
) -> Dict[str, Any]:
    """Delete a knowledge article."""
    return _knowledge_request(
        self,
        "DELETE",
        f"/knowledge/articles/{article_id}",
    )


def patch_knowledge_article_translations(
    self,
    article_id: str,
    translations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Create or update knowledge article translations."""
    payload: Dict[str, Any] = {}
    if translations is not None:
        payload["translations"] = translations
    return _knowledge_request(
        self,
        "PATCH",
        f"/knowledge/articles/{article_id}/translations",
        json_payload=payload,
    )


def delete_knowledge_article_translation(
    self,
    article_id: str,
    language_id: str,
) -> Dict[str, Any]:
    """Delete one translation from a knowledge article."""
    return _knowledge_request(
        self,
        "DELETE",
        f"/knowledge/articles/{article_id}/translations/{language_id}",
    )


def publish_knowledge_article_translation(
    self,
    article_id: str,
    language_id: str,
) -> Dict[str, Any]:
    """Publish one knowledge article translation."""
    return _knowledge_request(
        self,
        "POST",
        f"/knowledge/articles/{article_id}/translations/{language_id}/publish",
    )


def unpublish_knowledge_article_translation(
    self,
    article_id: str,
    language_id: str,
) -> Dict[str, Any]:
    """Unpublish one knowledge article translation."""
    return _knowledge_request(
        self,
        "POST",
        f"/knowledge/articles/{article_id}/translations/{language_id}/unpublish",
    )


def publish_knowledge_article(
    self,
    article_id: str,
) -> Dict[str, Any]:
    """Publish every translation for a knowledge article."""
    return _knowledge_request(
        self,
        "POST",
        f"/knowledge/articles/{article_id}/publish",
    )


def unpublish_knowledge_article(
    self,
    article_id: str,
) -> Dict[str, Any]:
    """Unpublish every translation for a knowledge article."""
    return _knowledge_request(
        self,
        "POST",
        f"/knowledge/articles/{article_id}/unpublish",
    )


def move_knowledge_article(
    self,
    article_id: str,
    parent_id: str,
) -> Dict[str, Any]:
    """Move a knowledge article to a category."""
    return _knowledge_request(
        self,
        "PATCH",
        f"/knowledge/articles/{article_id}/parent/{parent_id}",
    )


def delete_knowledge_article_parent(
    self,
    article_id: str,
) -> Dict[str, Any]:
    """Remove a knowledge article from its parent category."""
    return _knowledge_request(
        self,
        "DELETE",
        f"/knowledge/articles/{article_id}/parent",
    )


def upload_knowledge_article_attachments(
    self,
    files: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Upload decoded in-memory files as knowledge article attachments."""
    multipart_files: List[MultipartFile] = [
        (
            "files",
            (
                attachment["filename"],
                attachment["content"],
                attachment["media_type"],
            ),
        )
        for attachment in files
    ]
    return _knowledge_request(
        self,
        "POST",
        "/knowledge/articles/attachments",
        files=multipart_files,
    )


def create_knowledge_collection(
    self,
    title: str,
    description: Optional[str] = None,
    internal_kb_enabled: Optional[bool] = None,
) -> Dict[str, Any]:
    """Call POST /knowledge/collections."""
    return api_request(
        self,
        'POST',
        '/knowledge/collections',
        payload={key: value for key, value in {'title': title, 'description': description, 'internalKbEnabled': internal_kb_enabled}.items() if value is not None},
    )
