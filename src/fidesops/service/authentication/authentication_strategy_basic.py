from requests import PreparedRequest

from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.schemas.saas.strategy_configuration import (
    BasicAuthenticationConfiguration,
)
from fidesops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fidesops.service.authentication.authentication_strategy_factory import register
from fidesops.util.saas_util import assign_placeholders


@register("basic", BasicAuthenticationConfiguration)
class BasicAuthenticationStrategy(AuthenticationStrategy):
    """
    Replaces the username and password placeholders with the actual credentials
    and uses them to add a basic authentication header to the incoming request.
    """

    def __init__(self, configuration: BasicAuthenticationConfiguration):
        self.username = configuration.username
        self.password = configuration.password

    def add_authentication(
        self, request: PreparedRequest, connection_config: ConnectionConfig
    ) -> PreparedRequest:
        """Add basic authentication to the request"""
        secrets = connection_config.secrets

        request.prepare_auth(
            auth=(
                assign_placeholders(self.username, secrets),  # type: ignore
                assign_placeholders(self.password, secrets),  # type: ignore
            )
        )
        return request
