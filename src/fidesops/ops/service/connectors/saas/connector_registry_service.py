from __future__ import annotations

from asyncio.log import logger
from os.path import exists
from typing import Any, Dict, List, Optional

from fideslib.core.config import load_toml
from pydantic import BaseModel, validator

from fidesops.schemas.dataset import FidesopsDataset
from fidesops.schemas.saas.saas_config import SaaSConfig
from fidesops.util.saas_util import load_config, load_dataset, load_yaml_as_string

_registry: ConnectorRegistry = {}


class ConnectorTemplate(BaseModel):
    """
    A collection of references to artifacts that make up
    a complete SaaS connector (SaaS config, dataset, etc.)
    """

    config: str
    dataset: str
    icon: str

    @validator("config")
    def validate_config(cls, config: str) -> str:
        """Validates the config at the given path"""
        SaaSConfig(**load_config(config))
        return config

    @validator("dataset")
    def validate_dataset(cls, dataset: str) -> str:
        """Validates the dataset at the given path"""
        FidesopsDataset(**load_dataset(dataset)[0])
        return dataset

    @validator("icon")
    def validate_icon(cls, icon: str) -> str:
        """Validates the icon at the given path"""
        if not exists(icon):
            raise ValueError(f"Icon file {icon} was not found")
        return icon


class ConnectorRegistry(BaseModel):
    """A map of SaaS connector templates"""

    __root__: Dict[str, ConnectorTemplate]

    def keys(self):
        return list(self.__root__)

    def get(self, item):
        try:
            return self.__root__[item]
        except:
            return None


def connector_types() -> List[str]:
    """List of registered SaaS connector types"""
    return _registry.keys()


def get_connector_template(connector_type: str) -> Optional[ConnectorTemplate]:
    """
    Returns an object containing the references to the various SaaS connector artifacts
    """
    return _registry.get(connector_type)


def instantiate_connector_template(
    connector_type: str, instance_key: str, secrets: Dict[str, Any]
) -> None:
    """Creates a SaaS connection config and associates the SaaS config and dataset with the new connection"""

    template = _registry.get(connector_type)
    # validate secrets
    # create connection config

    # add saas config
    saas_config = load_yaml_as_string(template.config).replace(
        "instance_fides_key", instance_key
    )
    logger.info(saas_config)

    # add dataset
    saas_dataset = load_yaml_as_string(template.dataset).replace(
        "instance_fides_key", instance_keyx
    )
    logger.info(saas_dataset)


def update_connector_instances() -> None:
    """
    Updates every SaaS connection config and dataset with the latest version
    defined in the SaaS connector registry
    """
    # get all saas connection configs
    # get version number from SaaS config (figure out versioning)
    # if registry version is newer
    # update saas config
    # update dataset
    pass


def load_registry(config_file: str) -> None:
    """Loads a SaaS connector registry from the given config file."""
    global _registry
    _registry = ConnectorRegistry.parse_obj(load_toml([config_file]))
