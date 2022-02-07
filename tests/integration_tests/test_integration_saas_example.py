import random
import pytest
from fidesops.graph.graph import DatasetGraph
from fidesops.models.datasetconfig import convert_dataset_to_graph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.models.saasconfig import SaaSConfig
from fidesops.schemas.dataset import FidesopsDataset

from fidesops.service.connectors import get_connector
from fidesops.models.connectionconfig import ConnectionTestStatus
from fidesops.task import graph_task
from fidesops.util.saas_util import merge_datasets

from tests.graph.graph_test_util import assert_rows_match, records_matching_fields


@pytest.mark.saas_connector
def test_saas_test_connection(integration_saas_connection_configs) -> None:
    """Dynamic connection test based on the SaaS config"""
    for saas_connection_config in integration_saas_connection_configs.values():
        connector = get_connector(saas_connection_config)
        assert connector.test_connection() == ConnectionTestStatus.succeeded

@pytest.mark.saas_connector
def test_saas_access_request_task(
    db, policy, integration_saas_connection_configs, example_saas_configs, example_saas_datasets, mailchimp_account_email
) -> None:
    """Full access request based on the Mailchimp SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_saas_access_request_task_{random.randint(0, 1000)}"
    )

    saas_config = SaaSConfig(**example_saas_configs["mailchimp"])
    mailchimp_config_dataset = saas_config.generate_dataset()
    mailchimp_dataset = convert_dataset_to_graph(
        FidesopsDataset(**example_saas_datasets["mailchimp"]), "mailchimp_connector"
    )
    merged_dataset = merge_datasets(mailchimp_dataset, mailchimp_config_dataset)
    graph = DatasetGraph(merged_dataset)

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [integration_saas_connection_configs["mailchimp"]],
        {"email": mailchimp_account_email},
    )

    assert_rows_match(
        v["mailchimp_connector:member"],
        min_size=1,
        keys=[
            "id",
            "list_id",
            "email_address",
            "unique_email_id",
            "web_id",
            "email_type",
            "status",
            "merge_fields",
            "ip_signup",
            "timestamp_signup",
            "ip_opt",
            "timestamp_opt",
            "language",
            "email_client",
            "location",
            "source",
            "tags",
        ],
    )
    assert_rows_match(
        v["mailchimp_connector:conversations"],
        min_size=2,
        keys=["id", "campaign_id", "list_id"],
    )
    assert_rows_match(
        v["mailchimp_connector:messages"],
        min_size=7,
        keys=[
            "id",
            "conversation_id",
            "from_label",
            "from_email",
            "subject",
            "message",
            "read",
            "timestamp",
        ],
    )

    # links
    assert v["mailchimp_connector:member"][0]["email_address"] == mailchimp_account_email

    logs = (
        ExecutionLog.query(db=db)
        .filter(ExecutionLog.privacy_request_id == privacy_request.id)
        .all()
    )

    logs = [log.__dict__ for log in logs]
    assert (
        len(
            records_matching_fields(
                logs, dataset_name="mailchimp_connector", collection_name="member"
            )
        )
        > 0
    )
    assert (
        len(
            records_matching_fields(
                logs, dataset_name="mailchimp_connector", collection_name="conversations"
            )
        )
        > 0
    )
    assert (
        len(
            records_matching_fields(
                logs, dataset_name="mailchimp_connector", collection_name="messages"
            )
        )
        > 0
    )