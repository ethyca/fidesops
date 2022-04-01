from starlette.testclient import TestClient


def test_health(api_client: TestClient) -> None:
    url = "http://0.0.0.0:8080/health"
    response = api_client.get(url)
    assert response.json() == {"healthy": True}
