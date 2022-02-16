from typing import Dict, Any

from fidesops.schemas.saas.strategy_configuration import FilterPostProcessorConfiguration, StrategyConfiguration
from fidesops.service.connectors.post_processor_strategy.post_processory_strategy import PostProcessorStrategy


class FilterPostProcessorStrategy(PostProcessorStrategy):

    def __init__(self, configuration: FilterPostProcessorConfiguration):
        self.field = configuration.field
        self.value = configuration.value

    def process(self, data, params):
        return data

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return FilterPostProcessorConfiguration
