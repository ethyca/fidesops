import pytest
from typing import Dict

from fidesops.graph.config import FieldAddress
from fidesops.models.saasconfig import SaaSConfig
from ..fixtures.application_fixtures import example_saas_configs

"""Simple test to verify that the available configs can be deserialized into SaaSConfigs"""
@pytest.mark.saas_connector
def test_saas_configs(example_saas_configs) -> None:
    for connector_name, saas_config in example_saas_configs.items():
        saas_config = SaaSConfig(**saas_config)

@pytest.mark.saas_connector
def test_saas_config_to_dataset(example_saas_configs: Dict[str, Dict]):
    # convert endpoint references to dataset references to be able to hook SaaS connectors into the graph traversal
    saas_config = SaaSConfig(**example_saas_configs["mailchimp"])
    mailchimp_dataset = saas_config.generate_dataset()

    messages_collection = mailchimp_dataset.collections[0]
    member_collection = mailchimp_dataset.collections[2]
    query_field = member_collection.fields[0]
    conversation_id_field = messages_collection.fields[0]
    conversations_reference = conversation_id_field.references[0]
    field_address, direction = conversations_reference

    assert messages_collection.name == "messages"
    assert conversation_id_field.name == "conversation_id"
    assert field_address == FieldAddress("mailchimp_connector", "conversations", "id")
    assert direction == "from"

    assert query_field.name == "query"
    assert query_field.identity == "email"