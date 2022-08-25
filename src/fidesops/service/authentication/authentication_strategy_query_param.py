from requests import PreparedRequest

from fidesops.models.connectionconfig import ConnectionConfig
from fidesops.schemas.saas.strategy_configuration import (
    QueryParamAuthenticationConfiguration,
)
from fidesops.service.authentication.authentication_strategy import (
    AuthenticationStrategy,
)
from fidesops.service.strategy_factory import register
from fidesops.util.saas_util import assign_placeholders
from fidesops.util.url_util import set_query_parameter


@register
class QueryParamAuthenticationStrategy(AuthenticationStrategy):
    """
    Replaces the value placeholder with the actual credentials
    and adds it as a query param to the incoming request.
    """

    name = "query_param"
    configuration_model = QueryParamAuthenticationConfiguration

    def __init__(self, configuration: QueryParamAuthenticationConfiguration):
        self.name = configuration.name
        self.value = configuration.value
        super().__init__(configuration)

    def add_authentication(
        self, request: PreparedRequest, connection_config: ConnectionConfig
    ) -> PreparedRequest:
        """Add token to the request as a query param"""
        request.url = set_query_parameter(
            request.url,  # type: ignore
            self.name,
            assign_placeholders(self.value, connection_config.secrets),  # type: ignore
        )
        return request
