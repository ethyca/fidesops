from typing import Dict, List, Optional, Union

from fidesops.schemas.connection_configuration.connection_config import (
    ConnectionConfigurationResponse,
)
from fidesops.schemas.shared_schemas import FidesOpsKey

from fidesops.models.policy import (
    ActionType,
    DataCategory,
    WebhookDirection,
)
from fidesops.schemas.api import BulkResponse, BulkUpdateFailed
from fidesops.schemas.base_class import BaseSchema
from fidesops.schemas.masking.masking_configuration import FormatPreservationConfig
from fidesops.schemas.storage.storage import StorageDestinationResponse


class PolicyMaskingSpec(BaseSchema):
    """Models the masking strategy definition int the policy document"""

    strategy: str
    configuration: Dict[str, Union[str, FormatPreservationConfig]]


class PolicyMaskingSpecResponse(BaseSchema):
    """
    The schema to use when returning a masking strategy via the API. This schema omits other
    potentially sensitive fields in the masking configuration, for example the encryption
    algorithm.
    """

    strategy: str


class RuleTarget(BaseSchema):
    """An external representation of a Rule's target DataCategory within a Fidesops Policy"""

    name: Optional[str]
    key: Optional[FidesOpsKey]
    data_category: DataCategory

    class Config:
        """Populate models with the raw value of enum fields, rather than the enum itself"""

        use_enum_values = True


class RuleBase(BaseSchema):
    """An external representation of a Rule within a Fidesops Policy"""

    name: str
    key: Optional[FidesOpsKey]
    action_type: ActionType

    class Config:
        """Populate models with the raw value of enum fields, rather than the enum itself"""

        use_enum_values = True


class RuleCreate(RuleBase):
    """
    The schema to use when creating a Rule. This schema accepts a storage_destination_key
    over a composite object.
    """

    storage_destination_key: Optional[FidesOpsKey]
    masking_strategy: Optional[PolicyMaskingSpec]


class RuleResponse(RuleBase):
    """
    The schema to use when returning a Rule via the API. This schema uses a censored version
    of the `PolicyMaskingSpec` that omits the configuration to avoid exposing secrets.
    """

    storage_destination: Optional[StorageDestinationResponse]
    masking_strategy: Optional[PolicyMaskingSpecResponse]


class Rule(RuleBase):
    """A representation of a Rule that features all storage destination data."""

    storage_destination: Optional[StorageDestinationResponse]
    masking_strategy: Optional[PolicyMaskingSpec]


class Policy(BaseSchema):
    """An external representation of a Fidesops Policy"""

    name: str
    key: Optional[FidesOpsKey]


class PolicyResponse(Policy):
    """A holistic view of a Policy record, including all foreign keys by default."""

    rules: Optional[List[RuleResponse]]


class BulkPutRuleTargetResponse(BulkResponse):
    """Schema with mixed success/failure responses for Bulk Create/Update of RuleTarget responses."""

    succeeded: List[RuleTarget]
    failed: List[BulkUpdateFailed]


class BulkPutRuleResponse(BulkResponse):
    """Schema with mixed success/failure responses for Bulk Create/Update of Rule responses."""

    succeeded: List[RuleResponse]
    failed: List[BulkUpdateFailed]


class BulkPutPolicyResponse(BulkResponse):
    """Schema with mixed success/failure responses for Bulk Create/Update of Policy responses."""

    succeeded: List[PolicyResponse]
    failed: List[BulkUpdateFailed]


class WebhookBase(BaseSchema):
    """Base schema for webhooks"""

    direction: WebhookDirection
    key: Optional[FidesOpsKey]
    name: Optional[str]


class PolicyWebhookCreate(WebhookBase):
    """Request schema for creating/updating a Policy Webhook"""

    connection_config_key: FidesOpsKey

    class Config:
        """Populate models with the raw value of enum fields, rather than the enum itself"""

        use_enum_values = True


class PolicyWebhookResponse(WebhookBase):
    """Response schema after creating a PolicyWebhook"""

    connection_config: Optional[ConnectionConfigurationResponse]
    order: int

    class Config:
        """Set orm_mode to True"""

        orm_mode = True


class PolicyWebhookUpdate(BaseSchema):
    """Request schema for updating a single webhook - fields are optional"""

    direction: Optional[WebhookDirection]
    name: Optional[str]
    connection_config_key: Optional[FidesOpsKey]
    order: Optional[int]

    class Config:
        """Only the included attributes will be used"""

        orm_mode = True
        extra = "forbid"
        use_enum_values = True


class WebhookOrder(BaseSchema):
    """Schema for displaying which order the webhooks should run"""

    key: FidesOpsKey
    order: int

    class Config:
        """Set orm_mode to True"""

        orm_mode = True


class PolicyWebhookUpdateResponse(BaseSchema):
    """Response schema after a PATCH to a single webhook - because updating the order of this webhook can update the
    order of other webhooks, reordered will include the new order if order was adjusted at all"""

    resource: PolicyWebhookResponse
    reordered: List[WebhookOrder]

    class Config:
        """Set orm_mode to True"""

        orm_mode = True
        extra = "forbid"
        use_enum_values = True
