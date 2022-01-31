from typing import Dict, Any

import yaml

from fidesops.graph.config import SaaSConfig


def test_mailchimp_config_yaml(example_saas_configs: Dict[str, Dict]):
    saas_config = SaaSConfig(**example_saas_configs["mailchimp"])
    configuration = saas_config.client_config.authentication.configuration
    print(configuration)
    username_key = configuration["username"].connector_param
    password_key = configuration["password"].connector_param
    assert username_key == "username"
    assert password_key == "api_key"

def test_stripe_config_yaml(example_saas_configs: Dict[str, Dict]):
    saas_config = SaaSConfig(**example_saas_configs["stripe"])
    configuration = saas_config.client_config.authentication.configuration
    print(configuration)
    token_key = configuration["token"].connector_param
    assert token_key == "api_key"
