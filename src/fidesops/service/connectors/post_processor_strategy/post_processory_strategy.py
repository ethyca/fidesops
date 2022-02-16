from abc import ABC, abstractmethod
from typing import Any


class PostProcessorStrategy(ABC):
    """Abstract base class for SaaS post processor strategies"""

    @abstractmethod
    def process(self, data: Any, params: Any) -> Any:
        """Process data from SaaS connector"""
