"""Prerequisite guidance appended to every registered tool's MCP description."""

TOOL_PREREQUISITES = {'activate_tag': 'Call list_tags to identify the tag, including deactivated tags where relevant; '
                 'fetch_tag_by_id before modifying it.',
 'add_agent': 'Call list_agents to check for existing email addresses and prevent duplicates. Confirm the '
              'complete new agent details before creation; inspect each bulk result.',
 'add_agents_bulk': 'Call list_agents to check for existing email addresses and prevent duplicates. Confirm '
                    'the complete new agent details before creation; inspect each bulk result.',
 'add_agents_to_team': 'Call list_teams and list_agents to resolve team/agent IDs, then list_team_agents to '
                       'inspect current membership.',
 'add_conversation_message': 'Call search_conversations to resolve conversation_id, then '
                             'fetch_conversation_by_id to inspect its requester, channel and current state. '
                             'Use list_agents/fetch_agent_by_id for an outbound author and list_end_users '
                             'for cc/bcc recipient IDs. Confirm exact text, recipients, destination and '
                             'attachments separately before sending.',
 'add_conversation_note': 'Call search_conversations to resolve conversation_id, then '
                          'fetch_conversation_by_id to inspect its requester, channel and current state. '
                          'Resolve any author agent ID with list_agents; confirm exact note content and '
                          'destination.',
 'add_conversation_notes_bulk': 'Call search_conversations to resolve conversation_id, then '
                                'fetch_conversation_by_id to inspect its requester, channel and current '
                                'state. Resolve any author agent ID with list_agents; confirm exact note '
                                'content and destination.',
 'add_end_user': 'Call list_end_users with matching email/phone to check for duplicates before creating '
                 'users.',
 'add_end_users_bulk': 'Call list_end_users with matching email/phone to check for duplicates before '
                       'creating users.',
 'add_knowledge_article': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog for the '
                          'parent category, which is required when pre_release=True. If a collection is '
                          'empty, inspect another approved collection; do not disable pre-release to '
                          'bypass a missing parent. Resolve non-empty tag IDs with list_tags; omitted '
                          'or empty tags mean no tags. Resolve attachment URLs with an approved '
                          'upload_knowledge_article_attachments call.',
 'add_knowledge_category': 'Call list_knowledge_collections for a top-level parent or '
                           'fetch_knowledge_collection_catalog for a nested parent. Inspect the selected '
                           'parent and confirm translated titles.',
 'add_knowledge_collection': 'Call list_knowledge_collections to avoid duplicates. Confirm title, '
                             'description and internal knowledge-base visibility.',
 'add_queue': 'Call list_queues to check for an existing queue before creating one.',
 'add_tag': 'Call list_tags, including deactivated tags, to avoid creating a duplicate.',
 'add_team': 'Call list_teams to check whether the proposed team already exists.',
 'add_webhook_subscription': 'Call list_webhook_subscriptions to avoid duplicates. For QueueId filters use '
                             'list_queues. Confirm URL, events, filters and enabled state as approval for '
                             'future external deliveries; do not expose credentials.',
 'anonymize_conversation': 'Call search_conversations to resolve conversation_id, then '
                           'fetch_conversation_by_id to inspect its requester, channel and current state. '
                           'Confirm closure or the separately approved force-close effect. Preserve the '
                           'request ID for fetch_anonymization_status.',
 'anonymize_conversation_message': 'Call search_conversations to resolve conversation_id, then '
                                   'fetch_conversation_by_id to inspect its requester, channel and current '
                                   'state. Call list_conversation_messages to identify the exact message. '
                                   'Preserve the returned request ID for fetch_anonymization_status.',
 'anonymize_end_user': 'Call list_end_users to resolve the user. Fetch fetch_end_user_by_id before changing '
                       'or anonymizing it; preserve the anonymization request ID for '
                       'fetch_anonymization_status.',
 'anonymize_entity_legacy': 'Prefer resource-specific anonymization tools. Resolve the target with '
                            'list_end_users/fetch_end_user_by_id or '
                            'search_conversations/fetch_conversation_by_id; use list_conversation_messages '
                            'for message IDs. Confirm irreversible erasure and any forced closure '
                            'separately.',
 'assign_agents_to_queue': 'Call list_queues and list_agents to resolve IDs, then list_queue_agents to '
                           'inspect current membership.',
 'assign_conversation_to_agent': 'Call search_conversations to resolve conversation_id, then '
                                 'fetch_conversation_by_id to inspect its requester, channel and current '
                                 'state. Call list_agents to identify the assignee.',
 'check_business_hours_status': 'Call list_business_hours_schedules to obtain schedule_id; use the schedule '
                                'timezone when interpreting results.',
 'check_conversation_queue_position': 'Call search_conversations or fetch_conversation_by_id to identify the '
                                      'conversation and confirm it is queued. No queue ID is required.',
 'check_queue_availability': 'Call list_queues to identify the queue and use its returned ID.',
 'close_conversation': 'Call search_conversations to resolve conversation_id, then fetch_conversation_by_id '
                       'to inspect its requester, channel and current state.',
 'create_conversation_rating_offer': 'Call search_conversations to resolve conversation_id, then '
                                     'fetch_conversation_by_id to inspect its requester, channel and current '
                                     'state. Use fetch_end_user_by_id for the requester, list_agents for the '
                                     'participating agent, and list_conversation_ratings to check existing '
                                     'offers before approved creation.',
 'deactivate_tag': 'Call list_tags to identify the tag, including deactivated tags where relevant; '
                   'fetch_tag_by_id before modifying it.',
 'fetch_agent_by_id': 'Call list_agents to identify the agent. Before a change, fetch_agent_by_id to inspect '
                      'the exact current user and confirm the intended change.',
 'fetch_agent_presence': 'Call list_agents to identify the agent. Before a change, fetch_agent_by_id to '
                         'inspect the exact current user and confirm the intended change.',
 'fetch_aggregated_data': 'Call prepare_analytics_metric_query without an ID, then with the chosen metric '
                          'ID. Inspect allowed aggregations and filters; use fetch_analytics_filter_values '
                          'for additional valid values.',
 'fetch_analytics_filter_values': 'Call prepare_analytics_metric_query or prepare_analytics_record_query '
                                  'with the selected ID to discover the exact filter_attribute. Use returned '
                                  'values in the final analytics query.',
 'fetch_anonymization_status': 'Use the request ID returned by anonymize_end_user, anonymize_conversation, '
                               'anonymize_conversation_message or anonymize_entity_legacy. Do not initiate '
                               'another anonymization just to obtain status.',
 'fetch_business_hours_definition': 'Call list_business_hours_schedules to obtain schedule_id; use the '
                                    'schedule timezone when interpreting results.',
 'fetch_contact_endpoint_by_id': 'Call list_contact_endpoints to identify the contact endpoint.',
 'fetch_conversation_by_id': 'Call search_conversations if the conversation ID is not already verified.',
 'fetch_custom_attribute_by_id': 'Call list_custom_attributes to identify the definition and its ID.',
 'fetch_end_user_by_id': 'Call list_end_users to resolve the user. Fetch fetch_end_user_by_id before '
                         'changing or anonymizing it; preserve the anonymization request ID for '
                         'fetch_anonymization_status.',
 'fetch_knowledge_article_by_id': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog '
                                  'for the article ID. Fetch fetch_knowledge_article_by_id and '
                                  'fetch_knowledge_article_translations before editing, moving, deleting or '
                                  'publishing. Resolve destination parent IDs from the catalog and tag IDs '
                                  'from list_tags.',
 'fetch_knowledge_article_translations': 'Call list_knowledge_collections then '
                                         'fetch_knowledge_collection_catalog for the article ID. Fetch '
                                         'fetch_knowledge_article_by_id and '
                                         'fetch_knowledge_article_translations before editing, moving, '
                                         'deleting or publishing. Resolve destination parent IDs from the '
                                         'catalog and tag IDs from list_tags.',
 'fetch_knowledge_category_by_id': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog '
                                   'to resolve category IDs.',
 'fetch_knowledge_category_translations': 'Call list_knowledge_collections then '
                                          'fetch_knowledge_collection_catalog to resolve category IDs.',
 'fetch_knowledge_collection_by_id': 'Call list_knowledge_collections to select a collection ID.',
 'fetch_knowledge_collection_catalog': 'Call list_knowledge_collections to select a collection ID.',
 'fetch_organization_details': 'None. This is a discovery tool; use returned IDs and metadata for subsequent '
                               'operations.',
 'fetch_queue_by_id': 'Call list_queues to identify the queue and use its returned ID.',
 'fetch_tag_by_id': 'Call list_tags to identify the tag, including deactivated tags where relevant; '
                    'fetch_tag_by_id before modifying it.',
 'fetch_team_by_id': 'Call list_teams to identify the team; fetch_team_by_id and list_team_agents before '
                     'removal to review the impact.',
 'fetch_unaggregated_data': 'Call prepare_analytics_record_query without record_id, then with the chosen ID, '
                            'and fetch_analytics_filter_values for any required filter values. Keep the '
                            'query identical on later pages and follow returned cursors only as needed.',
 'fetch_upcoming_business_hours': 'Call list_business_hours_schedules to obtain schedule_id; use the '
                                  'schedule timezone when interpreting results.',
 'fetch_webhook_delivery_status': 'Call list_webhook_subscriptions then fetch_webhook_subscription to verify '
                                  'the subscription and destination before checking delivery status.',
 'fetch_webhook_event_logs': 'Call list_webhook_subscriptions then fetch_webhook_subscription for the '
                             'subscription and exact event name; inspect fetch_webhook_delivery_status '
                             'before retrieving the needed event logs.',
 'fetch_webhook_subscription': 'Call list_webhook_subscriptions to resolve webhook_id. Inspect its '
                               'destination, events and enabled state before subsequent actions.',
 'import_conversations': 'Call list_end_users/fetch_end_user_by_id for requesters, list_agents for authors, '
                         'and list_contact_endpoints for the integration/channel. Verify the destination and '
                         'final content before separate explicit send/import approval.',
 'link_conversation_to_parent': 'Call search_conversations to resolve conversation_id, then '
                                'fetch_conversation_by_id to inspect its requester, channel and current '
                                'state. Fetch both parent and child conversations and '
                                'list_linked_conversations before linking.',
 'list_agent_teams': 'Call list_agents to identify the agent. Before a change, fetch_agent_by_id to inspect '
                     'the exact current user and confirm the intended change.',
 'list_agents': 'None. This is a discovery tool; use returned IDs and metadata for subsequent operations.',
 'list_agents_presence': 'None. This is a discovery tool; use returned IDs and metadata for subsequent '
                         'operations.',
 'list_ai_agents': 'None. This is a discovery tool; use returned IDs and metadata for subsequent operations.',
 'list_business_hours_schedules': 'None. This is a discovery tool; use returned IDs and metadata for '
                                  'subsequent operations.',
 'list_contact_endpoints': 'None. This is a discovery tool; use returned IDs and metadata for subsequent '
                           'operations.',
 'list_conversation_activity_log': 'Call search_conversations to resolve conversation_id, then '
                                   'fetch_conversation_by_id to inspect its requester, channel and current '
                                   'state.',
 'list_conversation_flows': 'None. This is a discovery tool; use returned IDs and metadata for subsequent '
                            'operations.',
 'list_conversation_messages': 'Call search_conversations to resolve conversation_id, then '
                               'fetch_conversation_by_id to inspect its requester, channel and current '
                               'state.',
 'list_conversation_notes': 'Call search_conversations to resolve conversation_id, then '
                            'fetch_conversation_by_id to inspect its requester, channel and current state.',
 'list_conversation_ratings': 'Call search_conversations to resolve conversation_id, then '
                              'fetch_conversation_by_id to inspect its requester, channel and current state.',
 'list_conversation_ratings_legacy': 'Call search_conversations to resolve conversation_id, then '
                                     'fetch_conversation_by_id to inspect its requester, channel and current '
                                     'state.',
 'list_conversation_tags': 'Call search_conversations to resolve conversation_id, then '
                           'fetch_conversation_by_id to inspect its requester, channel and current state.',
 'list_custom_attributes': 'None. This is a discovery tool; use returned IDs and metadata for subsequent '
                           'operations.',
 'list_end_user_conversations': 'Call list_end_users to resolve the user. Fetch fetch_end_user_by_id before '
                                'changing or anonymizing it; preserve the anonymization request ID for '
                                'fetch_anonymization_status.',
 'list_end_users': 'None. This is a discovery tool; use returned IDs and metadata for subsequent operations.',
 'list_knowledge_collections': 'None. This is a discovery tool; use returned IDs and metadata for subsequent '
                               'operations.',
 'list_linked_conversations': 'Call search_conversations to resolve conversation_id, then '
                              'fetch_conversation_by_id to inspect its requester, channel and current state.',
 'list_organization_activity_log': 'None. This reads organization-wide activity.',
 'list_queue_agents': 'Call list_queues to identify the queue and use its returned ID.',
 'list_queues': 'None. This is a discovery tool; use returned IDs and metadata for subsequent operations.',
 'list_tags': 'None. This is a discovery tool; use returned IDs and metadata for subsequent operations.',
 'list_team_agents': 'Call list_teams to identify the team; fetch_team_by_id and list_team_agents before '
                     'removal to review the impact.',
 'list_team_presence': 'Call list_teams to identify team_id. Use the optional channel filter only when the '
                       'task requires it.',
 'list_teams': 'None. This is a discovery tool; use returned IDs and metadata for subsequent operations.',
 'list_templates': 'None. This is a discovery tool; use returned IDs and metadata for subsequent operations.',
 'list_webhook_subscriptions': 'None. This is a discovery tool; use returned IDs and metadata for subsequent '
                               'operations.',
 'modify_agent_partial': 'Call list_agents to identify the agent. Before a change, fetch_agent_by_id to '
                         'inspect the exact current user and confirm the intended change.',
 'modify_agents_bulk': 'Call list_agents to resolve each agent ID, then fetch_agent_by_id for current '
                       'values. Prepare and confirm every item; full updates can clear omitted fields. '
                       'Inspect each outcome for partial failures.',
 'modify_end_user_partial': 'Call list_end_users to resolve the user. Fetch fetch_end_user_by_id before '
                            'changing or anonymizing it; preserve the anonymization request ID for '
                            'fetch_anonymization_status.',
 'modify_end_users_bulk': 'Call list_end_users and fetch_end_user_by_id for each affected user. Confirm '
                          'every item; full updates can clear omitted fields. Inspect all results for '
                          'partial failures.',
 'modify_knowledge_article': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog for '
                             'the article ID. Fetch fetch_knowledge_article_by_id and '
                             'fetch_knowledge_article_translations before editing, moving, deleting or '
                             'publishing. Resolve destination parent IDs from the catalog and tag IDs from '
                             'list_tags.',
 'modify_knowledge_article_translations': 'Call list_knowledge_collections then '
                                          'fetch_knowledge_collection_catalog for the article ID. Fetch '
                                          'fetch_knowledge_article_by_id and '
                                          'fetch_knowledge_article_translations before editing, moving, '
                                          'deleting or publishing. Resolve destination parent IDs from the '
                                          'catalog and tag IDs from list_tags.',
 'modify_webhook_subscription': 'Call list_webhook_subscriptions then fetch_webhook_subscription to inspect '
                                'the exact destination and current settings. Resolve QueueId filters with '
                                'list_queues. Confirm the delivery impact and never resend redacted '
                                'credential values.',
 'move_knowledge_article': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog for the '
                           'article ID. Fetch fetch_knowledge_article_by_id and '
                           'fetch_knowledge_article_translations before editing, moving, deleting or '
                           'publishing. Resolve destination parent IDs from the catalog and tag IDs from '
                           'list_tags.',
 'prepare_analytics_metric_query': 'Without metric_id this is the first discovery step. Then call it with a '
                                   'returned metric ID before fetch_aggregated_data; use '
                                   'fetch_analytics_filter_values if more filter values are needed.',
 'prepare_analytics_record_query': 'Use prepare_analytics_metric_query and fetch_aggregated_data for summary '
                                   'questions first. When records are needed, call this tool without '
                                   'record_id, then with a discovered ID. Fetch only the required filter '
                                   'values with fetch_analytics_filter_values.',
 'publish_knowledge_article': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog for '
                              'the article ID. Fetch fetch_knowledge_article_by_id and '
                              'fetch_knowledge_article_translations before editing, moving, deleting or '
                              'publishing. Resolve destination parent IDs from the catalog and tag IDs from '
                              'list_tags.',
 'publish_knowledge_article_translation': 'Call list_knowledge_collections then '
                                          'fetch_knowledge_collection_catalog for the article ID. Fetch '
                                          'fetch_knowledge_article_by_id and '
                                          'fetch_knowledge_article_translations before editing, moving, '
                                          'deleting or publishing. Resolve destination parent IDs from the '
                                          'catalog and tag IDs from list_tags.',
 'remove_agent': 'Call list_agents to identify the agent. Before a change, fetch_agent_by_id to inspect the '
                 'exact current user and confirm the intended change.',
 'remove_agents_from_queue': 'Call list_queues and list_agents to resolve IDs, then list_queue_agents to '
                             'inspect current membership.',
 'remove_agents_from_team': 'Call list_teams and list_agents to resolve team/agent IDs, then '
                            'list_team_agents to inspect current membership.',
 'remove_knowledge_article': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog for '
                             'the article ID. Fetch fetch_knowledge_article_by_id and '
                             'fetch_knowledge_article_translations before editing, moving, deleting or '
                             'publishing. Resolve destination parent IDs from the catalog and tag IDs from '
                             'list_tags.',
 'remove_knowledge_article_parent': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog '
                                    'for the article ID. Fetch fetch_knowledge_article_by_id and '
                                    'fetch_knowledge_article_translations before editing, moving, deleting '
                                    'or publishing. Resolve destination parent IDs from the catalog and tag '
                                    'IDs from list_tags.',
 'remove_knowledge_article_translation': 'Call list_knowledge_collections then '
                                         'fetch_knowledge_collection_catalog for the article ID. Fetch '
                                         'fetch_knowledge_article_by_id and '
                                         'fetch_knowledge_article_translations before editing, moving, '
                                         'deleting or publishing. Resolve destination parent IDs from the '
                                         'catalog and tag IDs from list_tags.',
 'remove_tag': 'Call list_tags to identify the tag, including deactivated tags where relevant; '
               'fetch_tag_by_id before modifying it.',
 'remove_tag_from_conversation': 'Call search_conversations to resolve conversation_id, then '
                                 'fetch_conversation_by_id to inspect its requester, channel and current '
                                 'state. Call list_tags for tag IDs and list_conversation_tags to inspect '
                                 'current tags.',
 'remove_team': 'Call list_teams to identify the team; fetch_team_by_id and list_team_agents before removal '
                'to review the impact.',
 'remove_template': 'Call list_templates and inspect the exact template. Verify it is unused by flows and '
                    'automations; ask the user when usage cannot be established. Confirm irreversible '
                    'deletion.',
 'remove_webhook_subscription': 'Call list_webhook_subscriptions then fetch_webhook_subscription to inspect '
                                'the exact destination and current settings. Resolve QueueId filters with '
                                'list_queues. Confirm the delivery impact and never resend redacted '
                                'credential values.',
 'reopen_conversation': 'Call search_conversations to resolve conversation_id, then fetch_conversation_by_id '
                        'to inspect its requester, channel and current state.',
 'search_conversations': 'None for a text search. If filters reference agents, queues, tags or users, first '
                         'resolve their IDs with list_agents, list_queues, list_tags or list_end_users. '
                         'Prefer search_conversations over the deprecated GET search.',
 'search_conversations_legacy': 'None for a text search. If filters reference agents, queues, tags or users, '
                                'first resolve their IDs with list_agents, list_queues, list_tags or '
                                'list_end_users. Prefer search_conversations over the deprecated GET search.',
 'set_agent_working_channel': 'Call list_agents to identify the agent. Before a change, fetch_agent_by_id to '
                              'inspect the exact current user and confirm the intended change.',
 'set_conversation_followup_status': 'Call search_conversations to resolve conversation_id, then '
                                     'fetch_conversation_by_id to inspect its requester, channel and current '
                                     'state.',
 'start_conversation': 'Call list_end_users/fetch_end_user_by_id for requesters, list_agents for authors, '
                       'and list_contact_endpoints for the integration/channel. Verify the destination and '
                       'final content before separate explicit send/import approval.',
 'submit_conversation_rating_result': 'Call search_conversations to resolve conversation_id, then '
                                      'fetch_conversation_by_id to inspect its requester, channel and '
                                      'current state. Obtain rating_id from list_conversation_ratings or a '
                                      'separately approved create_conversation_rating_offer for this '
                                      'conversation. Match the offer type and submit only a '
                                      'customer-provided score.',
 'tag_conversation': 'Call search_conversations to resolve conversation_id, then fetch_conversation_by_id to '
                     'inspect its requester, channel and current state. Call list_tags for tag IDs and '
                     'list_conversation_tags to inspect current tags.',
 'tag_conversation_bulk': 'Call search_conversations to resolve conversation_id, then '
                          'fetch_conversation_by_id to inspect its requester, channel and current state. '
                          'Call list_tags for tag IDs and list_conversation_tags to inspect current tags.',
 'transfer_conversation_to_queue': 'Call search_conversations to resolve conversation_id, then '
                                   'fetch_conversation_by_id to inspect its requester, channel and current '
                                   'state. Call list_queues, then fetch_queue_by_id to verify the '
                                   'destination queue.',
 'unpublish_knowledge_article': 'Call list_knowledge_collections then fetch_knowledge_collection_catalog for '
                                'the article ID. Fetch fetch_knowledge_article_by_id and '
                                'fetch_knowledge_article_translations before editing, moving, deleting or '
                                'publishing. Resolve destination parent IDs from the catalog and tag IDs '
                                'from list_tags.',
 'unpublish_knowledge_article_translation': 'Call list_knowledge_collections then '
                                            'fetch_knowledge_collection_catalog for the article ID. Fetch '
                                            'fetch_knowledge_article_by_id and '
                                            'fetch_knowledge_article_translations before editing, moving, '
                                            'deleting or publishing. Resolve destination parent IDs from the '
                                            'catalog and tag IDs from list_tags.',
 'update_agent_full': 'Call list_agents to identify the agent. Before a change, fetch_agent_by_id to inspect '
                      'the exact current user and confirm the intended change.',
 'update_agents_bulk': 'Call list_agents to resolve each agent ID, then fetch_agent_by_id for current '
                       'values. Prepare and confirm every item; full updates can clear omitted fields. '
                       'Inspect each outcome for partial failures.',
 'update_conversation_custom_attributes': 'Call search_conversations or fetch_conversation_by_id for the '
                                          'conversation, then list_custom_attributes and '
                                          'fetch_custom_attribute_by_id for the permitted IDs, types and '
                                          'values.',
 'update_end_user_custom_attributes': 'Call list_end_users or fetch_end_user_by_id for the user, then '
                                      'list_custom_attributes and fetch_custom_attribute_by_id for the '
                                      'permitted IDs, types and values.',
 'update_end_user_full': 'Call list_end_users to resolve the user. Fetch fetch_end_user_by_id before '
                         'changing or anonymizing it; preserve the anonymization request ID for '
                         'fetch_anonymization_status.',
 'update_end_users_bulk': 'Call list_end_users and fetch_end_user_by_id for each affected user. Confirm '
                          'every item; full updates can clear omitted fields. Inspect all results for '
                          'partial failures.',
 'upload_knowledge_article_attachments': 'Obtain the exact user-approved image bytes, filenames and MIME '
                                         'types. If editing an article, first fetch_knowledge_article_by_id '
                                         'and fetch_knowledge_article_translations. After approved upload, '
                                         'use returned URLs in a separately confirmed translation change.'}

def apply_workflow_instructions(namespace):
    """Annotate functions before registration; fail early for stale tool names."""
    for name, guidance in TOOL_PREREQUISITES.items():
        tool = namespace[name]
        marker = "\n\nPrerequisite tools: "
        original = (tool.__doc__ or "").split(marker, 1)[0].rstrip()
        tool.__doc__ = original + marker + guidance
