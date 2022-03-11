import json
import pytest
from requests import Response
from fidesops.schemas.saas.strategy_configuration import LinkPaginationConfiguration
from fidesops.schemas.saas.shared_schemas import SaaSRequestParams
from fidesops.service.pagination.pagination_strategy_link import LinkPaginationStrategy


@pytest.fixture(scope="function")
def response_with_header_link():
    response = Response()
    response.headers = {"link": "<https://domain.com/customers?page=def>; rel=next"}
    return response


@pytest.fixture(scope="function")
def response_with_body():
    response = Response()
    response._content = bytes(
        json.dumps({"links": {"next": "https://domain.com/customers?page=def"}}), "utf-8"
    )
    return response


def test_link_in_headers(response_with_header_link):
    config = LinkPaginationConfiguration(source="headers", rel="next")
    request_params: SaaSRequestParams = "GET", "/customers", {"page": "abc"}, None

    paginator = LinkPaginationStrategy(config)
    next_request: SaaSRequestParams = paginator.get_next_request(
        request_params, {}, response_with_header_link
    )
    assert next_request == ("GET", "/customers", {"page": "def"}, None)


def test_link_in_headers_missing():
    config = LinkPaginationConfiguration(source="headers", rel="next")
    request_params: SaaSRequestParams = "GET", "/customers", {"page": "abc"}, None

    paginator = LinkPaginationStrategy(config)
    next_request: SaaSRequestParams = paginator.get_next_request(
        request_params, {}, Response()
    )
    assert next_request == None


def test_link_in_response(response_with_body):
    config = LinkPaginationConfiguration(source="body", path="links.next")
    request_params: SaaSRequestParams = "GET", "/customers", {"page": "abc"}, None

    paginator = LinkPaginationStrategy(config)
    next_request: SaaSRequestParams = paginator.get_next_request(
        request_params, {}, response_with_body
    )
    assert next_request == ("GET", "/customers", {"page": "def"}, None)


def test_link_in_response_missing():
    config = LinkPaginationConfiguration(source="body", path="links.next")
    request_params: SaaSRequestParams = "GET", "/customers", {"page": "abc"}, None

    paginator = LinkPaginationStrategy(config)
    next_request: SaaSRequestParams = paginator.get_next_request(
        request_params, {}, Response()
    )
    assert next_request == None


def test_wrong_source():
    with pytest.raises(ValueError) as exc:
        LinkPaginationConfiguration(source="somewhere", path="links.next")
    assert "unexpected value" in str(exc.value)


def test_config_mismatch():
    with pytest.raises(ValueError) as exc:
        LinkPaginationConfiguration(source="headers", path="links.next")
    assert (
        "The 'rel' value must be specified when accessing the link from the headers"
        in str(exc.value)
    )

    with pytest.raises(ValueError) as exc:
        LinkPaginationConfiguration(source="body", rel="next")
    assert (
        "The 'path' value must be specified when accessing the link from the body"
        in str(exc.value)
    )
