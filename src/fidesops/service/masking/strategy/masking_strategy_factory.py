import logging
from enum import Enum
from typing import Callable, Dict, List, Union

from pydantic import ValidationError

from fidesops.common_exceptions import NoSuchStrategyException
from fidesops.common_exceptions import ValidationError as FidesopsValidationError
from fidesops.schemas.masking.masking_configuration import (
    FormatPreservationConfig,
    MaskingConfiguration,
)
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy

logger = logging.getLogger(__name__)

class MaskingStrategyFactory:
    registry: Dict[str, MaskingStrategy] = {}
    valid_strategies = ""

    @classmethod
    def register(cls, name:str) -> Callable[[MaskingStrategy], MaskingStrategy]:
        def wrapper(strategy_class: MaskingStrategy) -> MaskingStrategy:
            if name in cls.registry:
                logger.warning(f"Strategy with name {name} already exists in MaskingStrategy registry. It referred to class {cls.registry[name]}, but will now refer to {strategy_class}")
            logger.info(f"Registering MaskingStrategy class {strategy_class} under name {name}")
            cls.registry[name] = strategy_class
            cls.valid_strategies = ", ".join(cls.registry.keys())
            return strategy_class
        return wrapper

    @classmethod
    def get_strategy(
        cls,
        strategy_name: str,
        configuration: Dict[
            str,
            Union[str, FormatPreservationConfig],
        ],
    ) -> MaskingStrategy:
        """
        Returns the strategy given the name and configuration.
        Raises NoSuchStrategyException if the strategy does not exist
        """
        if strategy_name not in cls.registry:
            raise NoSuchStrategyException(
                f"Strategy '{strategy_name}' does not exist. Valid strategies are [{cls.valid_strategies}]"
            )
        strategy: MaskingStrategy = cls.registry[strategy_name]
        try:
            strategy_config: MaskingConfiguration = strategy.get_configuration_model()(
                **configuration
            )
            return strategy(configuration=strategy_config)
        except ValidationError as e:
            raise FidesopsValidationError(message=str(e))

    @classmethod
    def get_strategies(cls) -> List[MaskingStrategy]:
        """Returns all supported masking strategies"""
        
        return cls.registry.values()
