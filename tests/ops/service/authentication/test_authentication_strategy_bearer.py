import pytest
from requests import PreparedRequest, Request

from fidesops.common_exceptions import ValidationError as FidesopsValidationError
from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.service.strategy_factory import strategy


def test_bearer_auth_with_token():
    req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

    api_key = "imnotasecretitsok"
    secrets = {"api_key": api_key}

    authenticated_request = strategy(
        "bearer", {"token": "<api_key>"}
    ).add_authentication(req, ConnectionConfig(secrets=secrets))
    assert authenticated_request.headers["Authorization"] == f"Bearer {api_key}"


def test_bearer_auth_without_token():
    req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

    with pytest.raises(FidesopsValidationError):
        strategy("bearer", {}).add_authentication(req, ConnectionConfig(secrets={}))
