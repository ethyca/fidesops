import pytest
from starlette.testclient import TestClient

from fidesops.ops.api.v1.scope_registry import EMAIL_READ, IDENTITY_VERIFICATION_READ
from fidesops.ops.api.v1.urn_registry import ID_VERIFICATION_CONFIG, V1_URL_PREFIX
from fidesops.ops.core.config import config


class TestGetIdentityVerificationConfig:
    @pytest.fixture(scope="function")
    def url(self) -> str:
        return V1_URL_PREFIX + ID_VERIFICATION_CONFIG

    @pytest.fixture(scope="function")
    def subject_identity_verification_required(self):
        """Override autouse fixture to enable identity verification for tests"""
        original_value = config.execution.subject_identity_verification_required
        config.execution.subject_identity_verification_required = True
        yield
        config.execution.subject_identity_verification_required = original_value

    def test_get_id_verification_config_not_authenticated(
        self, api_client: TestClient, url
    ):
        response = api_client.get(url, headers={})
        assert 401 == response.status_code

    def test_get_id_verification_config_incorrect_scope(
        self,
        api_client: TestClient,
        url,
        generate_auth_header,
    ):
        auth_header = generate_auth_header([EMAIL_READ])
        response = api_client.get(url, headers=auth_header)
        assert 403 == response.status_code

    def test_get_config_with_verification_required_no_email_config(
        self,
        url,
        db,
        api_client: TestClient,
        subject_identity_verification_required,
        generate_auth_header,
    ):
        auth_header = generate_auth_header([IDENTITY_VERIFICATION_READ])
        resp = api_client.get(url, headers=auth_header)
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data["identity_verification_required"] is True
        assert response_data["valid_email_config_exists"] is False

    def test_get_config_with_verification_required_with_email_config(
        self,
        url,
        db,
        api_client: TestClient,
        email_config,
        subject_identity_verification_required,
        generate_auth_header,
    ):
        auth_header = generate_auth_header([IDENTITY_VERIFICATION_READ])
        resp = api_client.get(url, headers=auth_header)
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data["identity_verification_required"] is True
        assert response_data["valid_email_config_exists"] is True

    def test_get_config_with_verification_not_required_with_email_config(
        self,
        url,
        db,
        api_client: TestClient,
        email_config,
        generate_auth_header,
    ):
        auth_header = generate_auth_header([IDENTITY_VERIFICATION_READ])
        resp = api_client.get(url, headers=auth_header)
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data["identity_verification_required"] is False
        assert response_data["valid_email_config_exists"] is True

    def test_get_config_with_verification_not_required_with_no_email_config(
        self,
        url,
        db,
        api_client: TestClient,
        generate_auth_header,
    ):
        auth_header = generate_auth_header([IDENTITY_VERIFICATION_READ])
        resp = api_client.get(url, headers=auth_header)
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data["identity_verification_required"] is False
        assert response_data["valid_email_config_exists"] is False
