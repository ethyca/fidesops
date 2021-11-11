from abc import abstractmethod, ABC
from typing import Generic, Optional, Any, TypeVar
from enum import Enum

from bson.errors import InvalidId
from bson.objectid import ObjectId

T = TypeVar("T")


class DataType(ABC, Generic[T]):
    @abstractmethod
    def to_value(other: Any) -> Optional[T]:
        """How to convert from another datatype value to this type"""

    @abstractmethod
    def empty_value(self):
        pass


class StringType(DataType, str):
    def to_value(other: Any)->Optional[str]:
        return other and str(other) or None

    def empty_value(self)->Optional[str]:
        return ""


class IntType(DataType, int):
    def to_value(other: Any) -> Optional[int]:
        try:
            return int(other)

        except ValueError:
            return None

    def empty_value(self):
        return 0



class FloatType(DataType, float):
    def to_value(other: Any) -> Optional[float]:
        try:
            return float(other)

        except ValueError:
            return None

    def empty_value(self):
        return 0.0


class BooleanType(DataType, bool):

    true_vals = {"True","true", True, 1}
    false_vals = {"False", "false", False, 0}

    def to_value(other: Any) -> Optional[bool]:
        if other in BooleanType.true_vals:
            return True
        if other in BooleanType.false_vals:
            return False
        return None

    def empty_value(self):
        return False

class NoneType(DataType, None):
    def to_value(other: Any):
        return None

    def empty_value(self):
        return None

class ObjectIdType(DataType, ObjectId):
    def to_value(other: Any) -> Optional[ObjectId]:
        """Note: ObjectId also supports a 12-byte form, although it's unlikely we're going to use it."""
        t=type(other)
        if t == ObjectId:
            return other
        if t == str and len(t) == 24:
            try:
                return ObjectId(str)
            except InvalidId:
                return None
        return None

    def empty_value(self):
        return ObjectId("000000000000000000000000")


class DataType(Enum):
    """Supported data types for data retrieval and erasure.

    This type list is based on json-schema, with some alterations:
    - mongo_object_id is added to address mongodb keys
    - the json-schema 'null' type is omitted
    """

    string = StringType()
    integer = IntType()
    number = FloatType()
    boolean = BooleanType()
    object_id = ObjectIdType()
    none = NoneType()

