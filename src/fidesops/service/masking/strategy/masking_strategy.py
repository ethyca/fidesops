# MR Note - It would be nice to enforce this at compile time
from abc import abstractmethod, ABC
from typing import Optional, List

from fidesops.graph.data_type import DataType
from fidesops.schemas.masking.masking_configuration import MaskingConfiguration
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
)


class MaskingStrategy(ABC):
    """Abstract base class for masking strategies"""

    @abstractmethod
    def mask(self, value: Optional[str]) -> Optional[str]:
        """Used to mask the provided value"""
        pass

    @staticmethod
    @abstractmethod
    def get_configuration_model() -> MaskingConfiguration:
        """Used to get the configuration model to configure the strategy"""
        pass

    @staticmethod
    @abstractmethod
    def get_description() -> MaskingStrategyDescription:
        """Returns the description used for documentation. In particular, used by the
        documentation endpoint in masking_endpoints.list_masking_strategies"""
        pass

    @staticmethod
    @abstractmethod
    def get_supported_data_types() -> List[DataType]:
        """Returns the supported data types for the given strategy"""
        pass
        # fixme: add supported data types for each masking strategy
