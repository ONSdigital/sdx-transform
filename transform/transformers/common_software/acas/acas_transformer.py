import decimal
import logging
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Callable

from sdx_gcp.app import get_logger

from transform.transformers.common_software.acas.acas_transforms import TransformType, \
    DerivedTransform, DerivedTransformType, initial_transformations, derived_transformations, \
    replacement_transformations
from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.survey_transformer import SurveyTransformer

logger = get_logger()


def perform_transforms(response_data: Dict[str, str]) -> Dict[str, int]:
    transformed_data: Dict[str, int] = perform_initial_transforms(response_data, initial_transformations)
    transformed_data: Dict[str, int] = perform_derived_transforms(transformed_data, derived_transformations)
    transformed_data: Dict[str, int] = perform_replacement_transforms(response_data,
                                                                      transformed_data,
                                                                      replacement_transformations)
    transformed_data: Dict[str, int] = perform_add_missing_text(transformed_data, initial_transformations)
    perform_replace_negatives(transformed_data, response_data)
    return transformed_data


def perform_initial_transforms(
        response_data: Dict[str, str],
        transformation_dict: Dict[str, TransformType]) -> Dict[str, int]:
    result = {}

    for qcode, value in response_data.items():

        try:
            if qcode in transformation_dict:

                transform_type = transformation_dict[qcode]

                if transform_type == TransformType.DATE:
                    converted_value = date_transform(value)

                elif transform_type == TransformType.CURRENCY:
                    converted_value = currency_transform(value)

                elif transform_type == TransformType.TEXT_FIELD:
                    converted_value = text_transform(value)

                elif transform_type == TransformType.NUMBER:
                    converted_value = number_transform(value)

                else:
                    converted_value = number_transform(value)

                result[qcode] = converted_value

        except ValueError:
            logging.error(f"ValueError with qcode {qcode}, with value {value}")

    return result


def perform_derived_transforms(
        transformed_data: Dict[str, int],
        derived_transformation_dict: Dict[str, DerivedTransform]) -> Dict[str, int]:
    result = transformed_data.copy()

    for qcode, transform in derived_transformation_dict.items():
        parent_qcodes: List[str] = transform.parent_qcodes

        if transform.transform_type == DerivedTransformType.ADDITION:
            total = 0
            for p in parent_qcodes:
                total += result.get(p, 0)
            result[qcode] = total

        if transform.transform_type == DerivedTransformType.NON_ZEROS:
            parent_value_found = False
            for p in parent_qcodes:
                if result.get(p, 0) != 0:
                    parent_value_found = True
                    break

            result[qcode] = 2 if parent_value_found else 1

    return result


def perform_replacement_transforms(
        response_data: Dict[str, str],
        transformed_data: Dict[str, int],
        replacement_transforms: Dict[str, Dict[str, Callable[[str], int]]]) -> Dict[str, int]:
    for qcode, replacement_dict in replacement_transforms.items():
        v = response_data.get(qcode)
        if v:
            for new_qcode, func in replacement_dict.items():
                transformed_data[new_qcode] = func(v)

    return transformed_data


def perform_add_missing_text(transformed_data: Dict[str, int], initial_transforms: Dict[str, TransformType])\
        -> Dict[str, int]:
    """
    Add qcodes to transformed data if the text field was empty
    """
    for k, v in initial_transforms.items():
        if k not in transformed_data and v == TransformType.TEXT_FIELD:
            transformed_data[k] = 2

    return transformed_data


def perform_replace_negatives(transformed_data: Dict[str, int], response_data: Dict[str, str]):
    for qcode, value in response_data.items():
        if value.startswith("-"):
            if is_number(value):
                transformed_data[qcode] = 99999999999


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def currency_transform(value: str) -> int:
    """
    Round to the nearest thousand.
    """
    try:
        decimal.getcontext().rounding = ROUND_HALF_UP
        return int(Decimal(round(Decimal(float(value))) / 1000).quantize(1))

    except TypeError:
        logger.info("Tried to quantize a NoneType object. Returning an empty string")
        raise ValueError("Invalid value")


def date_transform(value: str) -> int:
    if type(value) == str:
        return int(datetime.strptime(value, "%d/%m/%Y").strftime('%d%m%y'))
    raise ValueError("Invalid value")


def text_transform(value: str) -> int:
    if value:
        return 1
    return 2


def number_transform(value: str) -> int:
    try:
        return int(value)
    except TypeError:
        raise ValueError("Non numeric value")


def extract_pck_period(period: str) -> str:
    if len(period) <= 2:
        return period
    return period[2:4]


class ACASTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the ACAS survey."""

    def _format_pck(self, transformed_data) -> str:
        """Return a pck file using provided data"""
        pck = CSFormatter.get_pck(
            transformed_data,
            self.survey_response.instrument_id,
            self.survey_response.ru_ref,
            self.survey_response.ru_check,
            extract_pck_period(self.survey_response.period),
        )
        return pck

    def create_pck(self):
        logger.info("Transforming data for processing", ru_ref=self.survey_response.ru_ref)
        transformed_data = perform_transforms(self.survey_response.data)
        logger.info("Data successfully transformed")

        logger.info("Creating PCK")
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        logger.info("Successfully created PCK")
        return pck_name, pck
