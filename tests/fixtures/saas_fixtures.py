import json
from fidesops.service.connectors.saas_connector import SaaSConnector
from fidesops.service.masking.strategy.masking_strategy_hmac import HMAC
from fidesops.util.data_category import DataCategory
import pytest
import os
from fidesops.models.client import ClientDetail
from fidesops.models.policy import ActionType, Policy, Rule, RuleTarget
from fidesops.models.storage import StorageConfig
from fidesops.schemas.saas.saas_config import SaaSConfig
import pydash
import yaml

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import ObjectDeletedError
from typing import Dict, Generator


from fidesops.core.config import load_file, load_toml
from fidesops.models.connectionconfig import (
    AccessLevel,
    ConnectionConfig,
    ConnectionType,
)
from fidesops.models.datasetconfig import DatasetConfig
from fidesops.service.masking.strategy.masking_strategy_string_rewrite import (
    STRING_REWRITE,
)
from tests.fixtures.application_fixtures import load_dataset


saas_config = load_toml("saas_config.toml")

saas_secrets_dict = {
    "mailchimp": {
        "domain": pydash.get(saas_config, "mailchimp.domain")
        or os.environ.get("MAILCHIMP_DOMAIN"),
        "username": pydash.get(saas_config, "mailchimp.username")
        or os.environ.get("MAILCHIMP_USERNAME"),
        "api_key": pydash.get(saas_config, "mailchimp.api_key")
        or os.environ.get("MAILCHIMP_API_KEY"),
    }
}


def load_config(filename: str) -> Dict:
    yaml_file = load_file(filename)
    with open(yaml_file, "r") as file:
        return yaml.safe_load(file).get("saas_config", [])


@pytest.fixture
def example_saas_configs() -> Dict[str, Dict]:
    example_saas_configs = {}
    example_saas_configs["mailchimp"] = load_config(
        "data/saas/config/mailchimp_config.yml"
    )[0]
    return example_saas_configs


@pytest.fixture
def example_saas_datasets() -> Dict[str, Dict]:
    example_saas_datasets = {}
    example_saas_datasets["mailchimp"] = load_dataset(
        "data/saas/dataset/mailchimp_dataset.yml"
    )[0]
    return example_saas_datasets


@pytest.fixture
def dataset_config_saas(
    db: Session,
    connection_config_saas: ConnectionConfig,
    example_saas_datasets: Dict[str, Dict],
) -> Generator:
    saas_dataset = example_saas_datasets["mailchimp"]
    fides_key = saas_dataset["fides_key"]
    connection_config_saas.name = fides_key
    connection_config_saas.key = fides_key
    connection_config_saas.save(db=db)
    dataset = DatasetConfig.create(
        db=db,
        data={
            "connection_config_id": connection_config_saas.id,
            "fides_key": fides_key,
            "dataset": saas_dataset,
        },
    )
    yield dataset
    dataset.delete(db=db)


@pytest.fixture(scope="function")
def connection_config_saas(
    db: Session,
    example_saas_configs: Dict[str, Dict],
) -> Generator:
    saas_config = SaaSConfig(**example_saas_configs["mailchimp"])
    connection_config = ConnectionConfig.create(
        db=db,
        data={
            "key": saas_config.fides_key,
            "name": saas_config.fides_key,
            "connection_type": ConnectionType.saas,
            "access": AccessLevel.write,
            "secrets": saas_secrets_dict["mailchimp"],
            "saas_config": example_saas_configs["mailchimp"],
        },
    )
    yield connection_config
    connection_config.delete(db)


@pytest.fixture(scope="function")
def erasure_policy_string_rewrite(
    db: Session,
    oauth_client: ClientDetail,
    storage_config: StorageConfig,
) -> Generator:
    erasure_policy = Policy.create(
        db=db,
        data={
            "name": "SaaS string rewrite policy",
            "key": "saas_string_rewrite_policy",
            "client_id": oauth_client.id,
        },
    )

    erasure_rule = Rule.create(
        db=db,
        data={
            "action_type": ActionType.erasure.value,
            "client_id": oauth_client.id,
            "name": "SaaS Erasure Rule",
            "policy_id": erasure_policy.id,
            "masking_strategy": {
                "strategy": STRING_REWRITE,
                "configuration": {"rewrite_value": "MASKED"},
            },
        },
    )

    erasure_rule_target = RuleTarget.create(
        db=db,
        data={
            "client_id": oauth_client.id,
            "data_category": DataCategory("user.provided.identifiable.name").value,
            "rule_id": erasure_rule.id,
        },
    )

    yield erasure_policy
    try:
        erasure_rule_target.delete(db)
    except ObjectDeletedError:
        pass
    try:
        erasure_rule.delete(db)
    except ObjectDeletedError:
        pass
    try:
        erasure_policy.delete(db)
    except ObjectDeletedError:
        pass


@pytest.fixture(scope="function")
def erasure_policy_hmac(
    db: Session,
    oauth_client: ClientDetail,
    storage_config: StorageConfig,
) -> Generator:
    erasure_policy = Policy.create(
        db=db,
        data={
            "name": "SaaS hmac policy",
            "key": "saas_hmac_policy",
            "client_id": oauth_client.id,
        },
    )

    erasure_rule = Rule.create(
        db=db,
        data={
            "action_type": ActionType.erasure.value,
            "client_id": oauth_client.id,
            "name": "SaaS Erasure Rule",
            "policy_id": erasure_policy.id,
            "masking_strategy": {
                "strategy": HMAC,
                "configuration": {},
            },
        },
    )

    erasure_rule_target = RuleTarget.create(
        db=db,
        data={
            "client_id": oauth_client.id,
            "data_category": DataCategory("user.provided.identifiable.name").value,
            "rule_id": erasure_rule.id,
        },
    )

    yield erasure_policy
    try:
        erasure_rule_target.delete(db)
    except ObjectDeletedError:
        pass
    try:
        erasure_rule.delete(db)
    except ObjectDeletedError:
        pass
    try:
        erasure_policy.delete(db)
    except ObjectDeletedError:
        pass


@pytest.fixture(scope="function")
def saas_secrets():
    return saas_secrets_dict["mailchimp"]


@pytest.fixture(scope="function")
def mailchimp_account_email():
    return pydash.get(saas_config, "mailchimp.account_email") or os.environ.get(
        "MAILCHIMP_ACCOUNT_EMAIL"
    )


@pytest.fixture(scope="function")
def reset_saas_data(connection_config_saas, mailchimp_account_email) -> Generator:
    """
    Gets the current value of the resource and restores it after the test is complete.
    Used for erasure tests.
    """
    connector = SaaSConnector(connection_config_saas)
    request = (
        "GET",
        "/3.0/search-members",
        {"query": mailchimp_account_email},
        {},
    )
    response = connector.create_client().send(request)
    body = response.json()
    member = body["exact_matches"]["members"][0]
    yield member
    request = (
        "PUT",
        f'/3.0/lists/{member["list_id"]}/members/{member["id"]}',
        {},
        json.dumps(member),
    )
    connector.create_client().send(request)
