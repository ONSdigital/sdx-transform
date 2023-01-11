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

                if transform_type == TransformType.PERCENTRADIO:
                    converted_value = percent_radio_transform(value)

                if transform_type == TransformType.PERCENTAGE:
                    converted_value = percentage_transform(value)

                if transform_type == TransformType.NUMBER:
                    converted_value = number_transform(value)

                if transform_type == TransformType.TEXT:
                    converted_value = text_transform(value)

                if transform_type == TransformType.TEMPRADIO:
                    converted_value = temp_radio_transform(value)

                result[qcode] = converted_value

        except ValueError:
            logging.error(f"ValueError with qcode {qcode}, with value {value}")

    for qcode in remaining_checkbox_qcodes:
        result[qcode] = ""

    return result


def temp_radio_transform(value: str) -> str:
    if value.lower() == "further than 15 miles from the physical sites of your business and within the uk":
        return "temp answer"


def percentage_transform(value: str) -> str:
    if value.isdigit():
        return value
    else:
        return ""


def number_transform(value: str) -> str:
    if value.isdigit():
        return value
    else:
        raise ValueError("Non numeric value")


def text_transform(value: str):
    if value:
        return "1"
    return "2"


def percent_radio_transform(value: str) -> str:
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
    if value.lower() == "yes" or value.lower() == "yes, they were significant":
        return "10"
    elif value.lower() == "no" or value.lower() == "no, they were not significant":
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


def thousands_transform(value: str) -> str:
    """
    Round to the nearest thousand.
    """
    try:
        decimal.getcontext().rounding = ROUND_HALF_UP
        return str(int(Decimal(round(Decimal(float(value))) / 1000).quantize(1)))

    except TypeError:
        logger.info("Tried to quantize a NoneType object. Returning an empty string")
        raise ValueError("Invalid value")


