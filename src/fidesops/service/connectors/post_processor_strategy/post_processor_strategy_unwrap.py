from typing import Dict, Any

from fidesops.schemas.saas.strategy_configuration import UnwrapPostProcessorConfiguration, StrategyConfiguration
from fidesops.service.connectors.post_processor_strategy.post_processory_strategy import PostProcessorStrategy


class UnwrapPostProcessorStrategy(PostProcessorStrategy):

    def __init__(self, configuration: UnwrapPostProcessorConfiguration):
        self.data_path = configuration.data_path

    def process(self, data, params):
        return data

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return UnwrapPostProcessorConfiguration
