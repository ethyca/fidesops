from fidesops.util.collection_util import Row
import pydash
from typing import Any, Dict, Optional
from requests import Response
from fidesops.schemas.saas.shared_schemas import SaaSRequestParams
from fidesops.schemas.saas.strategy_configuration import (
    CursorPaginationConfiguration,
    StrategyConfiguration,
)
from fidesops.service.pagination.pagination_strategy import PaginationStrategy

STRATEGY_NAME = "cursor"


class CursorPaginationStrategy(PaginationStrategy):
    def __init__(self, configuration: CursorPaginationConfiguration):
        self.cursor_param = configuration.cursor_param
        self.value_field = configuration.value_field

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

        # read the new cursor value from row (post-processed response)
        cursor = pydash.get(row, self.value_field)

        # return None if the cursor value isn't found to stop further pagination
        if cursor is None:
            return None

        # deconstruct request_params and add or replace cursor_param
        # with new cursor value
        method, path, params, body = request_params
        params[self.cursor_param] = cursor

        return method, path, params, body

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return CursorPaginationConfiguration
