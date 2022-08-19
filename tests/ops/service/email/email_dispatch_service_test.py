from unittest import mock
from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from fidesops.ops.common_exceptions import EmailDispatchException
from fidesops.ops.models.email import EmailConfig
from fidesops.ops.schemas.email.email import (
    EmailActionType,
    EmailForActionType,
    EmailServiceDetails,
    EmailServiceType,
    SubjectIdentityVerificationBodyParams,
)
from fidesops.ops.service.email.email_dispatch_service import dispatch_email


@mock.patch("fidesops.ops.service.email.email_dispatch_service._mailgun_dispatcher")
def test_email_dispatch_mailgun_success(
    mock_mailgun_dispatcher: Mock, db: Session, email_config
) -> None:

    dispatch_email(
        db=db,
        action_type=EmailActionType.SUBJECT_IDENTITY_VERIFICATION,
        to_email="test@email.com",
        email_body_params=SubjectIdentityVerificationBodyParams(access_code="2348"),
    )

    mock_mailgun_dispatcher.assert_called_with(
        email_config=email_config,
        email=EmailForActionType(
            subject="Your one-time code",
            body=f"<html>Your one-time code is 2348. Hurry! It expires in 10 minutes.</html>",
        ),
        to_email="test@email.com",
    )


@mock.patch("fidesops.ops.service.email.email_dispatch_service._mailgun_dispatcher")
def test_email_dispatch_mailgun_config_not_found(
    mock_mailgun_dispatcher: Mock, db: Session
) -> None:

    with pytest.raises(EmailDispatchException) as exc:
        dispatch_email(
            db=db,
            action_type=EmailActionType.SUBJECT_IDENTITY_VERIFICATION,
            to_email="test@email.com",
            email_body_params=SubjectIdentityVerificationBodyParams(access_code="2348"),
        )
    assert exc.value.args[0] == "No email config found."

    mock_mailgun_dispatcher.assert_not_called()


@mock.patch("fidesops.ops.service.email.email_dispatch_service._mailgun_dispatcher")
def test_email_dispatch_mailgun_config_no_secrets(
    mock_mailgun_dispatcher: Mock, db: Session
) -> None:

    email_config = EmailConfig.create(
        db=db,
        data={
            "name": "mailgun config",
            "key": "my_email_config",
            "service_type": EmailServiceType.MAILGUN,
            "details": {
                EmailServiceDetails.DOMAIN.value: "some.domain",
            },
        },
    )

    with pytest.raises(EmailDispatchException) as exc:
        dispatch_email(
            db=db,
            action_type=EmailActionType.SUBJECT_IDENTITY_VERIFICATION,
            to_email="test@email.com",
            email_body_params=SubjectIdentityVerificationBodyParams(access_code="2348"),
        )
    assert (
        exc.value.args[0]
        == "Email secrets not found for config with key: my_email_config"
    )

    mock_mailgun_dispatcher.assert_not_called()

    email_config.delete(db)
