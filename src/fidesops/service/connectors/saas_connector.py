import logging
from typing import Any, Dict, List, Optional, TypeVar
from requests import Session, Request, PreparedRequest, Response

from fidesops.service.connectors.base_connector import BaseConnector
from fidesops.graph.traversal import Row, TraversalNode
from fidesops.models.connectionconfig import ConnectionTestStatus
from fidesops.models.policy import Policy
from fidesops.models.privacy_request import PrivacyRequest
from fidesops.common_exceptions import ConnectionException
from fidesops.models.saasconfig import SaaSConfig
from fidesops.models.saasconnectionconfig import SaaSConnectionConfig
from fidesops.models.saasconfig import ClientConfig

from fidesops.service.connectors.query_config import SaaSQueryConfig

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
            username_key = configuration["username"]["connector_param"]
            password_key = configuration["password"]["connector_param"]
            req.prepare_auth(
                auth=(self.secrets[username_key], self.secrets[password_key])
            )
        elif strategy_name == "bearer_authentication":
            token_key = configuration["token"]["connector_param"]
            req.headers["Authorization"] = "Bearer " + self.secrets[token_key]
        return req

    def getBaseRequest(self, path: str, params: Dict, data: Dict) -> PreparedRequest:
        host_key = self.client_config.host.connector_param
        req = Request(
            url=f"{self.client_config.protocol}://{self.secrets[host_key]}{path}",
            params=params,
            data=data,
        ).prepare()
        return self.addAuthentication(
            req, self.client_config.authentication.strategy_name
        )

    def get(self, path: str, params: Dict, data: Dict) -> Response:
        req = self.getBaseRequest(path=path, params=params, data=data)
        req.method = "GET"
        return self.s.send(req)


class SaaSConnector(BaseConnector[None]):
    def __init__(self, configuration: SaaSConnectionConfig):
        self.name = configuration.name
        self.secrets = configuration.secrets
        self.saas_config = SaaSConfig(**configuration.saas_config)
        self.endpoints = self.saas_config.top_level_endpoint_dict
        self.http_client = None

    def query_config(self, node: TraversalNode) -> SaaSQueryConfig:
        return SaaSQueryConfig(node)

    def test_connection(self) -> Optional[ConnectionTestStatus]:
        try:
            test_request_path = self.saas_config.test_request.path
            response = self.client().get(path=test_request_path, params={}, data={})
            print(response.json())
        except Exception:
            raise ConnectionException(f"Connection Error connecting to {self.name}")

        logger.info(f"Successfully connected to {self.name}")
        return ConnectionTestStatus.succeeded

    def create_client(self) -> AuthenticatedClient:
        return AuthenticatedClient(self.secrets, self.saas_config.client_config)

    def client(self) -> AuthenticatedClient:
        if not self.http_client:
            self.http_client = self.create_client()
        return self.http_client

    def populate_parameters(self, request: Request, param_values: Dict[str, Any]):
        path = request.path
        params = {}
        data = {}

        for param in request.request_params:
            if param.type == "query":
                if param.default_value:
                    params[param.name] = param.default_value
                elif param.references or param.identity:
                    # TODO: update for scenario with multiple references
                    params[param.name] = param_values[param.name][0]
            if param.type == "path":
                path = path.replace(f"<{param.name}>", param_values[param.name][0])

        return (path, params, data)

    def get_value_by_path(self, dict: Dict, path: str):
        value = dict
        for key in path.split("/"):
            value = value[key]
        return value

    def retrieve_data(
        self, node: TraversalNode, policy: Policy, input_data: Dict[str, List[Any]]
    ) -> List[Row]:
        # filter data using base methods
        query_config = self.query_config(node)
        filtered_data = query_config.typed_filtered_values(input_data)

        # get the request information for the given collection
        collection_name = node.address.collection
        read_request = self.endpoints[collection_name].requests["read"]

        processed_responses = []
        for key, values in filtered_data.items():
            for value in values:
                # generate path, query params, and body data based on request description and filtered data
                (path, params, data) = self.populate_parameters(
                    read_request, {key: [value]}
                )

                # make request
                response = self.client().get(path=path, params=params, data=data)

                # process response
                if read_request.data_path:
                    processed_response = self.get_value_by_path(
                        response.json(), read_request.data_path
                    )
                else:
                    # by default, we expect the collection_name to be one of the root fields in the response
                    processed_response = response.json()[collection_name]

                processed_responses.extend(processed_response)
        return processed_responses

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
