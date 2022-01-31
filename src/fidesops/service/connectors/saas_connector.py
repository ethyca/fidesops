import logging
from typing import Any, Dict, List, Optional
from requests import Session, Request, PreparedRequest, Response

from fidesops.service.connectors.base_connector import BaseConnector
from fidesops.graph.traversal import Row, TraversalNode
from fidesops.models.connectionconfig import ConnectionTestStatus
from fidesops.models.policy import Policy
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.service.connectors.query_config import QueryConfig
from fidesops.common_exceptions import ConnectionException
from fidesops.models.saasconnectionconfig import SaaSConnectionConfig
from fidesops.graph.config import SaaSConfig
from fidesops.graph.config import ClientConfig

logger = logging.getLogger(__name__)


class AuthenticatedClient:
    def __init__(self, secrets: Dict, client_config: ClientConfig):
        self.s = Session()
        self.secrets = secrets
        self.client_config = client_config

    def addAuthentication(
        self, req: PreparedRequest, strategy_name: str
    ) -> PreparedRequest:
        # TODO: keeping this simple for now since we only have two auth methods
        configuration = self.client_config.authentication.configuration
        if strategy_name == "basic_authentication":
            username_key = configuration["username"].connector_param
            password_key = configuration["password"].connector_param
            req.prepare_auth(
                auth=(self.secrets[username_key], self.secrets[password_key])
            )
        elif strategy_name == "bearer_authentication":
            token_key = configuration["token"].connector_param
            req.headers["Authorization"] = "Bearer " + self.secrets[token_key]
        return req

    def getBaseRequest(self, path: str) -> PreparedRequest:
        host_key = self.client_config.host.connector_param
        req = Request(
            url=f"{self.client_config.protocol}://{self.secrets[host_key]}{path}"
        ).prepare()
        return self.addAuthentication(
            req, self.client_config.authentication.strategy_name
        )

    def get(self, path: str) -> Response:
        req= self.getBaseRequest(path=path)
        req.method = "GET"
        return self.s.send(req)


class SaaSConnector(BaseConnector[None]):
    def __init__(self, configuration: SaaSConnectionConfig):
        self.name = configuration.name
        self.secrets = configuration.secrets
        self.saas_config = SaaSConfig(**configuration.saas_config)
        self.http_client = None

    def query_config(self, node: TraversalNode) -> QueryConfig[Any]:
        """Not required for this type"""

    def test_connection(self) -> Optional[ConnectionTestStatus]:
        try:
            test_connection_path = self.saas_config.test_connection.path
            response = self.client().get(path=test_connection_path)
            print(response.json())
        except Exception:
            raise ConnectionException(f"Connection Error connecting to {self.name}")

        print(f"Successfully connected to {self.name}")
        return ConnectionTestStatus.succeeded

    def create_client(self) -> AuthenticatedClient:
        return AuthenticatedClient(self.secrets, self.saas_config.client_config)

    def client(self) -> AuthenticatedClient:
        if not self.http_client:
            self.http_client = self.create_client()
        return self.http_client

    def retrieve_data(
        self, node: TraversalNode, policy: Policy, input_data: Dict[str, List[Any]]
    ) -> List[Row]:
        """Retrieve data in a connector dependent way based on input data.

        The input data is expected to include a key and list of values for
        each input key that may be queried on."""

    def mask_data(
        self,
        node: TraversalNode,
        policy: Policy,
        request: PrivacyRequest,
        rows: List[Row],
    ) -> int:
        """Execute a masking request. Return the number of rows that have been updated"""

    def close(self) -> None:
        """Not required for this type"""
