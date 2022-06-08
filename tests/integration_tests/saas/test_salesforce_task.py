import pytest
from requests import Response
from starlette.status import HTTP_200_OK

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.schemas.saas.shared_schemas import HTTPMethod, SaaSRequestParams
from fidesops.service.connectors.saas_connector import SaaSConnector
from fidesops.task import graph_task
from fidesops.task.graph_task import get_cached_data_for_erasures
from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.integration_saas
@pytest.mark.integration_salesforce
def test_salesforce_access_request_task(
    db,
    policy,
    salesforce_identity_email,
    salesforce_secrets,
    salesforce_connection_config,
    salesforce_data
) -> None:
    """Test getting a contact (placeholder)
    """
    connector = SaaSConnector(salesforce_connection_config)
    headers = {
        "Authorization": f"Bearer {salesforce_secrets['access_token']}",
    }
    get_contact_request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.GET,
        path=f"/services/data/v54.0/sobjects/Contact/Email/{salesforce_identity_email}",
        headers=headers,
    )
    get_contact_response: Response = connector.create_client().send(get_contact_request)
    assert HTTP_200_OK == get_contact_response.status_code
    assert salesforce_data == get_contact_response.json()['Id']
    

   