from typing import Any, Dict, Optional
from requests import Response
from fidesops.common_exceptions import FidesopsException
from fidesops.schemas.saas.strategy_configuration import (
    ConnectorParamRef,
    OffsetPaginationConfiguration,
    StrategyConfiguration,
)
from fidesops.schemas.saas.shared_schemas import SaaSRequestParams
from fidesops.service.pagination.pagination_strategy import PaginationStrategy
from fidesops.util.collection_util import Row

STRATEGY_NAME = "offset"


class OffsetPaginationStrategy(PaginationStrategy):
    def __init__(self, configuration: OffsetPaginationConfiguration):
        self.incremental_param = configuration.incremental_param
        self.increment_by = configuration.increment_by
        self.page_limit = configuration.page_limit

    def get_strategy_name(self) -> str:
        return STRATEGY_NAME

    def get_next_request(
        self,
        request_params: SaaSRequestParams,
        connector_params: Dict[str, Any],
        response: Response,
        row: Optional[Row],
    ) -> Optional[SaaSRequestParams]:
        """Build request for next page of data"""

        # find query param value from deconstructed request_params, throw exception if query param not found
        method, path, params, body = request_params
        param_value = params.get(self.incremental_param)
        if param_value is None:
            raise FidesopsException(
                f"Unable to find query param named '{self.incremental_param}' in request"
            )

        # increment param value and return None if page_limit has been reached to indicate there are no more pages
        page_limit = self.page_limit
        if isinstance(self.page_limit, ConnectorParamRef):
            page_limit = connector_params.get(self.page_limit.connector_param)
            if page_limit is None:
                raise FidesopsException(
                    f"Unable to find value for 'page_limit' with the connector_param reference '{self.page_limit.connector_param}'"
                )
        param_value += self.increment_by
        if param_value > page_limit:
            return None

        # update query param and return updated request_param tuple
        params[self.incremental_param] = param_value
        return method, path, params, body

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return OffsetPaginationConfiguration

    def validate_request(self, request: Dict[str, Any]) -> None:
        """Ensures that the query param specified by 'incremental_param' exists in the request"""
        request_params = (
            request_param
            for request_param in request.get("request_params", [])
            if request_param.get("name") == self.incremental_param
            and request_param.get("type") == "query"
        )
        request_param = next(request_params, None)
        if request_param is None:
            raise ValueError(f"Query param '{self.incremental_param}' not found.")
