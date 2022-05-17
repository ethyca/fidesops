from typing import Dict, List, Union

from pydantic import ValidationError

from fidesops.common_exceptions import NoSuchStrategyException
from fidesops.common_exceptions import ValidationError as FidesopsValidationError
from fidesops.schemas.masking.masking_configuration import (
    FormatPreservationConfig,
    MaskingConfiguration,
)
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy


class MaskingStrategyFactory:
    @staticmethod
    def get_strategy(
        strategy_name: str,
        configuration: Dict[
            str,
            Union[str, FormatPreservationConfig],
        ],
    ) -> MaskingStrategy:
        strategy = next(
            (
                s
                for s in MaskingStrategyFactory.strategies()
                if s.strategy_name() == strategy_name
            ),
            None,
        )
        if strategy:
            try:
                strategy_config: MaskingConfiguration = (
                    strategy.get_configuration_model()(**configuration)
                )
                return strategy(configuration=strategy_config)
            except ValidationError as e:
                raise FidesopsValidationError(message=str(e))
        else:
            valid_strategies = ", ".join(
                [s.strategy_name() for s in MaskingStrategyFactory.strategies()]
            )
            raise NoSuchStrategyException(
                f"Strategy '{strategy_name}' does not exist. Valid strategies are [{valid_strategies}]"
            )

    @staticmethod
    def strategies() -> List[MaskingStrategy]:
        """Returns all supported masking strategies"""
        return MaskingStrategy.__subclasses__()
