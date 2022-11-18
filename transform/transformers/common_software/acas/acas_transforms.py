from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Callable


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


initial_transformations: Dict[str, TransformType] = {
    "11": TransformType.DATE
}


derived_transformations: Dict[str, DerivedTransform] = {
    "158": DerivedTransform(
        DerivedTransformType.ADDITION,
        ["150", "151", "152", "153", "154", "155", "156"])
}

replacement_transformations: Dict[str, Dict[str, Callable[[str], int]]] = {
    "9977": {
        "902": lambda v: 1 if v == "Yes" else 2,
        "903": lambda v: 1 if v == "No" else 2,
    }
}
