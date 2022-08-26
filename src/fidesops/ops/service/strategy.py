import logging
from abc import ABC
from typing import Type

from fidesops.ops.schemas.saas.strategy_configuration import StrategyConfiguration

logger = logging.getLogger(__name__)


class Strategy(ABC):
    """Abstract base class for strategies"""

    name: str = None  # type: ignore
    configuration_model: Type[StrategyConfiguration] = None  # type: ignore

    def __init__(self, configuration: StrategyConfiguration):
        pass
