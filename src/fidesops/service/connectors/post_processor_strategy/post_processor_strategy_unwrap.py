from typing import Any, Optional, Dict

from fidesops.common_exceptions import FidesopsException
from fidesops.schemas.saas.strategy_configuration import UnwrapPostProcessorConfiguration, StrategyConfiguration
from fidesops.service.connectors.post_processor_strategy.post_processory_strategy import PostProcessorStrategy


STRATEGY_NAME = "unwrap"


class UnwrapPostProcessorStrategy(PostProcessorStrategy):
    """
    Given a path to an object/list, returns the object/list
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

    def get_strategy_name(self) -> str:
        return STRATEGY_NAME

    def process(self, data: Any, identity_data: Dict[str, Any] = None) -> Optional[Any]:
        """
        :param data: A list or an object. Preserves format of data.
        :param identity_data: Dict of cached identity data
        :return:
        """
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
