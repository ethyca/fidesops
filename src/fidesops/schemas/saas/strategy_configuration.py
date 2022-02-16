from typing import Dict

from pydantic import BaseModel


class StrategyConfiguration(BaseModel):
    """Base class for strategy configuration"""

    pass


class UnwrapPostProcessorConfiguration(StrategyConfiguration):
    """Dynamic JSON path access"""
    data_path: str


class FilterPostProcessorConfiguration(StrategyConfiguration):
    """Returns objects where a field has a given value"""
    field: str
    value: Dict[str, str]

