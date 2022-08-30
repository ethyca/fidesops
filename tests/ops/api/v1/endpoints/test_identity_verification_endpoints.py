import pytest
from starlette.testclient import TestClient
from fidesops.ops.api.v1.urn_registry import (
    V1_URL_PREFIX, ID_VERIFICATION_CONFIG,
)


class TestGetIdentityVerificationConfig:
    @pytest.fixture(scope="function")
    def url(self) -> str:
        return V1_URL_PREFIX + ID_VERIFICATION_CONFIG

    def test_get_config_with_verification_enabled_no_email_config(
            self,
            url,
            db,
            api_client: TestClient,
    ):

        resp = api_client.get(url)
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data["identity_verification_required"] is True
        assert response_data["valid_email_config_exists"] is False

    def test_get_config_with_verification_enabled_with_email_config(
            self,
            url,
            db,
            api_client: TestClient,
    ):

        resp = api_client.get(url)
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data["identity_verification_required"] is True
        assert response_data["valid_email_config_exists"] is True
