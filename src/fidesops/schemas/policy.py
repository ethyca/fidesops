from typing import Dict, List, Optional, Union

from fideslang.validation import FidesKey

from fidesops.models.policy import (
    ActionType,
    DataCategory,
)
from fidesops.schemas.api import BulkResponse, BulkUpdateFailed
from fidesops.schemas.base_class import BaseSchema
from fidesops.schemas.masking.masking_configuration import FormatPreservationConfig
from fidesops.schemas.shared_mixins import FidesKeyMixin
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


class RuleTarget(FidesKeyMixin):
    """An external representation of a Rule's target DataCategory within a Fidesops Policy"""

    name: Optional[str]
    key: Optional[FidesKey]
    data_category: DataCategory

    class Config:
        """Populate models with the raw value of enum fields, rather than the enum itself"""

        use_enum_values = True
        orm_mode = True


class RuleBase(FidesKeyMixin):
    """An external representation of a Rule within a Fidesops Policy"""

    name: str
    key: Optional[FidesKey]
    action_type: ActionType

    class Config:
        """Populate models with the raw value of enum fields, rather than the enum itself"""

        use_enum_values = True
        orm_mode = True


class RuleCreate(RuleBase):
    """
    The schema to use when creating a Rule. This schema accepts a storage_destination_key
    over a composite object.
    """

    _fides_key_field_names = ["key", "storage_destination_key"]
    storage_destination_key: Optional[FidesKey]
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
    key: Optional[FidesKey]

    class Config:
        """Allow ORM access"""

        orm_mode = True


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
