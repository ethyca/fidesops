import logging
from typing import Any, Dict, List, Union

import pydash

from fidesops.common_exceptions import FidesopsException
from fidesops.schemas.saas.shared_schemas import IdentityParamRef
from fidesops.schemas.saas.strategy_configuration import (
    FilterPostProcessorConfiguration,
    StrategyConfiguration,
)
from fidesops.service.processors.post_processor_strategy.post_processor_strategy import (
    PostProcessorStrategy,
)

STRATEGY_NAME = "filter"

logger = logging.getLogger(__name__)


class FilterPostProcessorStrategy(PostProcessorStrategy):
    """
    Filters object or array given field name and value
    Value can be reference a dynamic identity passed in through the request OR hard-coded value.
    E.g.
    data = [
        {
            "id": 1397429347
            "email_contact": somebody@email.com
            "name": Somebody Awesome
        },
        {
            "id": 238475234
            "email_contact": somebody-else@email.com
            "name": Somebody Cool
        }
    ]
    field: email_contact
    value: {"identity": email}, where email == somebody@email.com
    result = {
        id: 1397429347
        email_contact: somebody@email.com
        name: Somebody Awesome
    }
    """

    def __init__(self, configuration: FilterPostProcessorConfiguration):
        self.field = configuration.field
        self.value = configuration.value
        self.exact = configuration.exact
        self.case_sensitive = configuration.case_sensitive

    def get_strategy_name(self) -> str:
        return STRATEGY_NAME

    def process(
        self,
        data: Union[List[Dict[str, Any]], Dict[str, Any]],
        identity_data: Dict[str, Any] = None,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        - data: A list or a dict
        - identity_data: A dict of cached identity data

        returns a filtered dict, list of dicts, or empty list
        """

        if not data:
            return []

        # find value to filter by
        filter_value = self.value
        if isinstance(self.value, IdentityParamRef):
            if identity_data is None or identity_data.get(self.value.identity) is None:
                logger.warning(
                    f"Could not retrieve identity reference '{self.value.identity}' "
                    "due to missing identity data for the following post processing "
                    f"strategy: {self.get_strategy_name()}"
                )
                return []
            filter_value = identity_data.get(self.value.identity)

        try:
            if isinstance(data, list):
                return [
                    item
                    for item in data
                    if self._matches(
                        self.exact,
                        self.case_sensitive,
                        filter_value,
                        pydash.get(item, self.field),
                    )
                ]
            return (
                data
                if self._matches(
                    self.exact,
                    self.case_sensitive,
                    filter_value,
                    pydash.get(data, self.field),
                )
                else []
            )
        except KeyError:
            logger.warning(
                f"{self.field} could not be found on data for the following post processing strategy: {self.get_strategy_name()}"
            )
            return []

    def _matches(
        self,
        exact: bool,
        case_sensitive: bool,
        filter_value: str,
        target: Union[str, List[str]],
    ) -> bool:
        """
        Returns a boolean indicating if the filter_value (string) is contained
        in the target (string or list of strings).

        - exact: filter_value and target must be the same length (no extra characters)
        - case_sensitive: cases must match between filter_value and target
        """

        # validate inputs
        if not isinstance(target, (str, list)):
            raise FidesopsException(
                f"Field value '{self.field}' for filter postprocessor must be a string or list of strings, found '{type(target).__name__}'"
            )

        # validate list contents
        if isinstance(target, list):
            if not all(isinstance(item, str) for item in target):
                raise FidesopsException(
                    f"Every value in the '{self.field}' list must be a string"
                )

        # prep inputs by converting them to lowercase
        if not case_sensitive:
            filter_value = filter_value.casefold()
            if isinstance(target, list):
                target = [item.casefold() for item in target]
            elif isinstance(target, str):
                target = target.casefold()

        # compare filter_values to a target list
        if isinstance(target, list):
            return any(
                filter_value == item if exact else filter_value in item
                for item in target
            )

        # base case, compare filter_value to a single string
        return filter_value == target if exact else filter_value in target

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return FilterPostProcessorConfiguration
