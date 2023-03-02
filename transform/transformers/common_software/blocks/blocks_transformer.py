from enum import Enum
from typing import Dict


class Transform(Enum):
    NO_TRANSFORM = 1


def perform_transforms(data: Dict[str, str], transforms_spec: Dict[str, Transform]) -> Dict[str, str]:

    output_dict = {}

    for k, v in transforms_spec.items():
        if k not in data:
            continue

        if v == Transform.NO_TRANSFORM:
            output_dict[k] = data[k]

    return output_dict
