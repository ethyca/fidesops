# pylint: disable=W0223
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests
from fideslib.models.audit_log import AuditLog, AuditLogAction
from sqlalchemy.orm import Session

from fidesops.ops.analytics import sync_send_analytics_event_wrapper
from fidesops.ops.analytics_event_factory import failed_graph_analytics_event
from fidesops.ops.common_exceptions import EmailDispatchException
from fidesops.ops.core.config import config
from fidesops.ops.email_templates import get_email_template
from fidesops.ops.models.email import EmailConfig
from fidesops.ops.models.policy import ActionType, CurrentStep, Policy, PolicyPostWebhook
from fidesops.ops.models.privacy_request import (
    CheckpointActionRequired,
    PrivacyRequest,
    PrivacyRequestStatus,
    ProvidedIdentityType,
)
from fidesops.ops.schemas.email.email import (
    AccessRequestCompleteBodyParams,
    EmailActionType,
    EmailConnectorEmail,
    EmailForActionType,
    EmailServiceDetails,
    EmailServiceSecrets,
    EmailServiceType,
    FidesopsEmail,
    RequestReceiptBodyParams,
    RequestReviewDenyBodyParams,
    SubjectIdentityVerificationBodyParams,
)
from fidesops.ops.tasks import EMAIL_QUEUE_NAME, DatabaseTask, celery_app
from fidesops.ops.util.logger import Pii, _log_exception

logger = logging.getLogger(__name__)


class RequestCompletionBase(DatabaseTask):
    """
    A wrapper class to handle specific success/failure cases for request completion emails
    """

    def on_failure(self, exc, task_id, args, kwargs, einfo) -> None:
        logger.error("in celery error callback")
        privacy_request_id = kwargs["privacy_request_id"]

        with self.session as db:
            privacy_request = PrivacyRequest.get(db, object_id=privacy_request_id)
            privacy_request.error_processing(db=db)
            # If dev mode, log traceback
            sync_send_analytics_event_wrapper(
                failed_graph_analytics_event(privacy_request, exc)
            )
            _log_exception(exc, config.dev_mode)

    def on_success(self, retval, task_id, args, kwargs):
        privacy_request_id = kwargs["privacy_request_id"]
        with self.session as db:
            privacy_request = PrivacyRequest.get(db, object_id=privacy_request_id)
            privacy_request.finished_processing_at = datetime.utcnow()
            AuditLog.create(
                db=db,
                data={
                    "user_id": "system",
                    "privacy_request_id": privacy_request.id,
                    "action": AuditLogAction.finished,
                    "message": "",
                },
            )
            privacy_request.status = PrivacyRequestStatus.complete
            logging.info("Privacy request %s run completed.", privacy_request.id)
            privacy_request.save(db=db)


@celery_app.task(base=RequestCompletionBase, bind=True)
def dispatch_email_task_request_completion(
    self: DatabaseTask,
    privacy_request_id: str,
    to_email: str,
    access_result_urls: List[str],
    policy_id: str,
) -> None:
    """
    A wrapper function to dispatch an email task into the Celery queues
    """
    logger.info("Dispatching email for request completion")
    with self.session as db:
        policy = Policy.get(db, object_id=policy_id)
        if policy.get_rules_for_action(action_type=ActionType.access):
            dispatch_email(
                db,
                EmailActionType.PRIVACY_REQUEST_COMPLETE_ACCESS,
                to_email,
                AccessRequestCompleteBodyParams(download_links=access_result_urls),
            )
        if policy.get_rules_for_action(action_type=ActionType.erasure):
            dispatch_email(
                db,
                EmailActionType.PRIVACY_REQUEST_COMPLETE_DELETION,
                to_email,
                None,
            )


class IdentityVerificationBase(DatabaseTask):
    """
    A wrapper class to handle specific success/failure cases for identity verification emails
    """

    def on_failure(self, exc, task_id, args, kwargs, einfo) -> None:
        privacy_request_id = kwargs["privacy_request_id"]
        with self.session as db:
            # fixme: net new functionality- needs review. Previously we didn't set privacy request to error upon failure to send verification emil
            # we only returned failure for the create privacy request api response.
            privacy_request = PrivacyRequest.get(db, object_id=privacy_request_id)
            privacy_request.error_processing(db=db)
            # If dev mode, log traceback
            _log_exception(exc, config.dev_mode)


@celery_app.task(base=IdentityVerificationBase, bind=True)
def dispatch_email_task_identity_verification(
    self: DatabaseTask,
    email_meta: Dict[str, Any],
    to_email: str,
    privacy_request_id: str,
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


class EmailTaskEmailConnector(DatabaseTask):
    """
    A wrapper class to handle specific failure case for email connectors
    """

    def on_failure(self, exc, task_id, args, kwargs, einfo) -> None:

        privacy_request_id = kwargs["privacy_request_id"]
        with self.session as db:
            # fixme: net new functionality- needs review. Previously we didn't set privacy request to error state upon email failure
            privacy_request = PrivacyRequest.get(db, object_id=privacy_request_id)
            privacy_request.cache_failed_checkpoint_details(
                step=CurrentStep.erasure_email_post_send, collection=None
            )
            privacy_request.error_processing(db=db)
            sync_send_analytics_event_wrapper(
                failed_graph_analytics_event(privacy_request, exc)
            )
            # If dev mode, log traceback
            _log_exception(exc, config.dev_mode)

    def on_success(self, retval, task_id, args, kwargs):
        privacy_request_id = kwargs["privacy_request_id"]
        policy_id = kwargs["policy_id"]
        access_result_urls = kwargs["access_result_urls"]
        identity_data = kwargs["identity_data"]
        with self.session as db:
            privacy_request = PrivacyRequest.get(db, object_id=privacy_request_id)

            from fidesops.ops.service.privacy_request.request_runner_service import (  # pylint: disable=R0401
                run_webhooks_and_report_status,
            )

            # Run post-execution webhooks
            proceed = run_webhooks_and_report_status(
                db=db,
                privacy_request=privacy_request,
                webhook_cls=PolicyPostWebhook,  # type: ignore
            )
            if not proceed:
                return
            if config.notifications.send_request_completion_notification:
                dispatch_email_task_request_completion.apply_async(
                    queue=EMAIL_QUEUE_NAME,
                    kwargs={
                        "privacy_request_id": privacy_request.id,
                        "to_email": identity_data.get(ProvidedIdentityType.email.value),
                        "access_result_urls": access_result_urls,
                        "policy_id": policy_id,
                    },
                )
            else:
                privacy_request.finished_processing_at = datetime.utcnow()
                AuditLog.create(
                    db=db,
                    data={
                        "user_id": "system",
                        "privacy_request_id": privacy_request.id,
                        "action": AuditLogAction.finished,
                        "message": "",
                    },
                )
                privacy_request.status = PrivacyRequestStatus.complete
                logging.info("Privacy request %s run completed.", privacy_request.id)
                privacy_request.save(db=db)


@celery_app.task(base=EmailTaskEmailConnector, bind=True)
def dispatch_email_task_email_connector(
    self: DatabaseTask,
    emails_to_send: List[Dict[str, Any]],
    policy_key: str,
    privacy_request_id: str,
    access_result_urls: List[str],
    identity_data: Dict[str, Any],
) -> None:
    """
    A wrapper function to dispatch an email task into the Celery queues
    """

    # The on_success celery handler only runs once, after success of entire task,
    # but here we need know which dataset(s) to log upon success of each email in batch.
    # so we need to pass in an on_success for each dispatch call
    def on_success(session: Session, kwargs: Dict[str, Any]):
        logger.info(
            "Email send succeeded for request '%s' for dataset: '%s'",
            privacy_request_id,
            kwargs["dataset_key"],
        )
        AuditLog.create(
            db=session,
            data={
                "user_id": "system",
                "privacy_request_id": kwargs["pr_id"],
                "action": AuditLogAction.email_sent,
                "message": f"Erasure email instructions dispatched for '{kwargs['dataset_key']}'",
            },
        )
    for email in emails_to_send:
        parsed: EmailConnectorEmail = EmailConnectorEmail.parse_obj(email)
        schema = FidesopsEmail.parse_obj(parsed.email_meta)

        with self.session as db:
            dispatch_email(
                db,
                schema.action_type,
                parsed.to_email,
                schema.body_params,
                on_success=on_success,
                on_success_kwargs={
                    "pr_id": privacy_request_id,
                    "dataset_key": parsed.dataset_key
                }
            )


@celery_app.task(base=DatabaseTask, bind=True)
def dispatch_email_task_generic(
    self: DatabaseTask, email_meta: Dict[str, Any], to_email: str
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
    email_body_params: Optional[
        Union[
            AccessRequestCompleteBodyParams,
            SubjectIdentityVerificationBodyParams,
            RequestReceiptBodyParams,
            RequestReviewDenyBodyParams,
            List[CheckpointActionRequired],
        ]
    ] = None,
    on_success: Any = None,
    on_success_kwargs: Dict[str, Any] = None,
) -> None:
    """
    Sends an email to `to_email` with content supplied in `email_body_params`
    """
    if not to_email:
        logger.error("Email failed to send. No email supplied.")
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
    if on_success:
        on_success(db, on_success_kwargs)


def _build_email(  # pylint: disable=too-many-return-statements
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
    if action_type == EmailActionType.PRIVACY_REQUEST_RECEIPT:
        base_template = get_email_template(action_type)
        return EmailForActionType(
            subject="Your request has been received",
            body=base_template.render({"request_types": body_params.request_types}),
        )
    if action_type == EmailActionType.PRIVACY_REQUEST_COMPLETE_ACCESS:
        base_template = get_email_template(action_type)
        return EmailForActionType(
            subject="Your data is ready to be downloaded",
            body=base_template.render(
                {
                    "download_links": body_params.download_links,
                }
            ),
        )
    if action_type == EmailActionType.PRIVACY_REQUEST_COMPLETE_DELETION:
        base_template = get_email_template(action_type)
        return EmailForActionType(
            subject="Your data has been deleted",
            body=base_template.render(),
        )
    if action_type == EmailActionType.PRIVACY_REQUEST_REVIEW_APPROVE:
        base_template = get_email_template(action_type)
        return EmailForActionType(
            subject="Your request has been approved",
            body=base_template.render(),
        )
    if action_type == EmailActionType.PRIVACY_REQUEST_REVIEW_DENY:
        base_template = get_email_template(action_type)
        return EmailForActionType(
            subject="Your request has been denied",
            body=base_template.render(
                {"rejection_reason": body_params.rejection_reason}
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
        raise EmailDispatchException(f"Email failed to send due to: {Pii(e)}")
