import pytest
from fastapi_pagination import Params
from starlette.testclient import TestClient

from fidesops.api.v1.scope_registry import CONNECTION_READ, CONNECTION_TYPE_READ
from fidesops.api.v1.urn_registry import CONNECTION_TYPES, V1_URL_PREFIX
from fidesops.models.client import ClientDetail


class TestGetConnections:
    @pytest.fixture(scope="function")
    def url(self, oauth_client: ClientDetail, policy) -> str:
        return V1_URL_PREFIX + CONNECTION_TYPES

    def test_get_connection_types_not_authenticated(self, api_client, url):
        resp = api_client.get(url, headers={})
        assert resp.status_code == 401

    def test_get_connection_types_forbidden(
        self, api_client, url, generate_auth_header
    ):
        auth_header = generate_auth_header(scopes=[CONNECTION_READ])
        resp = api_client.get(url, headers=auth_header)
        assert resp.status_code == 403

    def test_get_connection_types(
        self, api_client: TestClient, generate_auth_header, url
    ) -> None:
        auth_header = generate_auth_header(scopes=[CONNECTION_TYPE_READ])
        resp = api_client.get(url, headers=auth_header)
        data = resp.json()
        assert resp.status_code == 200
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert data["size"] == Params().size

        assert "postgres" in data["items"]
        assert "stripe" in data["items"]

        assert "saas" not in data["items"]
        assert "https" not in data["items"]
        assert "custom" not in data["items"]
        assert "manual" not in data["items"]

    def test_search_connection_types(self, api_client, generate_auth_header, url):
        auth_header = generate_auth_header(scopes=[CONNECTION_TYPE_READ])

        resp = api_client.get(url + "?search=str", headers=auth_header)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert data["items"][0] == "stripe"

        resp = api_client.get(url + "?search=re", headers=auth_header)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert data["items"] == ["outreach", "postgres", "redshift"]
