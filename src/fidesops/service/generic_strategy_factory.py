import logging
from abc import ABC
from typing import Any, Callable, Dict, Generic, Type, TypeVar, ValuesView

from pydantic import ValidationError

from fidesops.common_exceptions import NoSuchStrategyException
from fidesops.common_exceptions import ValidationError as FidesopsValidationError
from fidesops.service.generic_strategy import GenericStrategy

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=GenericStrategy)


class GenericStrategyFactory(ABC, Generic[T]):
    def __init__(self) -> None:
        self.registry: Dict[str, Type[T]] = {}
        self.valid_strategies: str = ""

    def register(self, name: str) -> Callable[[Type[T]], Type[T]]:
        def wrapper(
            strategy_class: Type[T],
        ) -> Type[T]:
            logger.debug(
                f"Registering new strategy '{strategy_class}' under name '{name}'"
            )

            if name in self.registry:
                logger.warning(
                    f"Strategy with name '{name}' already exists. It previously referred to class '{self.registry[name]}', but will now refer to '{strategy_class}'"
                )

            self.registry[name] = strategy_class
            self.valid_strategies = ", ".join(self.registry.keys())
            return self.registry[name]

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
            strategy = self.registry[strategy_name]
        except KeyError:
            raise NoSuchStrategyException(
                f"Strategy '{strategy_name}' does not exist. Valid strategies are [{self.valid_strategies}]"
            )
        try:
            strategy_config = strategy.get_configuration_model()(**configuration)  # type: ignore
        except ValidationError as e:
            raise FidesopsValidationError(message=str(e))
        return strategy(configuration=strategy_config)  # type: ignore

    def get_strategies(self) -> ValuesView[T]:
        """Returns all supported strategies"""
        return self.registry.values()  # type: ignore
