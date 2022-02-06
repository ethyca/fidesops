from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel
from fidesops.graph.config import Collection, FieldAddress, ScalarField

from fidesops.graph.traversal import Dataset
from fidesops.schemas.dataset import FidesopsDatasetReference
from fidesops.schemas.shared_schemas import FidesOpsKey


class ConnectorParams(BaseModel):
    name: str
    default_value: str
    from_user: bool
    is_secret: bool


class RequestParam(BaseModel):
    name: str
    type: Literal[
        "query", "path", "body"
    ]  # used to determine location in the generated request
    default_value: Optional[Any]
    identity: Optional[str]
    data_type: Optional[str]
    references: Optional[List[FidesopsDatasetReference]]


class Strategy(BaseModel):
    """General shape for swappable strategies (ex: auth, pagination, postprocessing, etc.)"""

    strategy_name: str
    configuration: Dict[str, Any]


class Request(BaseModel):
    path: str
    request_params: Optional[List[RequestParam]]
    data_path: Optional[str]  # defaults to collection name if not specified
    preprocessor: Optional[Strategy]
    postprocessor: Optional[Strategy]
    pagination: Optional[Strategy]


class Endpoint(BaseModel):
    """The name is the corresponding collection name in the associated Dataset"""

    name: str
    requests: Dict[Literal["read", "update", "delete"], Request]


class ConnectorParam(BaseModel):
    """Used to define the required parameters for the connector (user-provided and constants)"""

    name: str
    default_value: Optional[Any]
    from_user: bool
    is_secret: bool


class ConnectorParamRef(BaseModel):
    connector_param: str


class ClientConfig(BaseModel):
    """Definition for base HTTP client"""

    protocol: str
    host: Union[
        str, ConnectorParamRef
    ]  # can be defined inline or be a connector_param reference
    authentication: Strategy


class SaaSConfig(BaseModel):
    """
    Used to store endpoint and param configurations for a SaaS connector.
    This is done to separate the details of how to make the API calls
    from the data provided by a given API collection.

    The required fields for the config are converted into a Dataset which is
    merged with the standard Fidesops Dataset to provide a complete set of dependencies
    for the graph traversal
    """

    fides_key: FidesOpsKey
    name: str
    description: str
    version: str
    connector_params: List[ConnectorParam]
    client_config: ClientConfig
    endpoints: List[Endpoint]
    test_request: Request

    @property
    def top_level_endpoint_dict(self) -> Dict[str, Endpoint]:
        """Returns a map of endpoint names mapped to Endpoints"""
        return {endpoint.name: endpoint for endpoint in self.endpoints}

    def generate_dataset(self) -> Dataset:
        """Converts endpoints to a Dataset with collections and field references"""
        collections = []
        for endpoint in self.endpoints:
            fields = []
            # TODO parametrize this method to account for update and delete
            for param in endpoint.requests["read"].request_params:
                if param.references:
                    references = []
                    for reference in param.references:
                        first, *rest = reference.field.split(".")
                        references.append(
                            (
                                FieldAddress(reference.dataset, first, *rest),
                                reference.direction,
                            )
                        )
                    fields.append(ScalarField(name=param.name, references=references))
                if param.identity:
                    fields.append(ScalarField(name=param.name, identity=param.identity))
            if fields:
                collections.append(Collection(name=endpoint.name, fields=fields))
        return Dataset(
            name=self.name,
            collections=collections,
            connection_key=self.fides_key,
        )
