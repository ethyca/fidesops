from typing import Literal, Optional

from fideslang.validation import FidesKey
from pydantic import BaseModel

EdgeDirection = Literal["from", "to"]


class FidesOpsKey(FidesKey):
    """
    Overrides fideslang FidesKey validation to throw ValueError
    """

    @classmethod
    def validate(cls, value: Optional[str]) -> Optional[str]:
        """Throws ValueError if val is not a valid FidesKey"""
        if value is not None and not cls.regex.match(value):
            raise ValueError(
                "FidesKey must only contain alphanumeric characters, '.' or '_'."
            )

        return value


# NOTE: this extends pydantic.BaseModel instead of our BaseSchema, for
# consistency with other fideslang models
class FidesopsDatasetReference(BaseModel):
    """Reference to a field from another Collection"""

    dataset: FidesOpsKey
    field: str
    direction: Optional[EdgeDirection]
