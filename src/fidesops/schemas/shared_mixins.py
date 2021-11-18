from typing import Dict, Any, List

from fideslang.validation import FidesKey, FidesValidationError
from pydantic import root_validator
from pydantic.main import BaseModel


class FidesKeyMixin(BaseModel):
    """
    Abstract mixin to validate fields of type FidesKey
    Converts FidesValidationError to api-friendly ValueError
    """

    _fides_key_field_names: List[str] = ["key"]

    @root_validator()
    def validate_keys(cls, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Calls validate function for fields that claim to be a FidesKey"""
        for key, val in fields.items():
            if key in cls._fides_key_field_names and val is not None:
                cls._validate(val)
        return fields

    @staticmethod
    def _validate(val: Any) -> None:
        """Determines whether val is a valid FidesKey, else throws ValueError"""
        try:
            FidesKey.validate(val)
        except FidesValidationError as exc:
            raise ValueError(exc)
