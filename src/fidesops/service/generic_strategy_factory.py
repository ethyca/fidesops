import logging
from abc import ABC
from typing import Any, Callable, Dict, Generic, List, Tuple, Type, TypeVar

from pydantic import ValidationError

from fidesops.common_exceptions import NoSuchStrategyException
from fidesops.common_exceptions import ValidationError as FidesopsValidationError
from fidesops.schemas.saas.strategy_configuration import StrategyConfiguration

logger = logging.getLogger(__name__)

T = TypeVar("T")


class GenericStrategyFactory(ABC, Generic[T]):
    def __init__(self) -> None:
        self.registry: Dict[str, Tuple[Type[T], Type[StrategyConfiguration]]] = {}
        self.valid_strategies: str = ""

    def register(
        self, name: str, configuration_model: Type[StrategyConfiguration]
    ) -> Callable[[Type[T]], Type[T]]:
        def wrapper(
            strategy_class: Type[T],
        ) -> Type[T]:
            logger.debug(
                f"Registering new strategy '{strategy_class}' under name '{name}'"
            )

            if name in self.registry:
                logger.warning(
                    f"Strategy with name '{name}' already exists. It previously referred to class '{self.registry[name][0]}', but will now refer to '{strategy_class}'"
                )

            self.registry[name] = (strategy_class, configuration_model)
            self.valid_strategies = ", ".join(self.registry.keys())
            return self.registry[name][0]

        return wrapper

    def get_strategy(
        self,
        strategy_name: str,
        configuration: Dict[str, Any],
    ) -> T:
        """
        Returns the strategy given the name and configuration.
        Raises NoSuchStrategyException if the strategy does not exist
        """
        try:
            (strategy, configuration_model) = self.registry[strategy_name]
        except KeyError:
            raise NoSuchStrategyException(
                f"Strategy '{strategy_name}' does not exist. Valid strategies are [{self.valid_strategies}]"
            )
        try:
            strategy_config = configuration_model(**configuration)
        except ValidationError as e:
            raise FidesopsValidationError(message=str(e))
        return strategy(strategy_config)  # type: ignore

    def get_strategies(self) -> List[Type[T]]:
        """Returns all supported strategies"""
        return [val[0] for val in self.registry.values()]
