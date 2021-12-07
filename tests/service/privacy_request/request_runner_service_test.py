from unittest import mock
from unittest.mock import Mock

from sqlalchemy.orm import Session
from pydantic import ValidationError

from fidesops.common_exceptions import PrivacyRequestPaused, ClientUnsuccessfulException
from fidesops.models.policy import PolicyPreWebhook
from fidesops.models.privacy_request import PrivacyRequest, PrivacyRequestStatus
from fidesops.schemas.external_https import SecondPartyResponseFormat
from fidesops.service.privacy_request.request_runner_service import PrivacyRequestRunner


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
    privacy_request_runner.run()
    assert privacy_request.finished_processing_at is not None
    assert upload_mock.called
    assert run_access_request_mock.called


def test_start_processing_sets_started_processing_at(
    db: Session,
    privacy_request: PrivacyRequest,
    privacy_request_runner: PrivacyRequestRunner,
) -> None:
    privacy_request.started_processing_at = None
    privacy_request_runner.start_processing(db=db)
    assert privacy_request.started_processing_at is not None


def test_start_processing_doesnt_overwrite_started_processing_at(
    db: Session,
    privacy_request: PrivacyRequest,
    privacy_request_runner: PrivacyRequestRunner,
) -> None:
    before = privacy_request.started_processing_at
    privacy_request_runner.start_processing(db=db)
    assert privacy_request.started_processing_at == before


class TestPrivacyRequestRunnerRunWebhooks:
    @mock.patch("fidesops.models.privacy_request.PrivacyRequest.trigger_policy_webhook")
    def test_run_webhooks_halt_received(
        self,
        mock_trigger_policy_webhook,
        privacy_request,
        privacy_request_runner,
        policy_pre_execution_webhooks,
    ):
        mock_trigger_policy_webhook.side_effect = PrivacyRequestPaused(
            "Request received to halt"
        )

        proceed = privacy_request_runner.run_webhooks(PolicyPreWebhook)
        assert not proceed
        assert privacy_request.finished_processing_at is None
        assert privacy_request.status == PrivacyRequestStatus.paused

    @mock.patch("fidesops.models.privacy_request.PrivacyRequest.trigger_policy_webhook")
    def test_run_webhooks_client_error(
        self,
        mock_trigger_policy_webhook,
        privacy_request,
        privacy_request_runner,
        policy_pre_execution_webhooks,
    ):
        mock_trigger_policy_webhook.side_effect = ClientUnsuccessfulException(
            status_code=500, message="Received 500 from client-defined endpoint"
        )

        proceed = privacy_request_runner.run_webhooks(PolicyPreWebhook)
        assert not proceed
        assert privacy_request.status == PrivacyRequestStatus.error

    @mock.patch("fidesops.models.privacy_request.PrivacyRequest.trigger_policy_webhook")
    def test_run_webhooks_validation_error(
        self,
        mock_trigger_policy_webhook,
        privacy_request,
        privacy_request_runner,
        policy_pre_execution_webhooks,
    ):
        mock_trigger_policy_webhook.side_effect = ValidationError(
            errors={}, model=SecondPartyResponseFormat
        )

        proceed = privacy_request_runner.run_webhooks(PolicyPreWebhook)
        assert not proceed
        assert privacy_request.finished_processing_at is not None
        assert privacy_request.status == PrivacyRequestStatus.error

    @mock.patch("fidesops.models.privacy_request.PrivacyRequest.trigger_policy_webhook")
    def test_run_webhooks(
        self,
        mock_trigger_policy_webhook,
        privacy_request,
        privacy_request_runner,
        policy_pre_execution_webhooks,
    ):

        proceed = privacy_request_runner.run_webhooks(PolicyPreWebhook)
        assert proceed
        assert privacy_request.status == PrivacyRequestStatus.in_processing
        assert privacy_request.finished_processing_at is None
        assert mock_trigger_policy_webhook.call_count == 2

    @mock.patch("fidesops.models.privacy_request.PrivacyRequest.trigger_policy_webhook")
    def test_run_webhooks_after_webhook(
        self,
        mock_trigger_policy_webhook,
        privacy_request,
        privacy_request_runner,
        policy_pre_execution_webhooks,
    ):
        """Test running webhooks after specific webhook - for when we're resuming privacy request execution"""
        proceed = privacy_request_runner.run_webhooks(
            PolicyPreWebhook, policy_pre_execution_webhooks[0]
        )
        assert proceed
        assert privacy_request.status == PrivacyRequestStatus.in_processing
        assert privacy_request.finished_processing_at is None
        assert mock_trigger_policy_webhook.call_count == 1
