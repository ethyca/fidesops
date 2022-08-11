import json
import logging
import random

import pytest

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import ExecutionLog, PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.schemas.saas.shared_schemas import HTTPMethod, SaaSRequestParams
from fidesops.service.connectors import SaaSConnector
from fidesops.task import graph_task
from fidesops.task.filter_results import filter_data_categories
from fidesops.task.graph_task import get_cached_data_for_erasures
from fidesops.util.saas_util import format_body
from tests.ops.graph.graph_test_util import assert_rows_match, records_matching_fields


logger = logging.getLogger(__name__)


@pytest.mark.integration_saas
@pytest.mark.integration_datadog
def test_saas_access_request_task(
    db,
    policy,
    datadog_connection_config,
    dataset_config_datadog,
    datadog_identity_email,
) -> None:
    """Full access request based on the Hubspot SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_datadog_access_request_task_{random.randint(0, 1000)}"
    )
    identity_attribute = "email"
    identity_value = datadog_identity_email
    identity_kwargs = {identity_attribute: identity_value}
    identity = PrivacyRequestIdentity(**identity_kwargs)
    privacy_request.cache_identity(identity)

    dataset_name = datadog_connection_config.get_saas_config().fides_key
    merged_graph = dataset_config_datadog.get_graph()
    graph = DatasetGraph(merged_graph)

    # import pdb; pdb.set_trace()

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [datadog_connection_config],
        {"email": datadog_identity_email},
        db,
    )

    assert_rows_match(
        v[f"{dataset_name}:events"],
        min_size=1,
        keys=[
            "attributes",
            "type",
            "id",
        ]
    )

    for item in v[f"{dataset_name}:events"]:
        assert_rows_match(
            [item['attributes']],
            min_size=1,
            keys=[
                "status",
                "timestamp",
                "message",
                "tags",
            ]
        )
    logger.info(msg=v[f"{dataset_name}:events"][0]['attributes']['timestamp'])
    logger.info(msg=v[f"{dataset_name}:events"][0]['attributes']['timestamp'])
    logger.info(msg=v[f"{dataset_name}:events"][0]['attributes']['timestamp'])
    logger.info(msg=v[f"{dataset_name}:events"][0]['attributes']['timestamp'])
    logger.info(msg=f"{len(v[f'{dataset_name}:events'])}")
    for item in v[f"{dataset_name}:events"]:
        assert datadog_identity_email in item["attributes"]["message"]

