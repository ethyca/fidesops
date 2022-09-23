from __future__ import annotations

import logging

from fastapi import Body, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from fidesops.ops.api.deps import get_db
from fidesops.ops.api.v1.urn_registry import (
    CONSENT_REQUEST,
    CONSENT_REQUEST_PREFERENCES,
    CONSENT_REQUEST_VERIFY,
    V1_URL_PREFIX,
)
from fidesops.ops.common_exceptions import FunctionalityNotConfigured
from fidesops.ops.core.config import config
from fidesops.ops.models.email import EmailConfig
from fidesops.ops.models.privacy_request import (
    Consent,
    ConsentRequest,
    ProvidedIdentity,
    ProvidedIdentityType,
)
from fidesops.ops.schemas.email.email import (
    EmailActionType,
    FidesopsEmail,
    RequestReceiptBodyParams,
    RequestReviewDenyBodyParams,
    SubjectIdentityVerificationBodyParams,
)
from fidesops.ops.schemas.privacy_request import ConsentRequest as ConsentRequestSchema
from fidesops.ops.schemas.privacy_request import (
    ConsentRequestResponse,
    ConsentRequestVerification,
)
from fidesops.ops.schemas.redis_cache import Identity
from fidesops.ops.service.email.email_dispatch_service import (
    dispatch_email,
    dispatch_email_task,
)
from fidesops.ops.service.privacy_request.request_runner_service import (
    generate_id_verification_code,
    queue_privacy_request,
)
from fidesops.ops.tasks import EMAIL_QUEUE_NAME
from fidesops.ops.util.api_router import APIRouter
from fidesops.ops.util.cache import FidesopsRedis

router = APIRouter(tags=["Consent"], prefix=V1_URL_PREFIX)

logger = logging.getLogger(__name__)


@router.post(
    CONSENT_REQUEST,
    status_code=HTTP_200_OK,
    response_model=ConsentRequestResponse,
)
def consent_request(
    *,
    db: Session = Depends(get_db),
    data: Identity,
) -> ConsentRequestResponse:
    """Record the users consent preference."""
    if not config.redis.enabled:
        raise FunctionalityNotConfigured(
            "Application redis cache required, but it is currently disabled! Please update your application configuration to enable integration with a redis cache."
        )

    if not config.execution.subject_identity_verification_required:
        raise FunctionalityNotConfigured(
            "Subject identity verification is required, but it is currently disabled! Please update your application configuration to enable subject identity verification."
        )

    if not data.email:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail="An email address is required")

    identity = ProvidedIdentity.filter(
        db=db,
        conditions=(
            (ProvidedIdentity.field_name == ProvidedIdentityType.email)
            & (ProvidedIdentity.hashed_value == ProvidedIdentity.hash_value(data.email))
        ),
    ).first()

    if not identity:
        provided_identity_data = {
            "privacy_request_id": None,
            "field_name": "email",
            "encrypted_value": {"value": "test@email.com"},
        }
        identity = ProvidedIdentity.create(db, data=provided_identity_data)

    consent_request = {
        "provided_identity_id": identity.id,
    }
    consent_request = ConsentRequest.create(db, data=consent_request)
    verificaiton_code = _send_verification_code_to_user(db, consent_request, data.email)
    return ConsentRequestResponse(identity=data, verification_code=verificaiton_code)


@router.post(
    CONSENT_REQUEST_VERIFY,
    status_code=HTTP_200_OK,
    response_model=ConsentRequestResponse,
)
def consent_request(
    *,
    db: Session = Depends(get_db),
    data: Identity,
) -> ConsentRequest:
    ...


def _send_verification_code_to_user(
    db: Session, request: ConsentRequest, email: str | None
) -> str:
    """Generate and cache a verification code, and then email to the user"""
    EmailConfig.get_configuration(
        db=db
    )  # Validates Fidesops is currently configured to send emails
    verification_code = generate_id_verification_code()
    request.cache_identity_verification_code(verification_code)
    dispatch_email_task.apply_async(
        queue=EMAIL_QUEUE_NAME,
        kwargs={
            "email_meta": FidesopsEmail(
                action_type=EmailActionType.SUBJECT_IDENTITY_VERIFICATION,
                body_params=SubjectIdentityVerificationBodyParams(
                    verification_code=verification_code,
                    verification_code_ttl_seconds=config.redis.identity_verification_code_ttl_seconds,
                ),
            ).dict(),
            "to_email": email,
        },
    )

    return verification_code
