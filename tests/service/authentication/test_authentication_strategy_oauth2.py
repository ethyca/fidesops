from requests import PreparedRequest, Request

from fidesops.service.authentication.authentication_strategy_factory import get_strategy


def test_oauth2_authentication():
    req: PreparedRequest = Request(method="POST", url="https://localhost").prepare()

    domain = "localhost"
    client_id = "client"
    client_secret = "secret"
    redirect_uri = "https://auth.ethyca.com/callback"
    access_token = "access"
    refresh_token = "refresh"

    secrets = {
        "domain": domain,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "access_token": access_token,
        "refersh_token": refresh_token,
    }

    authenticated_request = get_strategy(
        "oauth2",
        {
            "authorization_request": {
                "method": "GET",
                "path": "/auth/authorize",
                "query_params": [
                    {"name": "client_id", "value": "<client_id>"},
                    {"name": "redirect_uri", "value": "<redirect_uri>"},
                    {"name": "response_type", "value": "code"},
                    {
                        "name": "scope",
                        "value": "full_access",
                    },
                ],
            },
            "token_request": {
                "method": "POST",
                "path": "/oauth/token",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": "application/x-www-form-urlencoded",
                    }
                ],
                "query_params": [
                    {"name": "client_id", "value": "<client_id>"},
                    {"name": "client_secret", "value": "<client_secret>"},
                    {"name": "grant_type", "value": "authorization_code"},
                    {"name": "code", "value": "<code>"},
                    {"name": "redirect_uri", "value": "<redirect_uri>"},
                ],
            },
            "refresh_request": {
                "method": "POST",
                "path": "/oauth/token",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": "application/x-www-form-urlencoded",
                    }
                ],
                "query_params": [
                    {"name": "client_id", "value": "<client_id>"},
                    {"name": "client_secret", "value": "<client_secret>"},
                    {"name": "redirect_uri", "value": "<redirect_uri>"},
                    {"name": "grant_type", "value": "refresh_token"},
                    {"name": "refresh_token", "value": "<refresh_token>"},
                ],
            },
        },
    ).add_authentication(req, secrets)
    assert authenticated_request.headers["Authorization"] == f"Bearer {access_token}"
