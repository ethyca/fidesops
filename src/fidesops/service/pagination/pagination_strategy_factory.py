from __future__ import annotations

import logging

from fidesops.service.generic_strategy_factory import GenericStrategyFactory
from fidesops.service.pagination.pagination_strategy import PaginationStrategy

logger = logging.getLogger(__name__)


class PaginationStrategyFactory(GenericStrategyFactory[PaginationStrategy]):
    pass


pagination_strategy_factory = PaginationStrategyFactory()
register = pagination_strategy_factory.register
get_strategy = pagination_strategy_factory.get_strategy
