from typing import Any, Optional

from fidesops.common_exceptions import FidesopsException
from fidesops.schemas.saas.strategy_configuration import UnwrapPostProcessorConfiguration, StrategyConfiguration
from fidesops.service.connectors.post_processor_strategy.post_processory_strategy import PostProcessorStrategy


class UnwrapPostProcessorStrategy(PostProcessorStrategy):
    """
    Given a path to an object/array, returns the object/array
    E.g.
    data = {
        exact_matches: {
            members: [
                howdy: 123,
                meow: 841
            ]
        }
    }
    data_path = exact_matches.members
    result = [
                howdy: 123,
                meow: 841
            ]
    """

    def __init__(self, configuration: UnwrapPostProcessorConfiguration):
        self.data_path = configuration.data_path

    def process(self, data) -> Optional[Any]:
        path_items = self.data_path.split(".")
        unwrapped = data
        for item in path_items:
            try:
                unwrapped = unwrapped[item]
            except Exception:
                raise FidesopsException(
                    f"'{item}' could not be found on {unwrapped}"
                )
        return unwrapped

    @staticmethod
    def get_configuration_model() -> StrategyConfiguration:
        return UnwrapPostProcessorConfiguration
