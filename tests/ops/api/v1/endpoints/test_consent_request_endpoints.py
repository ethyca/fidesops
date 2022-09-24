from __future__ import annotations

from copy import deepcopy
from typing import Any
from unittest.mock import patch

import pytest

from fidesops.ops.api.v1.urn_registry import (
    CONSENT_REQUEST,
    CONSENT_REQUEST_VERIFY,
    V1_URL_PREFIX,
)
from fidesops.ops.models.privacy_request import (
    Consent,
    ConsentRequest,
    ProvidedIdentity,
)
from fidesops.ops.schemas.privacy_request import ConsentPreferences


@pytest.mark.usefixtures(
    "email_config",
    "email_connection_config",
    "email_dataset_config",
    "subject_identity_verification_required",
)
@patch("fidesops.ops.service.email.email_dispatch_service.dispatch_email")
def test_consent_request(
    mock_dispatch_email,
    api_client,
):
    data = {"email": "test@example.com"}
    response = api_client.post(f"{V1_URL_PREFIX}{CONSENT_REQUEST}", json=data)
    assert response.status_code == 200
    assert response.json()["identity"]["email"] == data["email"]
    assert not mock_dispatch_email.called


def test_consent_verify_no_cosent_request_id(
    api_client,
):
    data = {"code": "12345"}

    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id='abcd')}",
        json=data,
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_consent_verify_no_cosent_code(
    db,
    api_client,
):
    data = {"code": "12345"}

    provided_identity_data = {
        "privacy_request_id": None,
        "field_name": "email",
        "encrypted_value": {"value": "test@email.com"},
    }
    provided_identity = ProvidedIdentity.create(db, data=provided_identity_data)

    consent_request_data = {
        "provided_identity_id": provided_identity.id,
    }
    consent_request = ConsentRequest.create(db, data=consent_request_data)

    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id=consent_request.id)}",
        json=data,
    )
    assert response.status_code == 400
    assert "code expired" in response.json()["detail"]


def test_consent_verify_invalid_code(db, api_client):
    provided_identity_data = {
        "privacy_request_id": None,
        "field_name": "email",
        "encrypted_value": {"value": "test@email.com"},
    }
    provided_identity = ProvidedIdentity.create(db, data=provided_identity_data)

    consent_request_data = {
        "provided_identity_id": provided_identity.id,
    }
    consent_request = ConsentRequest.create(db, data=consent_request_data)
    consent_request.cache_identity_verification_code("abcd")

    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id=consent_request.id)}",
        json={"code": "1234"},
    )
    assert response.status_code == 403
    assert "Incorrect identification" in response.json()["detail"]


def test_consent_verify_no_consent_present(db, api_client):
    email = "test@email.com"
    provided_identity_data = {
        "privacy_request_id": None,
        "field_name": "email",
        "encrypted_value": {"value": email},
    }
    provided_identity = ProvidedIdentity.create(db, data=provided_identity_data)

    consent_request_data = {
        "provided_identity_id": provided_identity.id,
    }
    consent_request = ConsentRequest.create(db, data=consent_request_data)
    verification_code = "abcd"
    consent_request.cache_identity_verification_code(verification_code)

    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id=consent_request.id)}",
        json={"code": verification_code},
    )
    assert response.status_code == 200
    assert response.json()["identity"]["email"] == email
    assert response.json()["consent"] is None


def test_consent_verify_consent_preferences(db, api_client):
    email = "test@email.com"
    provided_identity_data = {
        "privacy_request_id": None,
        "field_name": "email",
        "encrypted_value": {"value": email},
    }
    provided_identity = ProvidedIdentity.create(db, data=provided_identity_data)

    consent_request_data = {
        "provided_identity_id": provided_identity.id,
    }
    consent_request = ConsentRequest.create(db, data=consent_request_data)
    verification_code = "abcd"
    consent_request.cache_identity_verification_code(verification_code)

    consent_data: list[dict[str, Any]] = [
        {
            "data_use": "location",
            "data_use_description": "Location data",
            "opt_in": False,
        },
        {
            "data_use": "email",
            "data_use_description": None,
            "opt_in": True,
        },
    ]

    for data in deepcopy(consent_data):
        data["provided_identity_id"] = provided_identity.id
        Consent.create(db, data=data)

    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id=consent_request.id)}",
        json={"code": verification_code},
    )
    assert response.status_code == 200
    assert response.json()["identity"]["email"] == email
    print(response.json()["consent"])
    print(consent_data)
    assert response.json()["consent"] == consent_data
