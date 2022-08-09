from enum import Enum
from typing import Union, List, Any, Dict, Optional

from pydantic import BaseModel, Extra, validator

from fidesops.common_exceptions import ValidationError
from fidesops.schemas import Msg
from fidesops.schemas.api import BulkResponse, BulkUpdateFailed
from fidesops.schemas.shared_schemas import FidesOpsKey


class EmailServiceType(Enum):
    """Enum for email service type"""
    # may support twilio or google in the future
    MAILGUN = "mailgun"


class EmailPurpose(Enum):  # support using different email services for different purposes
    """Enum for email usage type"""
    # verify email upon acct creation
    SUBJECT_IDENTITY_VERIFICATION = "subject_identity_verification"
    # e.g. your request is processing
    AUTOMATED_SUBJECT_COMMUNICATION = "automated_subject_communication"
    # for 3rd parties that require manual email upon subject request for access/deletion
    EMAIL_CONNECTOR = "email_connector"


# fixme: Add enums for email purpose (subject communication) mapped to email action (request processing, request completed, etc)
# fixme: Add service router logic to get email service based on email action


class EmailServiceDetails(Enum):
    """Enum for email service details"""
    # mailgun-specific
    IS_EU_DOMAIN = "is_eu_domain"
    API_VERSION = "api_version"
    DOMAIN = "domain"


class EmailServiceDetailsMailgun(BaseModel):
    """The details required to represent a Mailgun email configuration."""
    is_eu_domain: Optional[bool] = False
    api_version: Optional[str] = "v3"
    domain: str

    class Config:
        """Restrict adding other fields through this schema."""

        extra = Extra.forbid


class EmailServiceSecrets(Enum):
    """Enum for email service secrets"""
    # mailgun-specific
    API_KEY = "api_key"


class EmailServiceSecretsMailgun(BaseModel):
    """The secrets required to connect to mailgun."""
    api_key: str

    class Config:
        """Restrict adding other fields through this schema."""

        extra = Extra.forbid


class EmailConfigRequest(BaseModel):
    """Email Config Request Schema"""

    name: str
    key: Optional[FidesOpsKey]
    service_type: EmailServiceType
    details: Union[
        EmailServiceDetailsMailgun,
    ]
    # default to using this email service for all email purposes
    purposes: Optional[List[EmailPurpose]] = [usage for usage in EmailPurpose.value]

    class Config:
        use_enum_values = True
        orm_mode = True

    @validator("details", pre=True, always=True)
    def validate_details(
            cls,
            v: Dict[str, str],
            values: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Custom validation logic for the `details` field.
        """
        service_type = values.get("service_type")
        if not service_type:
            raise ValueError("A `service_type` field must be specified.")

        try:
            schema = {
                EmailServiceType.MAILGUN.value: EmailServiceDetailsMailgun,
            }[service_type]
        except KeyError:
            raise ValueError(
                f"`storage_type` {service_type} has no supported `details` validation."
            )

        try:
            schema.parse_obj(v)  # type: ignore
        except ValidationError as exc:
            # Pydantic requires validators raise either a ValueError, TypeError, or AssertionError
            # so this exception is cast into a `ValueError`.
            errors = [f"{err['msg']} {str(err['loc'])}" for err in exc.errors()]
            raise ValueError(errors)

        return v


class EmailConfigResponse(BaseModel):
    """Email Config Response Schema"""

    name: str
    key: FidesOpsKey
    service_type: EmailServiceType
    details: Dict[EmailServiceDetails, Any]
    purposes: List[EmailPurpose]

    class Config:
        orm_mode = True
        use_enum_values = True


class BulkPutEmailConfigResponse(BulkResponse):
    """Schema with mixed success/failure responses for Bulk Create/Update of EmailConfig."""

    succeeded: List[EmailConfigResponse]
    failed: List[BulkUpdateFailed]


SUPPORTED_EMAIL_SERVICE_SECRETS = Union[
    EmailServiceSecretsMailgun
]


class EmailConnectionTestStatus(Enum):
    """Enum for supplying statuses of validating credentials for an Email Config"""

    succeeded = "succeeded"
    failed = "failed"
    skipped = "skipped"


class TestEmailStatusMessage(Msg):
    """A schema for checking status of email config."""

    test_status: Optional[EmailConnectionTestStatus] = None
    failure_reason: Optional[str] = None
