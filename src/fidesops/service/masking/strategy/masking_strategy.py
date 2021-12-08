# MR Note - It would be nice to enforce this at compile time
from abc import abstractmethod, ABC
from typing import Optional, List

from fidesops.schemas.masking.masking_configuration import MaskingConfiguration
from fidesops.schemas.masking.masking_secrets import MaskingSecretGeneration
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
)


class MaskingStrategy(ABC):
    """Abstract base class for masking strategies"""

    @abstractmethod
    def mask(self, value: Optional[str], request_id: Optional[str]) -> Optional[str]:
        """Used to mask the provided value"""
        # fixme: how to handle when no request id provided? maybe generate secrets before calling mask
        pass

    def generate_secrets(self) -> List[MaskingSecretGeneration]:
        """Generates secrets for strategy"""
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
    def data_type_supported(data_type: Optional[str]) -> bool:
        """Returns the whether the data type is supported for the given strategy"""
        pass
