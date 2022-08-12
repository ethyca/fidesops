import logging
from typing import Any, Union

import requests
from requests import Response
from sqlalchemy.orm import Session

from fidesops.common_exceptions import EmailConfigNotFoundException
from fidesops.core.config import config
from fidesops.models.email import EmailConfig
from fidesops.schemas.email.email import EmailServiceType, EmailServiceDetails, EmailServiceSecrets, EmailForActionType, \
    EmailActionType, SubjectIdentityVerificationBodyParams

logger = logging.getLogger(__name__)


def dispatch_email(db: Session, action_type, to_email: str, email_body_params: Union[SubjectIdentityVerificationBodyParams]):
    logger.info(f"Retrieving email config")
    # for now get first result, since we only support 1 email config
    email_config: EmailConfig = db.query(EmailConfig).first()
    if not email_config:
        raise EmailConfigNotFoundException
    logger.info(f"Building appropriate email template for action type: {action_type}")
    email: EmailForActionType = _build_email(action_type=action_type, body_params=email_body_params)
    logger.info(f"Retrieving appropriate dispatcher for email service: {email_config.service_type}")
    dispatcher: Any = _get_dispatcher_from_config_type(email_service_type=email_config.service_type)
    logger.info(f"Starting email dispatch for email service: {action_type}")
    try:
        dispatcher(email_config=email_config, email=email, to_email=to_email)
    except Exception as e:
        logger.info(e)  # fixme: throw exception


def _build_email(action_type: EmailActionType, body_params: Union[SubjectIdentityVerificationBodyParams]) -> EmailForActionType:
    if action_type == EmailActionType.SUBJECT_IDENTITY_VERIFICATION:
        return EmailForActionType(
            subject="Your one-time code",
            # for 1st iteration, below will be replaced with actual template files
            body=f"<html>Your one-time code is {body_params.access_code}. Hurry! It expires in 10 minutes.</html>"
        )
    logger.info(f"action type {action_type} not supported")
    # todo - handle not found case


def _get_dispatcher_from_config_type(email_service_type: EmailServiceType) -> Any:
    """Determines which dispatcher to use based on email service type"""
    return {
        EmailServiceType.MAILGUN.value: _mailgun_dispatcher,
    }[email_service_type.value]


def _mailgun_dispatcher(email_config: EmailConfig, email: EmailForActionType, to_email: str) -> None:
    """Dispatches email using mailgun"""
    logger.info("here")
    base_url = "https://api.mailgun.net" if email_config.details[EmailServiceDetails.IS_EU_DOMAIN.value] is False else "https://api.eu.mailgun.net"
    logger.info(f"organization is {config.organization}")
    domain = email_config.details[EmailServiceDetails.DOMAIN.value]
    data = {
        "from": f"{config.organization.name} <mailgun@{domain}>",
        "to": [to_email],
        "subject": email.subject,
        "html": email.body
    }
    # todo- implement retry logic
    try:
        response: Response = requests.post(
            f"{base_url}/{email_config.details[EmailServiceDetails.API_VERSION.value]}/{domain}/messages",
            auth=("api", email_config.secrets[EmailServiceSecrets.MAILGUN_API_KEY.value]),
            data=data
        )
        if not response.ok:
            logger.info(f"status code: {response.status_code}")
    except Exception as e:
        logger.info(e)

