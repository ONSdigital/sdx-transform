from typing import Dict

from transform.transformers.common_software.bricks.bricks_transform_spec import BRICKS_DICT, PREPEND_QCODE, Transform


def get_prepend_value(data: Dict[str, str]) -> str:
    return BRICKS_DICT.get(data.get(PREPEND_QCODE), "")


def prepend_to_qcode(qcode: str, value: str) -> str:
    return f"{value}{qcode}"


def perform_transforms(data: Dict[str, str], transforms_spec: Dict[str, Transform]) -> Dict[str, str]:

    prepend_value = get_prepend_value(data)
    output_dict = {}

    for k, v in transforms_spec.items():

        if k not in data:
            continue

        if v == Transform.PREPEND:
            output_dict[f"{prepend_value}{k}"] = data[k]

        if v == Transform.TEXT:
            output_dict[k] = data[k]

        # if v == Transform.ADDITION:
        #     output_dict[k] =

    return output_dict

