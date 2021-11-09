from abc import abstractmethod, ABC
from typing import Any


class ThirdPartyBase(ABC):
    """
    Base class for third party privacy request services
    """

    @abstractmethod
    def notify_request(self, success: bool, context: Any) -> None:
        """callback for success / error of privacy request"""
