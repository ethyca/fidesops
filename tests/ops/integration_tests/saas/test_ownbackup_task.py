import random

import pytest

from fidesops.service.connectors import get_connector


@pytest.mark.integration_saas
@pytest.mark.integration_ownbackup
def test_ownbackup_connection_test(ownbackup_connection_config) -> None:
    get_connector(ownbackup_connection_config).test_connection()


@pytest.mark.integration_saas
@pytest.mark.integration_ownbackup
def test_ownbackup_access_request_task(
    policy,
    ownbackup_identity_email,
    ownbackup_connection_config,
    ownbackup_dataset_config,
    db,
) -> None:
    """Full access request based on the OwnBackup SaaS config"""

    pass


@pytest.mark.integration_saas
@pytest.mark.integration_ownbackup
def test_ownbackup_erasure_request_task(
    db,
    policy,
    erasure_policy_string_rewrite,
    ownbackup_connection_config,
    ownbackup_dataset_config,
    ownbackup_erasure_identity_email,
    ownbackup_create_erasure_data,
) -> None:
    """Full erasure request based on the OwnBackup SaaS config"""

    pass
