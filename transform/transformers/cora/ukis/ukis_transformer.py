import decimal
import logging
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List

import structlog

from transform.transformers.cora.ukis.ukis_transforms import TransformType

logger = structlog.get_logger()


def perform_transforms(
        response_data: Dict[str, str],
        transformation_dict: Dict[str, TransformType],
        expected_checkbox_qcodes: List[str]) -> Dict[str, str]:

    result = {}
    remaining_checkbox_qcodes = set(expected_checkbox_qcodes)

    for qcode, value in response_data.items():
        try:
            if qcode in transformation_dict:
                transform_type = transformation_dict[qcode]

                if transform_type == TransformType.CURRENCY:
                    converted_value = thousands_transform(value)

                if transform_type == TransformType.YESNO:
                    converted_value = yes_no_transform(value)

                if transform_type == TransformType.IMPORTANCE:
                    converted_value = importance_transform(value)

                if transform_type == TransformType.CHECKBOX:
                    converted_value = checkbox_transform(value)
                    remaining_checkbox_qcodes.remove(qcode)

                if transform_type == TransformType.PERCENTAGE:
                    converted_value = percentage_transform(value)

                result[qcode] = converted_value

        except ValueError:
            logging.error(f"ValueError with qcode {qcode}, with value {value}")

    for qcode in remaining_checkbox_qcodes:
        result[qcode] = ""

    return result


def percentage_transform(value: str) -> str:
    if value.lower() == "over 90%":
        return "0001"
    elif value.lower() == "40-90%":
        return "0010"
    elif value.lower() == "less than 40%":
        return "0011"
    elif value.lower() == "none":
        return "0100"
    else:
        return ""


def checkbox_transform(value: str) -> str:
    if value.lower() != "":
        return "1"


def yes_no_transform(value: str) -> str:
    if value.lower() == "yes":
        return "10"
    elif value.lower() == "no":
        return "01"
    elif value == "":
        return ""


def importance_transform(value: str) -> str:
    if value.lower() == "high importance":
        return "1000"
    elif value.lower() == "medium importance":
        return "0100"
    elif value.lower() == "low importance":
        return "0010"
    elif value.lower() == "not important":
        return "0001"
    elif value == "":
        return ""


def thousands_transform(value: str) -> int:
    """
    Round to the nearest thousand.
    """
    try:
        decimal.getcontext().rounding = ROUND_HALF_UP
        return int(Decimal(round(Decimal(float(value))) / 1000).quantize(1))

    except TypeError:
        logger.info("Tried to quantize a NoneType object. Returning an empty string")
        raise ValueError("Invalid value")


