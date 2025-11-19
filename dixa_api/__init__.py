"""
Dixa API Client Package

This package provides a modular DixaClient class split across multiple modules
for better organization and maintainability.
"""

from dixa_api.client import DixaClient

# Import all method modules
from dixa_api import organization
from dixa_api import agents
from dixa_api import settings
from dixa_api import conversations
from dixa_api import custom_attributes
from dixa_api import users
from dixa_api import knowledge
from dixa_api import queues
from dixa_api import tags
from dixa_api import teams
from dixa_api import analytics

# Attach all methods to DixaClient class
# Organization
DixaClient.get_organization = organization.get_organization

# Agents
DixaClient.get_agent = agents.get_agent
DixaClient.get_agents = agents.get_agents
DixaClient.get_agents_presence = agents.get_agents_presence
DixaClient.get_agent_teams = agents.get_agent_teams
DixaClient.create_agent = agents.create_agent
DixaClient.patch_agent = agents.patch_agent
DixaClient.update_agent = agents.update_agent
DixaClient.update_agent_working_channel = agents.update_agent_working_channel

# Settings
DixaClient.get_business_hours_status = settings.get_business_hours_status
DixaClient.get_business_hours_schedules = settings.get_business_hours_schedules
DixaClient.get_contact_endpoints = settings.get_contact_endpoints
DixaClient.get_contact_endpoint = settings.get_contact_endpoint

# Conversations
DixaClient.create_conversation_note = conversations.create_conversation_note
DixaClient.create_conversation_notes_bulk = conversations.create_conversation_notes_bulk
DixaClient.patch_conversation_anonymize = conversations.patch_conversation_anonymize
DixaClient.patch_conversation_message_anonymize = conversations.patch_conversation_message_anonymize
DixaClient.create_conversation_tags_bulk = conversations.create_conversation_tags_bulk
DixaClient.update_conversation_claim = conversations.update_conversation_claim
DixaClient.update_conversation_close = conversations.update_conversation_close
DixaClient.create_conversation = conversations.create_conversation
DixaClient.get_conversation = conversations.get_conversation
DixaClient.get_conversation_flows = conversations.get_conversation_flows
DixaClient.get_conversation_activity_log = conversations.get_conversation_activity_log
DixaClient.update_conversation_link = conversations.update_conversation_link
DixaClient.create_conversations_import = conversations.create_conversations_import
DixaClient.get_conversation_notes = conversations.get_conversation_notes
DixaClient.get_conversation_linked = conversations.get_conversation_linked
DixaClient.get_conversation_messages = conversations.get_conversation_messages
DixaClient.get_organization_activity_log = conversations.get_organization_activity_log
DixaClient.get_conversation_ratings = conversations.get_conversation_ratings
DixaClient.patch_conversation_custom_attributes = conversations.patch_conversation_custom_attributes
DixaClient.update_conversation_reopen = conversations.update_conversation_reopen
DixaClient.post_search_conversations = conversations.post_search_conversations
DixaClient.update_conversation_tag = conversations.update_conversation_tag
DixaClient.delete_conversation_tag = conversations.delete_conversation_tag
DixaClient.update_conversation_followup = conversations.update_conversation_followup

# Custom Attributes
DixaClient.get_custom_attribute = custom_attributes.get_custom_attribute
DixaClient.get_custom_attributes = custom_attributes.get_custom_attributes
DixaClient.patch_end_user_custom_attributes = custom_attributes.patch_end_user_custom_attributes

# Users (End Users)
DixaClient.get_end_users = users.get_end_users
DixaClient.get_end_user = users.get_end_user
DixaClient.create_end_user = users.create_end_user
DixaClient.create_end_users_bulk = users.create_end_users_bulk
DixaClient.patch_end_user = users.patch_end_user
DixaClient.patch_end_users_bulk = users.patch_end_users_bulk
DixaClient.update_end_user = users.update_end_user
DixaClient.update_end_users_bulk = users.update_end_users_bulk
DixaClient.get_end_user_conversations = users.get_end_user_conversations
DixaClient.patch_end_user_anonymize = users.patch_end_user_anonymize

# Knowledge
DixaClient.get_knowledge_articles = knowledge.get_knowledge_articles
DixaClient.get_knowledge_article = knowledge.get_knowledge_article
DixaClient.create_knowledge_article = knowledge.create_knowledge_article
DixaClient.patch_knowledge_article = knowledge.patch_knowledge_article
DixaClient.delete_knowledge_article = knowledge.delete_knowledge_article
DixaClient.get_knowledge_categories = knowledge.get_knowledge_categories
DixaClient.create_knowledge_category = knowledge.create_knowledge_category

# Queues
DixaClient.get_queues = queues.get_queues
DixaClient.get_queue = queues.get_queue
DixaClient.get_queue_availability = queues.get_queue_availability
DixaClient.get_queue_conversation_position = queues.get_queue_conversation_position
DixaClient.get_queue_agents = queues.get_queue_agents
DixaClient.create_queue = queues.create_queue
DixaClient.patch_queue_assign_agents = queues.patch_queue_assign_agents
DixaClient.delete_queue_remove_agents = queues.delete_queue_remove_agents

# Tags
DixaClient.get_tags = tags.get_tags
DixaClient.get_tag = tags.get_tag
DixaClient.create_tag = tags.create_tag
DixaClient.patch_tag_activate = tags.patch_tag_activate
DixaClient.patch_tag_deactivate = tags.patch_tag_deactivate
DixaClient.delete_tag = tags.delete_tag
DixaClient.get_conversation_tags = tags.get_conversation_tags

# Teams
DixaClient.get_teams = teams.get_teams
DixaClient.get_team = teams.get_team
DixaClient.get_team_agents = teams.get_team_agents
DixaClient.get_team_presence = teams.get_team_presence
DixaClient.create_team = teams.create_team
DixaClient.patch_team_add_agents = teams.patch_team_add_agents
DixaClient.delete_team_remove_agents = teams.delete_team_remove_agents
DixaClient.delete_team = teams.delete_team

# Analytics
DixaClient.get_analytics_filter_values = analytics.get_analytics_filter_values
DixaClient.get_analytics_metrics_catalogue = analytics.get_analytics_metrics_catalogue
DixaClient.get_analytics_metric_description = analytics.get_analytics_metric_description
DixaClient.post_analytics_metric_data = analytics.post_analytics_metric_data
DixaClient.get_analytics_records_catalogue = analytics.get_analytics_records_catalogue
DixaClient.get_analytics_record_description = analytics.get_analytics_record_description
DixaClient.post_analytics_metric_records_data = analytics.post_analytics_metric_records_data

__all__ = ['DixaClient']

