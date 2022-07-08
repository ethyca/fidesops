import random

import pytest

from fidesops.graph.graph import DatasetGraph
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.schemas.redis_cache import PrivacyRequestIdentity
from fidesops.service.connectors import get_connector
from fidesops.task import graph_task
from tests.graph.graph_test_util  import assert_rows_match


@pytest.mark.integration_saas
@pytest.mark.integration_saas
def test_logiid_connection_test(logiid_connection_config) -> None:
    get_connector(logiid_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_logiid
def test_logiid_access_request_task(
    db,
    policy,
    logiid_connection_config,
    logiid_dataset_config,
    logiid_identity_email,
) -> None:
    """Full access request based on the Logiid SaaS config"""

    privacy_request = PrivacyRequest(
        id=f"test_logiid_access_request_task_{random.randint(0, 1000)}"
    )
    identity = PrivacyRequestIdentity(**{"email": logiid_identity_email})
    privacy_request.cache_identity(identity)

    dataset_name = logiid_connection_config.get_saas_config().fides_key
    merged_graph = logiid_dataset_config.get_graph()
    graph = DatasetGraph(merged_graph)

    v = graph_task.run_access_request(
        privacy_request,
        policy,
        graph,
        [logiid_connection_config],
        {"email": logiid_identity_email},
    )
    