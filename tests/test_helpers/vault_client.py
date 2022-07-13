import logging
import os

from hvac import Client

from fidesops.common_exceptions import FidesopsException

logger = logging.getLogger(__name__)

params = {
    "VAULT_ADDR": os.environ.get("VAULT_ADDR"),
    "VAULT_NAMESPACE": os.environ.get("VAULT_NAMESPACE"),
    "VAULT_TOKEN": os.environ.get("VAULT_TOKEN"),
}
_environment = os.environ.get("VAULT_ENVIRONMENT", "development")

if not all(params.values()):
    raise FidesopsException(
        "Missing environment variables "
        f"{', '.join([key for key, value in params.items() if not value])}"
        " for Vault client"
    )

try:
    _client = Client(
        url=params["VAULT_ADDR"],
        namespace=params["VAULT_NAMESPACE"],
        token=params["VAULT_TOKEN"],
    )
except Exception as exc:
    raise FidesopsException(f"Unable to create Vault client: {str(exc)}")


def get_secrets(connector: str):
    """Returns a map of secrets for the given connector."""
    secrets = _client.secrets.kv.v2.read_secret_version(
        mount_point=_environment, path=connector
    )
    secrets_map = secrets["data"]["data"]
    logger.info(f'Loading secrets for {connector}: {", ".join(secrets_map.keys())}')
    return secrets_map
