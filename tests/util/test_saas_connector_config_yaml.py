from typing import Dict, Any

import yaml

from fidesops.graph.config import SaasConnectorConfig

example_saas_connector_config_yaml = """saas_connector_config:
  - fides_key: mailchimp_connector
    name: Mailchimp Connector
    description: A sample schema representing the Mailchimp connector for Fidesops
    version: 1.0

    connector_params:
    - name: domain
      is_secret: false
    - name: api_key
      is_secret: true
    test_connection:
      path: /3.0/lists
    
    endpoints:
      - name: messages
        request_params:
          read:
            path: /3.0/conversations/{conversation_id}/messages
            parameters:
              - name: conversation_id
                type: path
                references:
                - dataset: mailchimp_dataset
                  field: conversations.id
                  direction: from
      - name: conversations
        request_params:
          read:
            path: /3.0/conversations
            parameters:
              - name: count
                type: query
                default_value: 1000
              - name: offset
                type: query
        pagination:
          strategy: basic_pagination
          configuration:
            incremental_param: offset
            increment_by: 1000
            initial_value: 0
      - name: member
        request_params:
          read:
            path: /3.0/search-members
            parameters:
              - name: query
                type: query
                identity: email
                data_type: string
          delete:
            path: /3.0/lists/{list_id}/members/{subscriber_hash}/actions/delete-permanent
            parameters:
              - name: list_id
                type: path
                references:
                  - dataset: mailchimp_dataset
                    field: member.list_id
                    direction: from
              - name: subscriber_hash
                type: path
                references:
                  - dataset: mailchimp_dataset
                    field: member.id
                    direction: from
"""


def __to_saas_connector_config__(yamlstr: str) -> Dict[str, Any]:
    return yaml.safe_load(yamlstr).get("saas_connector_config")[0]


def test_saas_connector_config_yaml():
    saas_connector_config = __to_saas_connector_config__(
        example_saas_connector_config_yaml
    )
    config = SaasConnectorConfig.parse_obj(saas_connector_config)
    assert config.test_connection.path == "/3.0/lists"
