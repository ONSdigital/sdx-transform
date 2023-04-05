import decimal
import logging
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List

import structlog

from transform.transformers.cora.cora_formatter import CORAFormatter
from transform.transformers.cora.ukis.ukis_transforms import TransformType, ukis_transformations
from transform.transformers.survey_transformer import SurveyTransformer

logger = structlog.get_logger()


def perform_transforms(
        response_data: Dict[str, str],
        transformation_dict: Dict[str, TransformType]):

    result = {}

    for qcode, transform_type in transformation_dict.items():
        try:
            if transform_type == TransformType.ZERO:
                result[qcode] = "0"

            elif transform_type == TransformType.DISTANCE_RADIO:
                if qcode == "2121":
                    distance_qcodes = ["2121", "2122", "2123", "2124"]
                elif qcode == "2131":
                    distance_qcodes = ["2131", "2132", "2133", "2134"]
                else:
                    continue

                if qcode in response_data:
                    converted_value_dict = distance_radio_transform(response_data[qcode], distance_qcodes)
                    result.update(converted_value_dict)

            elif qcode in response_data:
                value = response_data[qcode]

                if transform_type == TransformType.CURRENCY:
                    converted_value = thousands_transform(value)

                elif transform_type == TransformType.ZERO:
                    converted_value = "0"

                elif transform_type == TransformType.YESNO:
                    converted_value = yes_no_transform(value)

                elif transform_type == TransformType.IMPORTANCE:
                    converted_value = importance_transform(value)

                elif transform_type == TransformType.CHECKBOX:
                    converted_value = checkbox_transform(value)

                elif transform_type == TransformType.PERCENT_RADIO:
                    converted_value = percent_radio_transform(value)

                elif transform_type == TransformType.PERCENTAGE:
                    converted_value = percentage_transform(value)

                elif transform_type == TransformType.NUMBER:
                    converted_value = number_transform(value)

                elif transform_type == TransformType.TEXT:
                    converted_value = text_transform(value)

                else:
                    continue

                result[qcode] = converted_value

            else:
                result[qcode] = ""

        except ValueError:
            logging.error(f"ValueError with qcode {qcode}")

    return result


def distance_radio_transform(value: str, qcode_list: List[str]) -> Dict[str, str]:

    distance_radio_output = {
        qcode_list[0]: "0",
        qcode_list[1]: "0",
        qcode_list[2]: "0",
        qcode_list[3]: "0"
    }

    if value.lower().startswith("within"):
        distance_radio_output[qcode_list[0]] = "1"
    elif value.lower().startswith("further"):
        distance_radio_output[qcode_list[1]] = "1"
    elif value.lower().startswith("outside"):
        distance_radio_output[qcode_list[2]] = "1"
    elif value.lower().startswith("your business"):
        distance_radio_output[qcode_list[3]] = "1"

    return distance_radio_output


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

    except Exception:
        logger.info(f"Could not convert {value} into a number:")
        return ""


class UKISTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the UKIS survey."""

    def _create_pck(self, transformed_data):
        """Return a pck file using provided data"""
        pck = CORAFormatter.get_pck(
            transformed_data,
            self.survey_response.survey_id,
            self.survey_response.ru_ref,
            "1",
            self.survey_response.period,
            "0",
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.survey_response.ru_ref, tx_id=self.survey_response.tx_id)
        bound_logger.info("Transforming data for processing")
        transformed_data = perform_transforms(self.survey_response.data, ukis_transformations)
        bound_logger.info("Data successfully transformed")
        pck_name = CORAFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._create_pck(transformed_data)
        return pck_name, pck
