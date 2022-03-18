import pydash
from typing import Any, Dict, List, Literal, Optional, Union
from fidesops.service.pagination.pagination_strategy_factory import get_strategy
from pydantic import BaseModel, validator, root_validator
from fidesops.schemas.base_class import BaseSchema
from fidesops.schemas.dataset import FidesopsDatasetReference
from fidesops.graph.config import Collection, Dataset, FieldAddress, ScalarField
from fidesops.schemas.saas.strategy_configuration import ConnectorParamRef
from fidesops.schemas.shared_schemas import FidesOpsKey


class ConnectorParams(BaseModel):
    """
    Required information for the given SaaS connector.
    """

    name: str


class RequestParam(BaseModel):
    """
    A request parameter which includes the type (query or path) along with a default value or
    a reference to an identity value or a value in another dataset.
    """

    name: str
    type: Literal[
        "query", "path"
    ]  # used to determine location in the generated request
    identity: Optional[str]
    references: Optional[List[FidesopsDatasetReference]]
    default_value: Optional[Any]
    data_type: Optional[str]

    @validator("references")
    def check_reference_direction(
        cls, references: Optional[List[FidesopsDatasetReference]]
    ) -> Optional[List[FidesopsDatasetReference]]:
        """Validates the request_param only contains inbound references"""
        for reference in references or {}:
            if reference.direction == "to":
                raise ValueError(
                    "References can only have a direction of 'from', found 'to'"
                )
        return references

    @root_validator
    def check_exactly_one_value_field(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        value_fields = [
            bool(values.get("identity")),
            bool(values.get("references")),
            bool(
                values.get("default_value") is not None
            ),  # to prevent a value of 0 from returning False
        ]
        if sum(value_fields) != 1:
            raise ValueError(
                "Must have exactly one of 'identity', 'references', or 'default_value'"
            )
        return values


class Strategy(BaseModel):
    """General shape for swappable strategies (ex: auth, processors, pagination, etc.)"""

    strategy: str
    configuration: Dict[str, Any]


class SaaSRequest(BaseModel):
    """
    A single request with a static or dynamic path, and the request params needed to build the request.
    Also includes optional strategies for postprocessing and pagination.
    """

    path: str
    request_params: Optional[List[RequestParam]]
    data_path: Optional[str]
    postprocessors: Optional[List[Strategy]]
    pagination: Optional[Strategy]
    grouped_inputs: Optional[List[str]] = []

    @root_validator(pre=True)
    def validate_request_for_pagination(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calls the appropriate validation logic for the request based on
        the specified pagination strategy. Passes in the raw value dict
        before any field validation.
        """
        pagination = values.get("pagination")
        if pagination is not None:
            pagination_strategy = get_strategy(
                pagination.get("strategy"), pagination.get("configuration")
            )
            pagination_strategy.validate_request(values)
        return values

    @root_validator
    def validate_grouped_inputs(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that grouped_inputs must reference fields from the same collection"""
        grouped_inputs = values.get("grouped_inputs")

        if grouped_inputs:
            request_params = values.get("request_params", [])
            names = [param.name for param in request_params]

            if not all(field in names for field in grouped_inputs):
                raise ValueError(
                    "Grouped_input fields must also be declared as request_params."
                )

            referenced_collections: List[str] = []
            for param in request_params:
                if param.name in grouped_inputs:
                    if not param.references:
                        raise ValueError(
                            "Grouped input fields must be on incoming references."
                        )
                    collect = param.references[0].field.split(".")[0]
                    referenced_collections.append(collect)
            if not all(x == referenced_collections[0] for x in referenced_collections):
                raise ValueError(
                    "Grouped input fields must all reference the same collection."
                )

        return values


class Endpoint(BaseModel):
    """An collection of read/update/delete requests which corresponds to a FidesopsDataset collection (by name)"""

    name: str
    requests: Dict[Literal["read", "update", "delete"], SaaSRequest]


class ConnectorParam(BaseModel):
    """Used to define the required parameters for the connector (user-provided and constants)"""

    name: str
    default_value: Optional[Any]


class ClientConfig(BaseModel):
    """Definition for an authenticated base HTTP client"""

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
    test_request: SaaSRequest

    @property
    def top_level_endpoint_dict(self) -> Dict[str, Endpoint]:
        """Returns a map of endpoint names mapped to Endpoints"""
        return {endpoint.name: endpoint for endpoint in self.endpoints}

    def get_graph(self) -> Dataset:
        """Converts endpoints to a Dataset with collections and field references"""
        collections = []
        for endpoint in self.endpoints:
            fields = []
            for param in endpoint.requests["read"].request_params or []:
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
                if endpoint.requests.get("read"):
                    grouped_inputs = endpoint.requests["read"].grouped_inputs
                collections.append(
                    Collection(
                        name=endpoint.name,
                        fields=fields,
                        grouped_inputs=grouped_inputs,
                    )
                )

        return Dataset(
            name=self.name,
            collections=collections,
            connection_key=self.fides_key,
        )


class SaaSConfigValidationDetails(BaseSchema):
    """
    Message with any validation issues with the SaaS config
    """

    msg: Optional[str]


class ValidateSaaSConfigResponse(BaseSchema):
    """
    Response model for validating a SaaS config, which includes both the SaaS config
    itself (if valid) plus a details object describing any validation errors.
    """

    saas_config: SaaSConfig
    validation_details: SaaSConfigValidationDetails
