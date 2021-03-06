from typing import List, Optional

from fidesops.schemas.masking.masking_configuration import (
    MaskingConfiguration,
    NullMaskingConfiguration,
)
from fidesops.schemas.masking.masking_strategy_description import (
    MaskingStrategyDescription,
)
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy
from fidesops.service.masking.strategy.masking_strategy_factory import (
    MaskingStrategyFactory,
)

NULL_REWRITE_STRATEGY_NAME = "null_rewrite"


@MaskingStrategyFactory.register(NULL_REWRITE_STRATEGY_NAME)
class NullMaskingStrategy(MaskingStrategy):
    """Masks provided values each with a null value."""

    def __init__(
        self,
        configuration: NullMaskingConfiguration,
    ):
        """For parity with other MaskingStrategies, but for NullMaskingStrategy, nothing is pulled from the config"""

    def mask(
        self, values: Optional[List[str]], request_id: Optional[str]
    ) -> Optional[List[None]]:
        """Replaces the value with a null value"""
        if values is None:
            return None
        masked_values: List[None] = []
        for _ in range(len(values)):
            masked_values.append(None)
        return masked_values

    def secrets_required(self) -> bool:
        return False

    @staticmethod
    def get_configuration_model() -> MaskingConfiguration:
        return NullMaskingConfiguration  # type: ignore

    @staticmethod
    def get_description() -> MaskingStrategyDescription:
        return MaskingStrategyDescription(
            name=NULL_REWRITE_STRATEGY_NAME,
            description="Masks the input value with a null value",
            configurations=[],
        )

    @staticmethod
    def data_type_supported(data_type: Optional[str]) -> bool:
        """Determines whether or not the given data type is supported by this masking strategy"""
        return True
