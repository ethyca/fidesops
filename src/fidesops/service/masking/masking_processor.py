import logging

from typing import List

from fidesops.schemas.policy import PolicyMaskingSpec
from fidesops.service.masking.strategy import masking_strategy_factory

logger = logging.getLogger(__name__)


# Deferred-TODO MASKING validator to be built - ex. datatype lengths for hashing strategy, data type, etc.
def mask(value: str, masking_strategies: List[PolicyMaskingSpec]) -> str:
    """Masks the value using the provided strategies in sequential order"""
    masked_value = value
    logger.info(
        f"Masking value with these strategies {[strat.strategy for strat in masking_strategies]} in this order"
    )
    for strategy in masking_strategies:
        strategy = masking_strategy_factory.get_strategy(
            strategy.strategy, strategy.configuration
        )
        # fixme: generate secrets, but what privacy request id to use?
        masked_value = strategy.mask(masked_value, None)
    return masked_value
