"""Structured wire inputs for the additional endpoints.

Based on Dixa API v1. Explicit _type literals preserve the discriminators shown
in Dixa's examples, including where the component schema omits those fields.
"""
import json
from typing import Any, Dict, List, Literal, Optional, Union
from typing_extensions import Annotated, Required, TypedDict
from pydantic import BeforeValidator, Field


def decode_json(value: Any) -> Any:
    """Accept native structured inputs or their JSON-encoded equivalents."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("Expected valid JSON or a native structured value") from exc
    return value


class CreateAgentInput(TypedDict, total=False):
    """CreateAgentInput."""
    displayName: Required[Annotated[str, Field(description="The agent's display name")]]
    email: Required[Annotated[str, Field(description="The agent's primary email address")]]
    phoneNumber: Annotated[str, Field(description="The agent's primary phone number")]
    additionalEmails: Annotated[List[str], Field(description='Additional email addresses for the agent')]
    additionalPhoneNumbers: Annotated[List[str], Field(description='Additional phone numbers for the agent')]
    firstName: Annotated[str, Field(description="The agent's first name")]
    lastName: Annotated[str, Field(description="The agent's last name")]
    middleNames: Annotated[List[str], Field(description="The agent's middle names")]
    avatarUrl: Annotated[str, Field(description="The url from which to load the agent's avatar")]


class BulkUpdateAgentInput(TypedDict, total=False):
    """BulkUpdateAgentInput."""
    id: Required[Annotated[str, Field(description='Unique identifier for the agent')]]
    displayName: Required[Annotated[str, Field(description="The agent's display name")]]
    phoneNumber: Annotated[str, Field(description="The agent's primary phone number")]
    additionalEmails: Annotated[List[str], Field(description='Additional email addresses for the agent')]
    additionalPhoneNumbers: Annotated[List[str], Field(description='Additional phone numbers for the agent')]
    firstName: Annotated[str, Field(description="The agent's first name")]
    lastName: Annotated[str, Field(description="The agent's last name")]
    middleNames: Annotated[List[str], Field(description="The agent's middle names")]
    avatarUrl: Annotated[str, Field(description="The url from which to load the agent's avatar")]


class BulkPatchAgentInput(TypedDict, total=False):
    """BulkPatchAgentInput."""
    id: Required[Annotated[str, Field(description='Unique identifier for the agent')]]
    displayName: Annotated[str, Field(description="The agent's display name")]
    phoneNumber: Annotated[str, Field(description="The agent's primary phone number")]
    additionalEmails: Annotated[List[str], Field(description='Additional email addresses for the agent')]
    additionalPhoneNumbers: Annotated[List[str], Field(description='Additional phone numbers for the agent')]
    firstName: Annotated[str, Field(description="The agent's first name")]
    lastName: Annotated[str, Field(description="The agent's last name")]
    middleNames: Annotated[List[str], Field(description="The agent's middle names")]
    avatarUrl: Annotated[str, Field(description="The url from which to load the agent's avatar")]


class Html(TypedDict, total=False):
    """Html."""
    value: Required[str]
    _type: Required[Literal['Html']]


class Markdown(TypedDict, total=False):
    """Markdown."""
    value: Required[str]
    _type: Required[Literal['Markdown']]


class Text(TypedDict, total=False):
    """Text."""
    value: Required[str]
    _type: Required[Literal['Text']]


Content = Union[Html, Markdown, Text]


class File(TypedDict, total=False):
    """File."""
    url: Required[Annotated[str, Field(description='url')]]
    prettyName: str


class Inbound(TypedDict, total=False):
    """Inbound."""
    content: Required[Content]
    attachments: List[File]
    integrationEmail: Annotated[str, Field(description='Internal email address registered for the integration with format: \\<email-address\\>@email.dixa.io')]
    externalId: Annotated[str, Field(description='Client generated identifier for external reference')]
    _type: Required[Literal['Inbound']]


class Outbound(TypedDict, total=False):
    """Outbound."""
    content: Required[Content]
    agentId: Required[str]
    attachments: List[File]
    integrationEmail: str
    externalId: str
    cc: List[str]
    bcc: List[str]
    _type: Required[Literal['Outbound']]


CreateMessageInput = Annotated[Union[Inbound, Outbound], Field(description='Only Outbound messages are supported for Sms and Whatsapp.')]


class CreateRatingOfferInput(TypedDict, total=False):
    """CreateRatingOfferInput."""
    userId: Required[str]
    agentId: Required[Annotated[str, Field(description='Please note that providing agentId that is not part of the conversation may skew metrics in Intelligence')]]
    ratingType: Required[Annotated[Literal['Csat', 'Nps', 'ThumbsUpOrDown'], Field(description="The type of numeric rating. E.g.: 'Csat', 'ThumbsUpOrDown', 'Nps'.")]]
    offeredAt: str


class Csat(TypedDict, total=False):
    """Csat."""
    value: Required[Annotated[int, Field(description="Numeric value between 1 and 5 representing the customer's satisfaction level.", ge=1, le=5)]]
    _type: Required[Literal['Csat']]


class Nps(TypedDict, total=False):
    """Nps."""
    value: Required[Annotated[int, Field(description='Numeric value between 0 and 10 representing the net promoter score.', ge=0, le=10)]]
    _type: Required[Literal['Nps']]


class ThumbsUpOrDown(TypedDict, total=False):
    """ThumbsUpOrDown."""
    value: Required[Annotated[int, Field(description='One of the the numeric values 0 (thumbs down) and 1 (thumbs up).', ge=0, le=1)]]
    _type: Required[Literal['ThumbsUpOrDown']]


SubmittedRatingResult = Union[Csat, Nps, ThumbsUpOrDown]


class CreateRatingResultInput(TypedDict, total=False):
    """CreateRatingResultInput."""
    userId: Annotated[Optional[str], Field(description="The userId property is no longer used so it's made optional to keep backwards compatibility. A null value can be provided instead of an actual ID.")]
    ratingResult: Required[SubmittedRatingResult]
    comment: str
    submittedAt: str


class BasicAuth(TypedDict, total=False):
    """BasicAuth."""
    username: Required[str]
    password: Required[str]
    _type: Required[Literal['BasicAuth']]


class NoAuth(TypedDict, total=False):
    """NoAuth."""
    _type: Required[Literal['NoAuth']]


class TokenAuth(TypedDict, total=False):
    """TokenAuth."""
    value: Required[Annotated[str, Field(description="Token value. It will be added in the headers of the request as: 'Authorization': 'Bearer \\<value\\>'")]]
    _type: Required[Literal['TokenAuth']]


WebhookAuthorization = Annotated[Union[BasicAuth, NoAuth, TokenAuth], Field(description="Authorization to be added as a header in the webhook request. Can be either, Basic auth, added as 'Basic base64encoded(\\<username\\>:\\<password\\>)', Token auth, added as 'Bearer \\<token value\\>', or no auth")]


Map_String = Dict[str, str]


class IsNotOneOf5(TypedDict, total=False):
    """IsNotOneOf."""
    field: Required[Annotated[str, Field(description='values: [InitialChannel, OperationOrigin, QueueId]')]]
    values: Required[Annotated[List[str], Field(min_length=1)]]
    _type: Required[Literal['IsNotOneOf']]


class IsOneOf5(TypedDict, total=False):
    """IsOneOf."""
    field: Required[Annotated[str, Field(description='values: [InitialChannel, OperationOrigin, QueueId]')]]
    values: Required[Annotated[List[str], Field(min_length=1)]]
    _type: Required[Literal['IsOneOf']]


Condition1 = Union[IsNotOneOf5, IsOneOf5]


class CombinedFilters(TypedDict, total=False):
    """CombinedFilters."""
    strategy: Required[Annotated[str, Field(description='values: [All, Any]')]]
    conditions: Required[Annotated[List[Condition1], Field(min_length=1)]]
    _type: Required[Literal['CombinedFilters']]


Filters1 = CombinedFilters


Map_WebhookEventType_Filters = Dict[str, Filters1]


class CreateWebhookSubscriptionInput(TypedDict, total=False):
    """CreateWebhookSubscriptionInput."""
    name: Required[Annotated[str, Field(description='The Webhook Subscription name')]]
    events: Annotated[List[Annotated[str, Field(description='values: [SLAEvaluationVoided, ConversationPending, SLAEvaluationBreached, ConversationMessageAdded, ConversationCustomAttributeUpdated, ConversationTranscriptionAdded, SLAEvaluationAchieved, ConversationAssigned, ConversationMessageDeliveryDelivered, ConversationMessageDeliveryInfo, ConversationTransferred, ConversationEnqueued, AgentUnbannedEnduser, TypingStarted, ConversationCreated, ConversationUnassigned, ConversationOpen, ConversationAbandoned, ConversationClosed, ConversationMessageDeliveryFailed, ConversationTagAdded, ConversationNoteAdded, AgentBannedEnduser, ConversationEndUserReplaced, ConversationMessageDeliverySeen, AgentUnbannedIp, ConversationMessageDeliverySent, AgentBannedIp, ConversationTagRemoved, ConversationRated, SLAEvaluationPending, ConversationMessageDeliverySpamComplaint, ConversationPendingExpired]')]], Field(description='The set of events this Webhook Subscription subscribes to. Allowed values: [SLAEvaluationVoided, ConversationPending, SLAEvaluationBreached, ConversationMessageAdded, ConversationCustomAttributeUpdated, ConversationTranscriptionAdded, SLAEvaluationAchieved, ConversationAssigned, ConversationMessageDeliveryDelivered, ConversationMessageDeliveryInfo, ConversationTransferred, ConversationEnqueued, AgentUnbannedEnduser, TypingStarted, ConversationCreated, ConversationUnassigned, ConversationOpen, ConversationAbandoned, ConversationClosed, ConversationMessageDeliveryFailed, ConversationTagAdded, ConversationNoteAdded, AgentBannedEnduser, ConversationEndUserReplaced, ConversationMessageDeliverySeen, AgentUnbannedIp, ConversationMessageDeliverySent, AgentBannedIp, ConversationTagRemoved, ConversationRated, SLAEvaluationPending, ConversationMessageDeliverySpamComplaint, ConversationPendingExpired]')]
    url: Required[Annotated[str, Field(description='URL of the server that the webhook request should be sent to')]]
    authorization: Required[WebhookAuthorization]
    customHeaders: Required[Annotated[Map_String, Field(description='Custom headers that will be added to the webhook request')]]
    enabled: Annotated[bool, Field(description='Defines whether this Webhook Subscription is enabled or disabled. Default is `true`')]
    filters: Annotated[Map_WebhookEventType_Filters, Field(description='Filters to be applied to the events of the Webhook Subscription, only filtered events will be sent out. Filters can target a conversation channel, queue...')]


class PatchWebhookSubscriptionInput(TypedDict, total=False):
    """PatchWebhookSubscriptionInput."""
    name: Annotated[str, Field(description='The Webhook Subscription name')]
    events: Annotated[List[Annotated[str, Field(description='values: [SLAEvaluationVoided, ConversationPending, SLAEvaluationBreached, ConversationMessageAdded, ConversationCustomAttributeUpdated, ConversationTranscriptionAdded, SLAEvaluationAchieved, ConversationAssigned, ConversationMessageDeliveryDelivered, ConversationMessageDeliveryInfo, ConversationTransferred, ConversationEnqueued, AgentUnbannedEnduser, TypingStarted, ConversationCreated, ConversationUnassigned, ConversationOpen, ConversationAbandoned, ConversationClosed, ConversationMessageDeliveryFailed, ConversationTagAdded, ConversationNoteAdded, AgentBannedEnduser, ConversationEndUserReplaced, ConversationMessageDeliverySeen, AgentUnbannedIp, ConversationMessageDeliverySent, AgentBannedIp, ConversationTagRemoved, ConversationRated, SLAEvaluationPending, ConversationMessageDeliverySpamComplaint, ConversationPendingExpired]')]], Field(description='The set of events this Webhook Subscription subscribes to. Allowed values: [SLAEvaluationVoided, ConversationPending, SLAEvaluationBreached, ConversationMessageAdded, ConversationCustomAttributeUpdated, ConversationTranscriptionAdded, SLAEvaluationAchieved, ConversationAssigned, ConversationMessageDeliveryDelivered, ConversationMessageDeliveryInfo, ConversationTransferred, ConversationEnqueued, AgentUnbannedEnduser, TypingStarted, ConversationCreated, ConversationUnassigned, ConversationOpen, ConversationAbandoned, ConversationClosed, ConversationMessageDeliveryFailed, ConversationTagAdded, ConversationNoteAdded, AgentBannedEnduser, ConversationEndUserReplaced, ConversationMessageDeliverySeen, AgentUnbannedIp, ConversationMessageDeliverySent, AgentBannedIp, ConversationTagRemoved, ConversationRated, SLAEvaluationPending, ConversationMessageDeliverySpamComplaint, ConversationPendingExpired]')]
    url: Annotated[str, Field(description='URL of the server that the webhook request should be sent to')]
    authorization: WebhookAuthorization
    customHeaders: Annotated[Map_String, Field(description='Custom headers that will be added to the webhook request')]
    enabled: Annotated[bool, Field(description='Defines whether this Webhook Subscription is enabled or disabled')]
    filters: Annotated[Map_WebhookEventType_Filters, Field(description='Filters to be applied to the events of the Webhook Subscription, only filtered events will be sent out. Filters can target a conversation channel, queue...')]


ConversationAnonymizationType = Dict[str, Any]


MessageAnonymizationType = Dict[str, Any]


UnknownAnonymizationType = Dict[str, Any]


UserAnonymizationType = Dict[str, Any]


DeprecatedAnonymizationType = Annotated[Union[ConversationAnonymizationType, MessageAnonymizationType, UnknownAnonymizationType, UserAnonymizationType], Field(description='Replaced by _type field')]


class AnonymizeEntityInput(TypedDict, total=False):
    """AnonymizeEntityInput."""
    entityId: Required[str]
    entityType: DeprecatedAnonymizationType
    forceAnonymization: bool
    _type: Annotated[Literal['Conversation', 'Message', 'User'], Field(description='values: [Conversation, Message, User]')]

AgentCreateList = Annotated[List[CreateAgentInput], BeforeValidator(decode_json)]

AgentUpdateList = Annotated[List[BulkUpdateAgentInput], BeforeValidator(decode_json)]

AgentPatchList = Annotated[List[BulkPatchAgentInput], BeforeValidator(decode_json)]

ConversationMessageInput = Annotated[CreateMessageInput, BeforeValidator(decode_json)]

RatingOfferInput = Annotated[CreateRatingOfferInput, BeforeValidator(decode_json)]

RatingResultInput = Annotated[CreateRatingResultInput, BeforeValidator(decode_json)]

WebhookCreateInput = Annotated[CreateWebhookSubscriptionInput, BeforeValidator(decode_json)]

WebhookPatchInput = Annotated[PatchWebhookSubscriptionInput, BeforeValidator(decode_json)]

LegacyAnonymizationInput = Annotated[AnonymizeEntityInput, BeforeValidator(decode_json)]
