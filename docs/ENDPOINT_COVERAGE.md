# Dixa v1 endpoint coverage

126 documented operations (123 current and 3 deprecated) are exposed through 124 MCP tools.
Inventory retrieved on 2026-10-29 from the [official OpenAPI specification](https://docs.dixa.io/openapi-specs/dixa-v1.json).
Some discovery tools combine multiple API operations; filter-value discovery also has a dedicated paginated tool.

The offline coverage test compares the pinned operation inventory with client routes and registered MCP tools.
New and corrected operations additionally run through MCP input validation and mocked HTTP serialization tests.
This proves local routing and request behavior, not live account permissions or upstream availability.

Every registered tool description includes prerequisite discovery/inspection calls, maintained in `tools/workflows.py`.
Use verified IDs already present in context or discover them first; inspect current state before mutations.
Messages require separate approval of exact content, recipients, destination, links and attachments.
Webhook creation/enabling requires approval of future deliveries. Mutation tools never authorize their own prerequisite mutations.

## Workflow examples

- Knowledge: `list_knowledge_collections` → `fetch_knowledge_collection_catalog` → select and inspect the parent → confirm → `add_knowledge_category`. Use `add_knowledge_collection` only after separately approved creation if a new collection is needed.
- Messages: `search_conversations` → `fetch_conversation_by_id` → resolve author/recipient IDs → confirm the final message and attachments → `add_conversation_message`.
- Ratings: fetch the conversation and existing ratings → obtain an offer ID from an existing offer or a separately approved `create_conversation_rating_offer` → confirm the actual customer response → `submit_conversation_rating_result`.
- Webhooks: `list_webhook_subscriptions` → `fetch_webhook_subscription` → `fetch_webhook_delivery_status` → `fetch_webhook_event_logs` for one subscribed event.
- Record analytics: summary discovery/query when applicable → `prepare_analytics_record_query` without an ID → with the chosen ID → `fetch_analytics_filter_values` as needed → `fetch_unaggregated_data` for one bounded page.
- Anonymization: resolve and confirm the target → resource-specific anonymization → preserve the returned request ID → `fetch_anonymization_status`. Polling must not trigger another anonymization.

## Compatibility changes

- `list_conversation_flows` accepts optional `channel`; it no longer requires a conversation ID and uses `GET /v1/conversations/flows`.
- `check_conversation_queue_position` requires only `conversation_id`; it no longer accepts `queue_id` and uses `GET /v1/queues/conversation-position/{csid}`.
- Bulk end-user PATCH and PUT now use `/v1/endusers`; bulk POST creation still uses `/v1/endusers/bulk`.
- Record tools are enabled. Page size defaults to 50, is capped at 100 on every request, and cursors are passed unchanged. No automatic full-dataset loops or silent truncation. Record preparation returns the upstream description; filter values are fetched separately.
- Webhook subscription responses redact authorization credentials and custom-header values. Omit unchanged credential fields from PATCH; never resend `[REDACTED]`.
- Deprecated search, singular ratings, and generic anonymization tools are explicitly marked compatibility-only and point to their replacements.

## Verification

```bash
.venv/bin/python -B -m unittest discover -s tests -p '*_check.py' -v
```

Update `tests/fixtures/dixa_v1_operations.json` when the published specification changes, then run the coverage test to identify gaps.

## Operation-to-tool mapping

| Method | Endpoint | Registered tools | Status |
|---|---|---|---|
| GET | `/v1/analytics/metrics` | `prepare_analytics_metric_query` | Current |
| POST | `/v1/analytics/metrics` | `fetch_aggregated_data` | Current |
| GET | `/v1/analytics/metrics/{metricId}` | `prepare_analytics_metric_query` | Current |
| GET | `/v1/analytics/filter/{filterAttribute}` | `fetch_analytics_filter_values`, `prepare_analytics_metric_query` | Current |
| GET | `/v1/analytics/records` | `prepare_analytics_record_query` | Current |
| POST | `/v1/analytics/records` | `fetch_unaggregated_data` | Current |
| GET | `/v1/analytics/records/{recordId}` | `prepare_analytics_record_query` | Current |
| GET | `/v1/agents/presence` | `list_agents_presence` | Current |
| GET | `/v1/agents` | `list_agents` | Current |
| PUT | `/v1/agents` | `update_agents_bulk` | Current |
| POST | `/v1/agents` | `add_agent` | Current |
| PATCH | `/v1/agents` | `modify_agents_bulk` | Current |
| GET | `/v1/agents/{agentId}/teams` | `list_agent_teams` | Current |
| GET | `/v1/agents/{agentId}/presence` | `fetch_agent_presence` | Current |
| POST | `/v1/agents/bulk` | `add_agents_bulk` | Current |
| GET | `/v1/agents/{agentId}` | `fetch_agent_by_id` | Current |
| PUT | `/v1/agents/{agentId}` | `update_agent_full` | Current |
| DELETE | `/v1/agents/{agentId}` | `remove_agent` | Current |
| PATCH | `/v1/agents/{agentId}` | `modify_agent_partial` | Current |
| PUT | `/v1/agents/{agentId}/presence/working-channel` | `set_agent_working_channel` | Current |
| GET | `/v1/ai-agents` | `list_ai_agents` | Current |
| GET | `/v1/endusers` | `list_end_users` | Current |
| PUT | `/v1/endusers` | `update_end_users_bulk` | Current |
| POST | `/v1/endusers` | `add_end_user` | Current |
| PATCH | `/v1/endusers` | `modify_end_users_bulk` | Current |
| POST | `/v1/endusers/bulk` | `add_end_users_bulk` | Current |
| GET | `/v1/endusers/{userId}` | `fetch_end_user_by_id` | Current |
| PUT | `/v1/endusers/{userId}` | `update_end_user_full` | Current |
| PATCH | `/v1/endusers/{userId}` | `modify_end_user_partial` | Current |
| PATCH | `/v1/endusers/{userId}/anonymize` | `anonymize_end_user` | Current |
| PATCH | `/v1/endusers/{userId}/custom-attributes` | `update_end_user_custom_attributes` | Current |
| GET | `/v1/endusers/{userId}/conversations` | `list_end_user_conversations` | Current |
| GET | `/v1/teams` | `list_teams` | Current |
| POST | `/v1/teams` | `add_team` | Current |
| GET | `/v1/teams/{teamId}/agents` | `list_team_agents` | Current |
| DELETE | `/v1/teams/{teamId}/agents` | `remove_agents_from_team` | Current |
| PATCH | `/v1/teams/{teamId}/agents` | `add_agents_to_team` | Current |
| GET | `/v1/teams/{teamId}/presence` | `list_team_presence` | Current |
| GET | `/v1/teams/{teamId}` | `fetch_team_by_id` | Current |
| DELETE | `/v1/teams/{teamId}` | `remove_team` | Current |
| PATCH | `/v1/conversations/{conversationId}/anonymize` | `anonymize_conversation` | Current |
| PATCH | `/v1/conversations/{conversationId}/messages/{messageId}/anonymize` | `anonymize_conversation_message` | Current |
| PUT | `/v1/conversations/{conversationId}/close` | `close_conversation` | Current |
| PUT | `/v1/conversations/{conversationId}/followup` | `set_conversation_followup_status` | Current |
| PUT | `/v1/conversations/{conversationId}/reopen` | `reopen_conversation` | Current |
| PUT | `/v1/conversations/{conversationId}/transfer/queue` | `transfer_conversation_to_queue` | Current |
| POST | `/v1/conversations/{conversationId}/notes/bulk` | `add_conversation_notes_bulk` | Current |
| GET | `/v1/conversations/{conversationId}/notes` | `list_conversation_notes` | Current |
| POST | `/v1/conversations/{conversationId}/notes` | `add_conversation_note` | Current |
| POST | `/v1/conversations/{conversationId}/ratings/{ratingId}/submit` | `submit_conversation_rating_result` | Current |
| POST | `/v1/conversations/{conversationId}/ratings/offer` | `create_conversation_rating_offer` | Current |
| GET | `/v1/conversations/{conversationId}/rating` | `list_conversation_ratings_legacy` | Deprecated |
| GET | `/v1/conversations/{conversationId}/ratings` | `list_conversation_ratings` | Current |
| GET | `/v1/conversations/activitylog` | `list_organization_activity_log` | Current |
| GET | `/v1/conversations/flows` | `list_conversation_flows` | Current |
| PUT | `/v1/conversations/{conversationId}/tags/{tagId}` | `tag_conversation` | Current |
| DELETE | `/v1/conversations/{conversationId}/tags/{tagId}` | `remove_tag_from_conversation` | Current |
| POST | `/v1/conversations/{conversationId}/tags/bulk` | `tag_conversation_bulk` | Current |
| GET | `/v1/conversations/{conversationId}/tags` | `list_conversation_tags` | Current |
| GET | `/v1/conversations/{conversationId}/messages` | `list_conversation_messages` | Current |
| POST | `/v1/conversations/{conversationId}/messages` | `add_conversation_message` | Current |
| POST | `/v1/conversations` | `start_conversation` | Current |
| POST | `/v1/conversations/import` | `import_conversations` | Current |
| PATCH | `/v1/conversations/{conversationId}/custom-attributes` | `update_conversation_custom_attributes` | Current |
| PUT | `/v1/conversations/{conversationId}/claim` | `assign_conversation_to_agent` | Current |
| GET | `/v1/conversations/{conversationId}/activitylog` | `list_conversation_activity_log` | Current |
| GET | `/v1/conversations/{conversationId}` | `fetch_conversation_by_id` | Current |
| PUT | `/v1/conversations/{conversationId}/link` | `link_conversation_to_parent` | Current |
| GET | `/v1/conversations/{conversationId}/linked` | `list_linked_conversations` | Current |
| GET | `/v1/queues` | `list_queues` | Current |
| POST | `/v1/queues` | `add_queue` | Current |
| GET | `/v1/queues/{queueId}/members` | `list_queue_agents` | Current |
| DELETE | `/v1/queues/{queueId}/members` | `remove_agents_from_queue` | Current |
| PATCH | `/v1/queues/{queueId}/members` | `assign_agents_to_queue` | Current |
| GET | `/v1/queues/{queueId}/availability` | `check_queue_availability` | Current |
| GET | `/v1/queues/{queueId}` | `fetch_queue_by_id` | Current |
| GET | `/v1/queues/conversation-position/{csid}` | `check_conversation_queue_position` | Current |
| GET | `/v1/tags` | `list_tags` | Current |
| POST | `/v1/tags` | `add_tag` | Current |
| GET | `/v1/tags/{tagId}` | `fetch_tag_by_id` | Current |
| DELETE | `/v1/tags/{tagId}` | `remove_tag` | Current |
| PATCH | `/v1/tags/{tagId}/deactivate` | `deactivate_tag` | Current |
| PATCH | `/v1/tags/{tagId}/activate` | `activate_tag` | Current |
| GET | `/v1/anonymization/request/{requestId}` | `fetch_anonymization_status` | Current |
| POST | `/v1/anonymization` | `anonymize_entity_legacy` | Deprecated |
| GET | `/v1/contact-endpoints/{contactEndpointId}` | `fetch_contact_endpoint_by_id` | Current |
| GET | `/v1/contact-endpoints` | `list_contact_endpoints` | Current |
| GET | `/v1/custom-attributes/{customAttributeId}` | `fetch_custom_attribute_by_id` | Current |
| GET | `/v1/custom-attributes` | `list_custom_attributes` | Current |
| GET | `/v1/search/conversations` | `search_conversations_legacy` | Deprecated |
| POST | `/v1/search/conversations` | `search_conversations` | Current |
| GET | `/v1/webhooks/{webhookSubscriptionId}` | `fetch_webhook_subscription` | Current |
| DELETE | `/v1/webhooks/{webhookSubscriptionId}` | `remove_webhook_subscription` | Current |
| PATCH | `/v1/webhooks/{webhookSubscriptionId}` | `modify_webhook_subscription` | Current |
| GET | `/v1/webhooks` | `list_webhook_subscriptions` | Current |
| POST | `/v1/webhooks` | `add_webhook_subscription` | Current |
| GET | `/v1/webhooks/{webhookSubscriptionId}/delivery-status` | `fetch_webhook_delivery_status` | Current |
| GET | `/v1/webhooks/{webhookSubscriptionId}/delivery-status/logs/{event}` | `fetch_webhook_event_logs` | Current |
| GET | `/v1/templates` | `list_templates` | Current |
| DELETE | `/v1/templates/{templateId}` | `remove_template` | Current |
| GET | `/v1/business-hours/schedules` | `list_business_hours_schedules` | Current |
| GET | `/v1/business-hours/schedules/{scheduleId}/definition` | `fetch_business_hours_definition` | Current |
| GET | `/v1/business-hours/schedules/{scheduleId}/upcoming` | `fetch_upcoming_business_hours` | Current |
| GET | `/v1/business-hours/schedules/{scheduleId}/status` | `check_business_hours_status` | Current |
| GET | `/v1/knowledge/collections/{collectionId}` | `fetch_knowledge_collection_by_id` | Current |
| GET | `/v1/knowledge/collections/{collectionId}/catalog` | `fetch_knowledge_collection_catalog` | Current |
| GET | `/v1/knowledge/categories/{categoryId}` | `fetch_knowledge_category_by_id` | Current |
| GET | `/v1/knowledge/categories/{categoryId}/translations` | `fetch_knowledge_category_translations` | Current |
| GET | `/v1/knowledge/articles/{articleId}` | `fetch_knowledge_article_by_id` | Current |
| DELETE | `/v1/knowledge/articles/{articleId}` | `remove_knowledge_article` | Current |
| PATCH | `/v1/knowledge/articles/{articleId}` | `modify_knowledge_article` | Current |
| GET | `/v1/knowledge/articles/{articleId}/translations` | `fetch_knowledge_article_translations` | Current |
| PATCH | `/v1/knowledge/articles/{articleId}/translations` | `modify_knowledge_article_translations` | Current |
| POST | `/v1/knowledge/articles` | `add_knowledge_article` | Current |
| POST | `/v1/knowledge/categories` | `add_knowledge_category` | Current |
| GET | `/v1/knowledge/collections` | `list_knowledge_collections` | Current |
| POST | `/v1/knowledge/collections` | `add_knowledge_collection` | Current |
| POST | `/v1/knowledge/articles/{articleId}/translations/{languageId}/publish` | `publish_knowledge_article_translation` | Current |
| POST | `/v1/knowledge/articles/{articleId}/translations/{languageId}/unpublish` | `unpublish_knowledge_article_translation` | Current |
| DELETE | `/v1/knowledge/articles/{articleId}/translations/{languageId}` | `remove_knowledge_article_translation` | Current |
| POST | `/v1/knowledge/articles/{articleId}/publish` | `publish_knowledge_article` | Current |
| POST | `/v1/knowledge/articles/{articleId}/unpublish` | `unpublish_knowledge_article` | Current |
| PATCH | `/v1/knowledge/articles/{articleId}/parent/{parentId}` | `move_knowledge_article` | Current |
| DELETE | `/v1/knowledge/articles/{articleId}/parent` | `remove_knowledge_article_parent` | Current |
| POST | `/v1/knowledge/articles/attachments` | `upload_knowledge_article_attachments` | Current |
| GET | `/v1/organization` | `fetch_organization_details` | Current |
