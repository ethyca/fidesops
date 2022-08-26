import pytest

from fidesops.ops.common_exceptions import NoSuchStrategyException
from fidesops.ops.schemas.saas.strategy_configuration import StrategyConfiguration
from fidesops.ops.service.strategy import Strategy
from fidesops.ops.service.strategy_factory import register, strategy


class TestStrategyFactory:
    """
    Unit tests for the ServiceFactory module functionality
    """

    def test_valid_strategy(self):
        """
        Test registering a valid Strategy
        """

        class SomeStrategyConfiguration(StrategyConfiguration):
            some_key: str = "default value"

        class SomeStrategy(Strategy):
            name = "some strategy"
            configuration_model = SomeStrategyConfiguration

            def __init__(self, configuration: SomeStrategyConfiguration):
                self.some_config = configuration.some_key
                super().__init__(configuration)

        class AnotherStrategy(Strategy):
            name = SomeStrategy.name
            configuration_model = SomeStrategyConfiguration

            def __init__(self, configuration: SomeStrategyConfiguration):
                self.some_config = configuration.some_key
                super().__init__(configuration)

        register(SomeStrategy)
        config = SomeStrategyConfiguration(some_key="non default value")
        retrieved_strategy = strategy(SomeStrategy.name, config.dict())
        assert isinstance(retrieved_strategy, SomeStrategy)
        assert retrieved_strategy.some_config == "non default value"

        # register another strategy type with same name
        # and ensure registry is properly updated
        register(AnotherStrategy)
        retrieved_strategy = strategy(SomeStrategy.name, config.dict())
        assert isinstance(retrieved_strategy, AnotherStrategy)
        assert retrieved_strategy.some_config == "non default value"

    def test_invalid_strategy(self):
        """
        Test registering an invalid Strategy throws expected errors
        """

        class SomeStrategyConfiguration(StrategyConfiguration):
            some_key: str = "default value"

        class SomeInvalidStrategy(Strategy):
            configuration_model = SomeStrategyConfiguration

        with pytest.raises(NotImplementedError) as exc:
            register(SomeInvalidStrategy)
        assert "'name'" in str(exc.value)

        class AnotherInvalidStrategy(Strategy):
            name = "some name"

        with pytest.raises(NotImplementedError) as exc:
            register(AnotherInvalidStrategy)
        assert "'configuration_model'" in str(exc.value)

    def test_retrieve_nonexistent_strategy(self):
        """
        Test attempt to retrieve a nonexistent strategy
        """
        with pytest.raises(NoSuchStrategyException) as exc:
            strategy("a nonexistent strategy", {})
        assert "'a nonexistent strategy'" in str(exc.value)
