from __future__ import annotations

import logging

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from fidesops.ops.api.deps import get_db
from fidesops.ops.api.v1.urn_registry import (
    CONSENT_REQUEST,
    CONSENT_REQUEST_PREFERENCES,
    CONSENT_REQUEST_VERIFY,
    V1_URL_PREFIX,
)
from fidesops.ops.common_exceptions import (
    FunctionalityNotConfigured,
    IdentityVerificationException,
)
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
    SubjectIdentityVerificationBodyParams,
)
from fidesops.ops.schemas.privacy_request import Consent as ConsentSchema
from fidesops.ops.schemas.privacy_request import (
    ConsentPreferences,
    ConsentPreferencesWithVerificationCode,
    ConsentRequestResponse,
    VerificationCode,
)
from fidesops.ops.schemas.redis_cache import Identity
from fidesops.ops.service.email.email_dispatch_service import dispatch_email_task
from fidesops.ops.service.privacy_request.request_runner_service import (
    generate_id_verification_code,
)
from fidesops.ops.tasks import EMAIL_QUEUE_NAME
from fidesops.ops.util.api_router import APIRouter

router = APIRouter(tags=["Consent"], prefix=V1_URL_PREFIX)

logger = logging.getLogger(__name__)


@router.post(
    CONSENT_REQUEST,
    status_code=HTTP_200_OK,
    response_model=ConsentRequestResponse,
)
def create_consent_request(
    *,
    db: Session = Depends(get_db),
    data: Identity,
) -> ConsentRequestResponse:
    """Creates a verification code for the user to verify access to manange consent preferences."""
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

    consent_request_data = {
        "provided_identity_id": identity.id,
    }
    consent_request = ConsentRequest.create(db, data=consent_request_data)
    verificaiton_code = _send_verification_code_to_user(db, consent_request, data.email)
    return ConsentRequestResponse(identity=data, verification_code=verificaiton_code)


@router.post(
    CONSENT_REQUEST_VERIFY,
    status_code=HTTP_200_OK,
    response_model=ConsentPreferences,
)
def consent_request_verify(
    *,
    consent_request_id: str,
    db: Session = Depends(get_db),
    data: VerificationCode,
) -> ConsentPreferences:
    """Verifies the verification code and returns the current consent preferences if successful."""
    provided_identity = _get_consent_request_and_provided_identity(
        db=db, consent_request_id=consent_request_id, verification_code=data.code
    )

    if not provided_identity.encrypted_value:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Provided identity missing email"
        )

    consent = Consent.filter(
        db=db, conditions=Consent.provided_identity_id == provided_identity.id
    ).all()

    identity = (
        Identity(email=provided_identity.encrypted_value["value"])
        if provided_identity.field_name == ProvidedIdentityType.email
        else Identity(phone_number=provided_identity.encrypted_value["value"])
    )

    if not consent:
        return ConsentPreferences(identity=identity, consent=None)

    return ConsentPreferences(
        identity=identity,
        consent=[
            Consent(
                data_use=x.data_use,
                data_use_description=x.data_use_description,
                opt_in=x.opt_in,
            )
            for x in consent
        ],
    )


@router.patch(
    CONSENT_REQUEST_PREFERENCES,
    status_code=HTTP_200_OK,
    response_model=ConsentPreferences,
)
def set_consent_preferences(
    *,
    consent_request_id: str,
    db: Session = Depends(get_db),
    data: ConsentPreferencesWithVerificationCode,
) -> ConsentPreferences:
    """Verifies the verification code and saves the user's consent preferences if successful."""
    if not data.consent:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="No consent preferences provided"
        )

    provided_identity = _get_consent_request_and_provided_identity(
        db=db,
        consent_request_id=consent_request_id,
        verification_code=data.code,
    )

    if not provided_identity.encrypted_value:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Provided identity missing email"
        )

    for preference in data.consent:
        current_preference = Consent.filter(
            db=db,
            conditions=(Consent.provided_identity_id == provided_identity.id)
            & (Consent.data_use == preference.data_use),
        ).first()

        if current_preference:
            current_preference.update(db, data=dict(preference))
        else:
            preference_dict = dict(preference)
            preference_dict["provided_identity_id"] = provided_identity.id
            Consent.create(db, data=preference_dict)

    preferences = Consent.filter(
        db, conditions=(Consent.provided_identity_id == provided_identity.id)
    ).all()

    if not preferences:
        return ConsentPreferences(identity=data.identity, consent=None)

    return ConsentPreferences(
        identity=data.identity,
        consent=[
            ConsentSchema(
                data_use=x.data_use,
                data_use_description=x.data_use_description,
                opt_in=x.opt_in,
            )
            for x in preferences
        ],
    )


def _get_consent_request_and_provided_identity(
    db: Session,
    consent_request_id: str,
    verification_code: str,
) -> ProvidedIdentity:
    """Verifies the consent request and verification code, then return the ProvidedIdentity if successful."""
    consent_request = ConsentRequest.get_by_key_or_id(
        db=db, data={"id": consent_request_id}
    )

    if not consent_request:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Consent request not found"
        )

    try:
        consent_request.verify_identity(verification_code)
    except IdentityVerificationException as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=exc.message)
    except PermissionError as exc:
        logger.info("Invalid verification code provided for %s.", consent_request.id)
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=exc.args[0])

    provided_identity: ProvidedIdentity | None = ProvidedIdentity.get_by_key_or_id(
        db, data={"id": consent_request.provided_identity_id}
    )

    # It shouldn't be possible to hit this because the cascade delete of the identity
    # data would also delete the consent_request, but including this as a safety net.
    if not provided_identity:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No identity found for consent request id",
        )

    return provided_identity


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
