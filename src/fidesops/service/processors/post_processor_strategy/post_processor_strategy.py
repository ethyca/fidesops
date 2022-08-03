from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from fidesops.service.generic_strategy import GenericStrategy


class PostProcessorStrategy(GenericStrategy):
    """Abstract base class for SaaS post processor strategies"""

    @abstractmethod
    def process(
        self, data: Any, identity_data: Dict[str, Any] = None
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Process data from SaaS connector"""
