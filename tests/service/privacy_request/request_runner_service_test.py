from unittest import mock
from unittest.mock import Mock

from sqlalchemy.orm import Session

from fidesops.db.session import get_db_session
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.service.privacy_request.request_runner_service import PrivacyRequestRunner
from ...test_support import wait_for_privacy_request


@mock.patch(
    "fidesops.service.privacy_request.request_runner_service.run_access_request"
)
@mock.patch("fidesops.service.privacy_request.request_runner_service.upload")
def test_policy_upload_called(
    upload_mock: Mock,
    run_access_request_mock: Mock,
    db: Session,
    privacy_request: PrivacyRequest,
    privacy_request_runner: PrivacyRequestRunner,
) -> None:
    privacy_request_runner.submit()
    wait_for_privacy_request(db, privacy_request.id)
    assert upload_mock.called
    assert run_access_request_mock.called


def test_start_processing_sets_started_processing_at(
    db: Session,
    privacy_request: PrivacyRequest,
    privacy_request_runner: PrivacyRequestRunner,
) -> None:
    privacy_request.started_processing_at = None
    privacy_request_runner.submit()
    db.commit()
    wait_for_privacy_request(db, privacy_request.id)
    _sessionmaker = get_db_session()
    db = _sessionmaker()
    privacy_request = PrivacyRequest.get(db=db, id=privacy_request.id)
    assert privacy_request.started_processing_at is not None


def test_start_processing_doesnt_overwrite_started_processing_at(
    db: Session,
    privacy_request: PrivacyRequest,
    privacy_request_runner: PrivacyRequestRunner,
) -> None:
    before = privacy_request.started_processing_at
    privacy_request_runner.submit()
    wait_for_privacy_request(db, privacy_request.id)
    privacy_request = PrivacyRequest.get(db=db, id=privacy_request.id)
    assert privacy_request.started_processing_at == before
