"""Knowledge tools for Dixa MCP."""

from tools.knowledge.add_knowledge_article import add_knowledge_article
from tools.knowledge.add_knowledge_category import add_knowledge_category
from tools.knowledge.fetch_knowledge_article_by_id import fetch_knowledge_article_by_id
from tools.knowledge.fetch_knowledge_article_translations import fetch_knowledge_article_translations
from tools.knowledge.fetch_knowledge_category_by_id import fetch_knowledge_category_by_id
from tools.knowledge.fetch_knowledge_category_translations import fetch_knowledge_category_translations
from tools.knowledge.fetch_knowledge_collection_by_id import fetch_knowledge_collection_by_id
from tools.knowledge.fetch_knowledge_collection_catalog import fetch_knowledge_collection_catalog
from tools.knowledge.list_knowledge_collections import list_knowledge_collections
from tools.knowledge.modify_knowledge_article import modify_knowledge_article
from tools.knowledge.modify_knowledge_article_translations import modify_knowledge_article_translations
from tools.knowledge.move_knowledge_article import move_knowledge_article
from tools.knowledge.publish_knowledge_article import publish_knowledge_article
from tools.knowledge.publish_knowledge_article_translation import publish_knowledge_article_translation
from tools.knowledge.remove_knowledge_article import remove_knowledge_article
from tools.knowledge.remove_knowledge_article_parent import remove_knowledge_article_parent
from tools.knowledge.remove_knowledge_article_translation import remove_knowledge_article_translation
from tools.knowledge.unpublish_knowledge_article import unpublish_knowledge_article
from tools.knowledge.unpublish_knowledge_article_translation import unpublish_knowledge_article_translation
from tools.knowledge.upload_knowledge_article_attachments import upload_knowledge_article_attachments
from tools.knowledge.add_knowledge_collection import add_knowledge_collection

__all__ = [
    'list_knowledge_collections',
    'fetch_knowledge_collection_by_id',
    'fetch_knowledge_collection_catalog',
    'fetch_knowledge_category_by_id',
    'fetch_knowledge_category_translations',
    'fetch_knowledge_article_by_id',
    'fetch_knowledge_article_translations',
    'add_knowledge_category',
    'add_knowledge_article',
    'modify_knowledge_article',
    'remove_knowledge_article',
    'modify_knowledge_article_translations',
    'remove_knowledge_article_translation',
    'publish_knowledge_article_translation',
    'unpublish_knowledge_article_translation',
    'publish_knowledge_article',
    'unpublish_knowledge_article',
    'move_knowledge_article',
    'remove_knowledge_article_parent',
    'upload_knowledge_article_attachments',
    'add_knowledge_collection',
]
