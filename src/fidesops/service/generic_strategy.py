from abc import ABC, abstractmethod

from fidesops.schemas.saas.strategy_configuration import StrategyConfiguration


class GenericStrategy(ABC):
    """Abstract base class for strategies"""

    @abstractmethod
    def __init__(self, config: StrategyConfiguration):
        pass

    @staticmethod
    @abstractmethod
    def get_configuration_model() -> StrategyConfiguration:
        """Used to get the configuration model to configure the strategy"""
