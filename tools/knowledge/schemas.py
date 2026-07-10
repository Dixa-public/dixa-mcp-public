"""Structured and documented input schemas exposed by Knowledge MCP tools."""

import json
from typing import Any, List

from pydantic import BeforeValidator, Field
from typing_extensions import Annotated, TypedDict


def _decode_json_array(value: Any) -> Any:
    """Accept either a native array or a client-supplied JSON-encoded array."""
    if not isinstance(value, str):
        return value

    try:
        decoded = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError("Input must be a list or a valid JSON-encoded list") from exc

    if not isinstance(decoded, list):
        raise ValueError("JSON-encoded input must decode to a list")
    return decoded


def _decode_json_object(value: Any) -> Any:
    """Accept either a native object or a client-supplied JSON-encoded object."""
    if not isinstance(value, str):
        return value

    try:
        decoded = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError("Input must be an object or a valid JSON-encoded object") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON-encoded input must decode to an object")
    return decoded


class KnowledgeTranslationRequired(TypedDict):
    """Required fields for a knowledge article translation."""

    languageId: Annotated[
        str,
        Field(description="ISO language code accepted by Dixa, such as en or da."),
    ]
    title: Annotated[
        str,
        Field(description="Translated article title for this language."),
    ]


class KnowledgeTranslationInput(KnowledgeTranslationRequired, total=False):
    """A translated article title and optional HTML body."""

    content: Annotated[
        str,
        Field(description="Optional HTML article body for this draft translation."),
    ]


class KnowledgeTagUpdate(TypedDict, total=False):
    """Tag IDs to add to or remove from a knowledge article."""

    add: Annotated[
        List[str],
        Field(description="Tag IDs to add; an explicit empty list is preserved."),
    ]
    remove: Annotated[
        List[str],
        Field(description="Tag IDs to remove; an explicit empty list is preserved."),
    ]


class KnowledgeAttachmentInput(TypedDict):
    """A remote-safe base64 attachment supplied through MCP."""

    filename: Annotated[
        str,
        Field(description="Original image filename, including its extension."),
    ]
    media_type: Annotated[
        str,
        Field(description="Image MIME type: image/png, image/jpeg, image/gif, or image/webp."),
    ]
    content_base64: Annotated[
        str,
        Field(description="Raw strict-base64 image bytes; data-URL prefixes and file paths are not accepted."),
    ]


KnowledgeTranslationList = Annotated[
    List[KnowledgeTranslationInput],
    BeforeValidator(_decode_json_array),
]
KnowledgeTagIdList = Annotated[
    List[str],
    BeforeValidator(_decode_json_array),
]
KnowledgeTagUpdateInput = Annotated[
    KnowledgeTagUpdate,
    BeforeValidator(_decode_json_object),
]
KnowledgeAttachmentList = Annotated[
    List[KnowledgeAttachmentInput],
    BeforeValidator(_decode_json_array),
]


__all__ = [
    "KnowledgeAttachmentInput",
    "KnowledgeAttachmentList",
    "KnowledgeTagIdList",
    "KnowledgeTagUpdate",
    "KnowledgeTagUpdateInput",
    "KnowledgeTranslationInput",
    "KnowledgeTranslationList",
]
