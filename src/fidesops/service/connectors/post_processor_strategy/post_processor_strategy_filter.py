from typing import Any, Optional, Dict

from fidesops.common_exceptions import PostProcessingException
from fidesops.schemas.saas.strategy_configuration import FilterPostProcessorConfiguration, StrategyConfiguration, \
    IdentityParamRef
from fidesops.service.connectors.post_processor_strategy.post_processory_strategy import PostProcessorStrategy

STRATEGY_NAME = "filter"


class FilterPostProcessorStrategy(PostProcessorStrategy):
    """
    Filters object or array given field name and value.
    Value can be reference a dynamic identity passed in through the request OR hard-coded value.
    E.g.
    data = [
        {
            id: 1397429347
            email_contact: somebody@email.com
            name: Somebody Awesome
        },
        {
            id: 238475234
            email_contact: somebody-else@email.com
            name: Somebody Cool
        }
    ]
    field: email_contact
    value: {identity: email}, where email == somebody@email.com
    result = [{
        id: 1397429347
        email_contact: somebody@email.com
        name: Somebody Awesome
    }]
    """

    def __init__(self, configuration: FilterPostProcessorConfiguration):
        self.field = configuration.field
        self.value = configuration.value

    def get_strategy_name(self) -> str:
        return STRATEGY_NAME

    def process(self, data: Any, identity_data: Dict[str, Any] = None) -> Optional[Any]:
        """
        :param data: A list or an object. Preserves format of data.
        :param identity_data: Dict of cached identity data
        :return:
        """
        filter_value = identity_data[self.value.identity] if isinstance(self.value, IdentityParamRef) else self.value
        if isinstance(data, list):
            return [item for item in data if item[self.field] == filter_value]
        return data if data[self.field] == filter_value else None

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return FilterPostProcessorConfiguration
