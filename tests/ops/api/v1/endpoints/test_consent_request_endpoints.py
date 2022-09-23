from unittest.mock import patch

import pytest

from fidesops.ops.api.v1.urn_registry import (
    CONSENT_REQUEST,
    CONSENT_REQUEST_VERIFY,
    V1_URL_PREFIX,
)
from fidesops.ops.models.privacy_request import ConsentRequest


@pytest.mark.usefixtures(
    "db",
    "email_config",
    "email_connection_config",
    "email_dataset_config",
    "subject_identity_verification_required",
)
@patch("fidesops.ops.service.email.email_dispatch_service.dispatch_email")
def test_consent_request_request(
    mock_dispatch_email,
    api_client,
):
    data = {"email": "test@example.com"}
    response = api_client.post(f"{V1_URL_PREFIX}{CONSENT_REQUEST}", json=data)
    assert response.status_code == 200
    assert response.json()["identity"]["email"] == data["email"]
    assert not mock_dispatch_email.called
