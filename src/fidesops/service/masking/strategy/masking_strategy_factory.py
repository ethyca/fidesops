import logging

from fidesops.service.generic_strategy_factory import GenericStrategyFactory
from fidesops.service.masking.strategy.masking_strategy import MaskingStrategy

logger = logging.getLogger(__name__)


class MaskingStrategyFactory(GenericStrategyFactory[MaskingStrategy]):
    pass


masking_strategy_factory = MaskingStrategyFactory()
register = masking_strategy_factory.register
get_strategy = masking_strategy_factory.get_strategy
get_strategies = masking_strategy_factory.get_strategies
