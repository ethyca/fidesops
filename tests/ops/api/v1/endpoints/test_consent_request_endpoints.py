from __future__ import annotations

from copy import deepcopy
from typing import Any
from unittest.mock import patch

import pytest

from fidesops.ops.api.v1.urn_registry import (
    CONSENT_REQUEST,
    CONSENT_REQUEST_PREFERENCES,
    CONSENT_REQUEST_VERIFY,
    V1_URL_PREFIX,
)
from fidesops.ops.models.privacy_request import (
    Consent,
    ConsentRequest,
    ProvidedIdentity,
)


@pytest.fixture
def provided_identity_and_consent_request(db):
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

    yield provided_identity, consent_request


@pytest.mark.usefixtures(
    "email_config",
    "email_connection_config",
    "email_dataset_config",
    "subject_identity_verification_required",
)
@patch("fidesops.ops.service.email.email_dispatch_service.dispatch_email")
def test_consent_request(mock_dispatch_email, api_client):
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
    provided_identity_and_consent_request, api_client
):
    data = {"code": "12345"}

    _, consent_request = provided_identity_and_consent_request
    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id=consent_request.id)}",
        json=data,
    )
    assert response.status_code == 400
    assert "code expired" in response.json()["detail"]


def test_consent_verify_invalid_code(provided_identity_and_consent_request, api_client):
    _, consent_request = provided_identity_and_consent_request
    consent_request.cache_identity_verification_code("abcd")

    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id=consent_request.id)}",
        json={"code": "1234"},
    )
    assert response.status_code == 403
    assert "Incorrect identification" in response.json()["detail"]


def test_consent_verify_no_email_provided(db, api_client):
    provided_identity_data = {
        "privacy_request_id": None,
        "field_name": "email",
        "encrypted_value": None,
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

    assert response.status_code == 404
    assert "missing email" in response.json()["detail"]


def test_consent_verify_no_consent_present(
    provided_identity_and_consent_request, api_client
):
    provided_identity, consent_request = provided_identity_and_consent_request
    verification_code = "abcd"
    consent_request.cache_identity_verification_code(verification_code)

    response = api_client.post(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_VERIFY.format(consent_request_id=consent_request.id)}",
        json={"code": verification_code},
    )
    assert response.status_code == 200
    assert (
        response.json()["identity"]["email"]
        == provided_identity.encrypted_value["value"]
    )
    assert response.json()["consent"] is None


def test_consent_verify_consent_preferences(
    provided_identity_and_consent_request, db, api_client
):
    verification_code = "abcd"
    provided_identity, consent_request = provided_identity_and_consent_request
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
    assert (
        response.json()["identity"]["email"]
        == provided_identity.encrypted_value["value"]
    )
    assert response.json()["consent"] == consent_data


def test_set_consent_preferences_no_cosent_request_id(api_client):
    data = {
        "code": "12345",
        "identity": {"email": "test@email.com"},
        "consent": [{"data_use": "email", "opt_in": True}],
    }

    response = api_client.patch(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_PREFERENCES.format(consent_request_id='abcd')}",
        json=data,
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_set_consent_preferences_no_consent_code(
    provided_identity_and_consent_request, api_client
):
    _, consent_request = provided_identity_and_consent_request

    data = {
        "code": "12345",
        "identity": {"email": "test@email.com"},
        "consent": [{"data_use": "email", "opt_in": True}],
    }

    response = api_client.patch(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_PREFERENCES.format(consent_request_id=consent_request.id)}",
        json=data,
    )
    assert response.status_code == 400
    assert "code expired" in response.json()["detail"]


def test_set_consent_preferences_invalid_code(
    provided_identity_and_consent_request, api_client
):
    _, consent_request = provided_identity_and_consent_request
    consent_request.cache_identity_verification_code("abcd")

    data = {
        "code": "12345",
        "identity": {"email": "test@email.com"},
        "consent": [{"data_use": "email", "opt_in": True}],
    }
    response = api_client.patch(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_PREFERENCES.format(consent_request_id=consent_request.id)}",
        json=data,
    )
    assert response.status_code == 403
    assert "Incorrect identification" in response.json()["detail"]


def test_set_consent_preferences_no_email_provided(db, api_client):
    provided_identity_data = {
        "privacy_request_id": None,
        "field_name": "email",
        "encrypted_value": None,
    }
    provided_identity = ProvidedIdentity.create(db, data=provided_identity_data)

    consent_request_data = {
        "provided_identity_id": provided_identity.id,
    }
    consent_request = ConsentRequest.create(db, data=consent_request_data)
    verification_code = "abcd"
    consent_request.cache_identity_verification_code(verification_code)

    data = {
        "code": verification_code,
        "identity": {"email": "test@email.com"},
        "consent": [{"data_use": "email", "opt_in": True}],
    }
    response = api_client.patch(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_PREFERENCES.format(consent_request_id=consent_request.id)}",
        json=data,
    )

    assert response.status_code == 404
    assert "missing email" in response.json()["detail"]


def test_set_consent_preferences_no_consent_present(
    provided_identity_and_consent_request, api_client
):
    _, consent_request = provided_identity_and_consent_request
    verification_code = "abcd"
    consent_request.cache_identity_verification_code(verification_code)

    data = {
        "code": verification_code,
        "identity": {"email": "test@email.com"},
        "consent": None,
    }
    response = api_client.patch(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_PREFERENCES.format(consent_request_id=consent_request.id)}",
        json=data,
    )
    assert response.status_code == 400
    assert "No consent" in response.json()["detail"]


def test_set_consent_consent_preferences(
    provided_identity_and_consent_request, db, api_client
):
    provided_identity, consent_request = provided_identity_and_consent_request
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

    consent_data[1]["opt_in"] = False

    data = {
        "code": verification_code,
        "identity": {"email": "test@email.com"},
        "consent": consent_data,
    }
    response = api_client.patch(
        f"{V1_URL_PREFIX}{CONSENT_REQUEST_PREFERENCES.format(consent_request_id=consent_request.id)}",
        json=data,
    )
    assert response.status_code == 200
    assert (
        response.json()["identity"]["email"]
        == provided_identity.encrypted_value["value"]
    )
    assert response.json()["consent"] == consent_data