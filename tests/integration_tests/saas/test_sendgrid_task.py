import json
import random
import time

import pytest

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.schemas.saas.shared_schemas import HTTPMethod, SaaSRequestParams
from fidesops.service.connectors import SaaSConnector
from fidesops.task import graph_task
from fidesops.task.graph_task import get_cached_data_for_erasures
from tests.graph.graph_test_util import assert_rows_match


@pytest.mark.integration_saas
@pytest.mark.integration_sendgrid
def test_sendgrid_access_request_task(
    db,
    policy,
    sendgrid_connection_config,
    sendgrid_dataset_config,
    sendgrid_identity_email,
) -> None:
    """Full access request based on the Sendgrid SaaS config"""
    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": sendgrid_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = sendgrid_connection_config.get_saas_config().fides_key
    merged_graph = sendgrid_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [sendgrid_connection_config],
        {"email": sendgrid_identity_email},
    )

    assert_rows_match(
        v[f"{dataset_name}:contacts"],
        min_size=1,
        keys=[
            "id",
            "first_name",
            "last_name",
            "email",
            "alternate_emails",
            "address_line_1",
            "address_line_2",
            "city",
            "state_province_region",
            "country",
            "postal_code",
            "phone_number",
            "whatsapp",
            "list_ids",
            "segment_ids",
            "created_at",
            "updated_at",
        ],
    )


@pytest.mark.integration_saas
@pytest.mark.integration_sendgrid
def test_sendgrid_erasure_request_task(
    db,
    policy,
    erasure_policy_string_rewrite,
    sendgrid_secrets,
    sendgrid_connection_config,
    sendgrid_dataset_config,
    sendgrid_erasure_identity_email,
    sendgrid_erasure_data,
) -> None:
    """Full erasure request based on the sendgrid SaaS config"""
    privacy_request = PrivacyRequest(
        id=f"test_saas_erasure_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": sendgrid_erasure_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = sendgrid_connection_config.get_saas_config().fides_key
    merged_graph = sendgrid_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    # access our erasure identity
    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [sendgrid_connection_config],
        {"email": sendgrid_erasure_identity_email},
    )

    # make sure erasure contact has expected fields
    assert_rows_match(
        v[f"{dataset_name}:contacts"],
        min_size=1,
        keys=[
            "id",
            "first_name",
            "last_name",
            "email",
            "alternate_emails",
            "address_line_1",
            "address_line_2",
            "city",
            "state_province_region",
            "country",
            "postal_code",
            "phone_number",
            "whatsapp",
            "list_ids",
            "segment_ids",
            "created_at",
            "updated_at",
        ],
    )

    erasure = graph_task.run_erasure(
        privacy_request,
        erasure_policy_string_rewrite,
        graph,
        [sendgrid_connection_config],
        {"email": sendgrid_erasure_identity_email},
        get_cached_data_for_erasures(privacy_request.id),
    )

    # masking request only issued to "contacts", for now
    assert erasure == {f"{dataset_name}:contacts": 1}

    # retrieve updated contact record, and verify its firstname is now masked
    # update may take a while (>25s) to propagate, so retry up to 10 times
    connector = SaaSConnector(sendgrid_connection_config)
    retries = 10
    while (
        contact_firstname := _get_contact_firstname(
            sendgrid_erasure_identity_email, connector, sendgrid_secrets
        )
    ) == "MASKED":
        if not retries:
            raise Exception(
                f"Contact with email {sendgrid_erasure_identity_email} was not updated in Sendgrid"
            )
        retries -= 1
        time.sleep(5)


def _get_contact_firstname(
    sendgrid_erasure_identity_email: str, connector: SaaSConnector, sendgrid_secrets
) -> bool:
    """
    Retrieves contact with specified email from Sendgrid
    Returns contact firstname if contact exists, returns None if it does not.
    """
    body = json.dumps({"emails": [sendgrid_erasure_identity_email]})
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sendgrid_secrets['api_key']}",
    }

    contact_request: SaaSRequestParams = SaaSRequestParams(
        method=HTTPMethod.POST,
        path="/v3/marketing/contacts/search/emails",
        headers=headers,
        body=body,
    )
    contact_response = connector.create_client().send(
        contact_request, ignore_errors=True
    )

    # this handles when the contact doesn't exist
    # really a 404 is returned, but the saas client catches the 404
    # and instead just returns a totally empty response object
    if None == contact_response.status_code:
        return None

    # response has result object where keys are contact emails.
    # confirm we get our contact back, and it has the right firstname
    return contact_response.json()["result"][sendgrid_erasure_identity_email][
        "contact"
    ]["first_name"]
