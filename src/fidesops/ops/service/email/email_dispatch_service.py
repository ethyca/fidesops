import logging
from typing import Any, Dict, Optional, Union

import requests
from sqlalchemy.orm import Session

from fidesops.ops.common_exceptions import EmailDispatchException
from fidesops.ops.email_templates import get_email_template
from fidesops.ops.models.email import EmailConfig
from fidesops.ops.models.privacy_request import EmailRequestFulfillmentBodyParams
from fidesops.ops.schemas.email.email import (
    EmailActionType,
    EmailForActionType,
    EmailServiceDetails,
    EmailServiceSecrets,
    EmailServiceType,
    FidesopsEmail,
    SubjectIdentityVerificationBodyParams,
)
from fidesops.ops.tasks import DatabaseTask, celery_app
from fidesops.ops.util.logger import Pii

logger = logging.getLogger(__name__)


@celery_app.task(base=DatabaseTask, bind=True)
def dispatch_email_task(
    self: DatabaseTask,
    email_meta: Dict[str, Any],
    to_email: str,
) -> None:
    """
    A wrapper function to dispatch an email task into the Celery queues
    """
    schema = FidesopsEmail.parse_obj(email_meta)
    with self.session as db:
        dispatch_email(
            db,
            schema.action_type,
            to_email,
            schema.body_params,
        )


def dispatch_email(
    db: Session,
    action_type: EmailActionType,
    to_email: Optional[str],
    email_body_params: Union[
        SubjectIdentityVerificationBodyParams,
        EmailRequestFulfillmentBodyParams,
    ],
) -> None:
    """
    Sends an email to `to_email` with content supplied in `email_body_params`
    """
    if not to_email:
        raise EmailDispatchException("No email supplied.")

    logger.info("Retrieving email config")
    email_config: EmailConfig = EmailConfig.get_configuration(db=db)
    logger.info("Building appropriate email template for action type: %s", action_type)
    email: EmailForActionType = _build_email(
        action_type=action_type,
        body_params=email_body_params,
    )
    email_service: EmailServiceType = email_config.service_type  # type: ignore
    logger.info(
        "Retrieving appropriate dispatcher for email service: %s", email_service
    )
    dispatcher: Any = _get_dispatcher_from_config_type(email_service_type=email_service)
    logger.info(
        "Starting email dispatch for email service with action type: %s", action_type
    )
    dispatcher(
        email_config=email_config,
        email=email,
        to_email=to_email,
    )


def _build_email(
    action_type: EmailActionType,
    body_params: Any,
) -> EmailForActionType:
    if action_type == EmailActionType.SUBJECT_IDENTITY_VERIFICATION:
        template = get_email_template(action_type)
        return EmailForActionType(
            subject="Your one-time code",
            body=template.render(
                {
                    "code": body_params.verification_code,
                    "minutes": body_params.get_verification_code_ttl_minutes(),
                }
            ),
        )
    if action_type == EmailActionType.EMAIL_ERASURE_REQUEST_FULFILLMENT:
        base_template = get_email_template(action_type)
        return EmailForActionType(
            subject="Data erasure request",
            body=base_template.render(
                {"dataset_collection_action_required": body_params}
            ),
        )
    logger.error("Email action type %s is not implemented", action_type)
    raise EmailDispatchException(f"Email action type {action_type} is not implemented")


def _get_dispatcher_from_config_type(email_service_type: EmailServiceType) -> Any:
    """Determines which dispatcher to use based on email service type"""
    return {
        EmailServiceType.MAILGUN.value: _mailgun_dispatcher,
    }[email_service_type.value]


def _mailgun_dispatcher(
    email_config: EmailConfig, email: EmailForActionType, to_email: str
) -> None:
    """Dispatches email using mailgun"""
    base_url = (
        "https://api.mailgun.net"
        if email_config.details[EmailServiceDetails.IS_EU_DOMAIN.value] is False
        else "https://api.eu.mailgun.net"
    )
    domain = email_config.details[EmailServiceDetails.DOMAIN.value]
    data = {
        "from": f"<mailgun@{domain}>",
        "to": [to_email],
        "subject": email.subject,
        "html": email.body,
    }
    try:
        response: requests.Response = requests.post(
            f"{base_url}/{email_config.details[EmailServiceDetails.API_VERSION.value]}/{domain}/messages",
            auth=(
                "api",
                email_config.secrets[EmailServiceSecrets.MAILGUN_API_KEY.value],  # type: ignore
            ),
            data=data,
        )
        if not response.ok:
            logger.error(
                "Email failed to send with status code: %s", response.status_code
            )
            raise EmailDispatchException(
                f"Email failed to send with status code {response.status_code}"
            )
    except Exception as e:
        logger.error("Email failed to send: %s", Pii(str(e)))
        raise EmailDispatchException(f"Email failed to send due to: {e}")
