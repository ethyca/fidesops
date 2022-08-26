import logging
from typing import Any, Callable, Dict, Type, ValuesView

from pydantic import ValidationError

from fidesops.ops.common_exceptions import NoSuchStrategyException
from fidesops.ops.common_exceptions import ValidationError as FidesopsValidationError
from fidesops.ops.service.strategy import Strategy

logger = logging.getLogger(__name__)


class StrategyFactory:
    def __init__(self) -> None:
        self.registry: Dict[str, Type[Strategy]] = {}
        self.valid_strategies: str = ""

    def register(self) -> Callable[[Type[Strategy]], Type[Strategy]]:
        def wrapper(
            strategy_class: Type[Strategy],
        ) -> Type[Strategy]:

            _validate_strategy_class(strategy_class)

            name = strategy_class.name
            logger.debug(
                ("Registering new strategy '%s' under name '%s'", strategy_class, name)
            )

            if name in self.registry:
                logger.warning(
                    (
                        "Strategy with name '%s' already exists. It previously referred to class '%s', but will now refer to '%s'",
                        name,
                        self.registry[name],
                        strategy_class,
                    )
                )

            self.registry[name] = strategy_class
            self.valid_strategies = ", ".join(self.registry.keys())
            return self.registry[name]

        return wrapper

    def strategy(
        self,
        strategy_name: str,
        configuration: Dict[str, Any],
    ) -> Strategy:
        """
        Returns the strategy given the name and configuration.
        Raises NoSuchStrategyException if the strategy does not exist
        """
        try:
            strategy_class = self.registry[strategy_name]
        except KeyError:
            raise NoSuchStrategyException(
                f"Strategy '{strategy_name}' does not exist. Valid strategies are [{self.valid_strategies}]"
            )
        try:
            strategy_config = strategy_class.configuration_model(**configuration)
        except ValidationError as e:
            raise FidesopsValidationError(message=str(e))
        return strategy_class(strategy_config)

    def strategies(self) -> ValuesView[Type[Strategy]]:
        """Returns all supported strategies"""
        return self.registry.values()


def _validate_strategy_class(strategy_class: Type[Strategy]) -> None:
    """
    Ensure the strategy class being registered has the necessary class variables set
    """
    if not strategy_class.name:
        raise NotImplementedError(
            "A 'name' class variable is not defined for this Strategy subclass"
        )

    if not strategy_class.configuration_model:
        raise NotImplementedError(
            "A 'configuration_model' class variable is not defined for this Strategy subclass"
        )


strategy_factory = StrategyFactory()
register = strategy_factory.register()
strategy = strategy_factory.strategy
strategies = strategy_factory.strategies
