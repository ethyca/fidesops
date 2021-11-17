from typing import List

from fideslang.validation import FidesKey
from pydantic import BaseModel


class MaskingStrategyConfigurationDescription(BaseModel):
    """The description model for a specific configuration in a masking strategy"""

    key: FidesKey
    optional: bool = True
    description: str


class MaskingStrategyDescription(BaseModel):
    """The description model for a masking strategy"""

    name: str
    description: str
    configurations: List[MaskingStrategyConfigurationDescription]
