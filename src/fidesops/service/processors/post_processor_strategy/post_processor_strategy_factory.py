import logging

from fidesops.service.generic_strategy_factory import GenericStrategyFactory
from fidesops.service.processors.post_processor_strategy.post_processor_strategy import (
    PostProcessorStrategy,
)

logger = logging.getLogger(__name__)


class PostProcessorStrategyFactory(GenericStrategyFactory[PostProcessorStrategy]):
    pass


post_processor_strategy_factory = PostProcessorStrategyFactory()
register = post_processor_strategy_factory.register
get_strategy = post_processor_strategy_factory.get_strategy
