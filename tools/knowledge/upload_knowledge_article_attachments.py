"""Tool for uploading knowledge article attachments through the Dixa API.

⚠️ WARNING: This is a MODIFICATION endpoint that modifies data.
The AI assistant MUST obtain explicit user confirmation before calling this tool.
"""

import base64
import binascii
from typing import Any, Dict, List

from tools.base import get_dixa_client
from tools.knowledge.schemas import KnowledgeAttachmentList


async def upload_knowledge_article_attachments(
    files: KnowledgeAttachmentList,
) -> Dict[str, Any]:
    """Upload images and return public URLs for later article HTML updates.

    This tool only uploads files; it does not attach them to an article or
    change translation content. After upload, take each successful public URL
    from ``data`` and reference it in a later
    ``modify_knowledge_article_translations`` HTML ``content`` value. The
    request can partially succeed.

    ⚠️ WARNING: This uploads data to the Dixa organization.
    The AI assistant MUST obtain explicit confirmation of the exact filenames
    and image contents before executing this tool.

    Args:
        files: One to five objects containing ``filename``, ``media_type``, and
            ``content_base64`` containing only the base64 encoding of the raw
            image bytes. Do not include a data-URL prefix such as
            ``data:image/png;base64,``. Server-local paths and remote URLs are
            not accepted as file content. Dixa supports PNG, JPEG, GIF, and
            WebP, with limits of 4 MB per file and 10 MB total per request.

    Returns:
        The unchanged Dixa response. ``data`` contains each successful
        ``originalFilename`` and public ``url``; ``partialErrors`` identifies
        failed files with their filename, message, and code. Always inspect and
        report both, and do not claim the whole request succeeded when any
        partial error is present.

    Raises:
        ValueError: If the file count or object shape is invalid, or if any
            ``content_base64`` value is not strict base64.
    """
    if not isinstance(files, list) or not 1 <= len(files) <= 5:
        raise ValueError("files must contain between 1 and 5 attachment objects")

    decoded_files: List[Dict[str, Any]] = []
    required_fields = ("filename", "media_type", "content_base64")

    for index, file_data in enumerate(files):
        if not isinstance(file_data, dict):
            raise ValueError(f"files[{index}] must be an object")

        for field in required_fields:
            if field not in file_data or not isinstance(file_data[field], str):
                raise ValueError(f"files[{index}].{field} must be a string")

        try:
            content = base64.b64decode(file_data["content_base64"], validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError(
                f"files[{index}].content_base64 must be valid base64"
            ) from exc

        decoded_files.append(
            {
                "filename": file_data["filename"],
                "media_type": file_data["media_type"],
                "content": content,
            }
        )

    client = get_dixa_client()
    return client.upload_knowledge_article_attachments(files=decoded_files)
