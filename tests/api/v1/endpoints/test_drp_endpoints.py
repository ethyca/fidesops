
from datetime import datetime
from unittest import mock

import jwt
import pytest
from starlette.testclient import TestClient

from fidesops.api.v1.urn_registry import (
    V1_URL_PREFIX, DRP_EXERCISE,
)
from fidesops.core.config import config

from fidesops.models.client import ClientDetail
from fidesops.models.privacy_request import (
    PrivacyRequest,
)
from fidesops.util.cache import get_drp_request_body_cache_key


class TestCreateDrpPrivacyRequest:
    @pytest.fixture(scope="function")
    def url(self, oauth_client: ClientDetail, policy) -> str:
        return V1_URL_PREFIX + DRP_EXERCISE

    @mock.patch(
        "fidesops.service.privacy_request.request_runner_service.PrivacyRequestRunner.submit"
    )
    def test_create_drp_privacy_request(
            self,
            run_access_request_mock,
            url,
            db,
            api_client: TestClient,
            policy_drp_action,
            cache,
    ):

        config.security.DRP_JWT_SECRET = "secret"
        identity = {"email": "test@example.com"}
        encoded_identity: str = jwt.encode(identity, config.security.DRP_JWT_SECRET, algorithms="HS256")
        data = {
                "meta": {"version": "0.5"},
                "regime": "ccpa",
                "exercise": [
                    "access"
                ],
                "identity": encoded_identity,
            }
        resp = api_client.post(url, json=data)
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data["status"] == "test"
        assert response_data["received_at"]
        assert response_data["request_id"]
        pr = PrivacyRequest.get(db=db, id=response_data["request_id"])

        # test body of req is cached
        key = get_drp_request_body_cache_key(
            privacy_request_id=pr.id,
            identity_attribute="email",
        )
        assert cache.get(key) == identity["email"]
        pr.delete(db=db)
        assert run_access_request_mock.called
        config.security.DRP_JWT_SECRET = None

    def test_create_drp_privacy_request_no_jwt(
            self,
            url,
            db,
            api_client: TestClient,
            policy_drp_action,
    ):

        identity = {"email": "test@example.com"}
        encoded_identity: str = jwt.encode(identity, "secret", algorithms="HS256")
        data = {
            "meta": {"version": "0.5"},
            "regime": "ccpa",
            "exercise": [
                "access"
            ],
            "identity": encoded_identity,
        }
        resp = api_client.post(url, json=data)
        assert resp.status_code == 400

    def test_create_drp_privacy_request_no_exercise(
            self,
            url,
            db,
            api_client: TestClient,
            policy_drp_action,
    ):

        config.security.DRP_JWT_SECRET = "secret"
        identity = {"email": "test@example.com"}
        encoded_identity: str = jwt.encode(identity, config.security.DRP_JWT_SECRET, algorithms="HS256")
        data = {
            "meta": {"version": "0.5"},
            "regime": "ccpa",
            "exercise": None,
            "identity": encoded_identity,
        }
        resp = api_client.post(url, json=data)
        assert resp.status_code == 400
        config.security.DRP_JWT_SECRET = None

    def test_create_drp_privacy_request_invalid_exercise(
            self,
            url,
            db,
            api_client: TestClient,
            policy_drp_action,
    ):

        config.security.DRP_JWT_SECRET = "secret"
        identity = {"email": "test@example.com"}
        encoded_identity: str = jwt.encode(identity, config.security.DRP_JWT_SECRET, algorithms="HS256")
        data = {
            "meta": {"version": "0.5"},
            "regime": "ccpa",
            "exercise": {"access", "deletion"},
            "identity": encoded_identity,
        }
        resp = api_client.post(url, json=data)
        assert resp.status_code == 422
        config.security.DRP_JWT_SECRET = None

    def test_create_drp_privacy_request_no_associated_policy(
            self,
            url,
            db,
            api_client: TestClient,
            policy,
    ):

        config.security.DRP_JWT_SECRET = "secret"
        identity = {"email": "test@example.com"}
        encoded_identity: str = jwt.encode(identity, config.security.DRP_JWT_SECRET, algorithms="HS256")
        data = {
            "meta": {"version": "0.5"},
            "regime": "ccpa",
            "exercise": {"access", "deletion"},
            "identity": encoded_identity,
        }
        resp = api_client.post(url, json=data)
        assert resp.status_code == 494
        config.security.DRP_JWT_SECRET = None
