from dataclasses import dataclass
from enum import Enum
from typing import List


class TransformType(Enum):
    DATE = 1
    CURRENCY = 2
    TEXT_FIELD = 3
    NUMBER = 4


class DerivedTransformType(Enum):
    ADDITION = 1
    NON_ZEROS = 2


@dataclass(order=True)
class DerivedTransform:
    transform_type: DerivedTransformType
    parent_qcodes: List[str]


initial_transformations = {
}


derived_transformations = {

}
