from typing import Dict

from sdx_gcp.app import get_logger

from transform.settings import USE_IMAGE_SERVICE
from transform.transformers.common_software.bricks.bricks_transform_spec import BRICKS_DICT, PREPEND_QCODE, Transform, \
    ADDITION_DICT, TRANSFORMS_SPEC
from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.response import SurveyResponse
from transform.transformers.survey_transformer import SurveyTransformer

logger = get_logger()


def get_prepend_value(data: Dict[str, str]) -> str:
    return BRICKS_DICT.get(data.get(PREPEND_QCODE), "")


def prepend_to_qcode(qcode: str, value: str) -> str:
    return f"{value}{qcode}"


def perform_transforms(data: Dict[str, str], transforms_spec: Dict[str, Transform]) -> Dict[str, int]:

    prepend_value = get_prepend_value(data)
    output_dict = {}

    for k, v in transforms_spec.items():
        try:
            if v == Transform.TEXT:
                if k not in data:
                    output_dict[k] = 2
                else:
                    output_dict[k] = 1 if data.get(k) != "" else 2

            if k not in data and k not in ADDITION_DICT:
                continue

            if v == Transform.PREPEND:
                output_dict[f"{prepend_value}{k}"] = int(data[k])

            if v == Transform.ADDITION:
                qcode_list = ADDITION_DICT.get(k)
                total = 0

                for qcode in qcode_list:
                    output = data.get(qcode, "0")

                    total += int(output)

                output_dict[k] = total

        except ValueError:
            logger.error(f"Unable to process qcode: {k} as received non numeric value: {v}")

    return output_dict


def extract_pck_period(period: str) -> str:
    if len(period) <= 4:
        return period
    return period[2:]


class BricksTransformer(SurveyTransformer):

    def __init__(self, response: SurveyResponse, seq_nr=0):
        super().__init__(response, seq_nr, use_sdx_image=USE_IMAGE_SERVICE)

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
        transformed_data = perform_transforms(self.survey_response.data, TRANSFORMS_SPEC)
        logger.info("Data successfully transformed")

        logger.info("Creating PCK")
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        logger.info("Successfully created PCK")
        return pck_name, pck
