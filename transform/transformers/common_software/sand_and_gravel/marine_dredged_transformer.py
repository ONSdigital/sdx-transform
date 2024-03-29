from typing import Dict, List

from sdx_gcp.app import get_logger

from transform.settings import USE_IMAGE_SERVICE
from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.common_software.sand_and_gravel.marine_dredged_transforms import Transform, TRANSFORMS_SPEC, \
    ADDITION_QCODES
from transform.transformers.response import SurveyResponse
from transform.transformers.survey_transformer import SurveyTransformer

logger = get_logger()


def perform_transforms(data: Dict[str, str], transforms_spec: Dict[str, Transform],
                       addition_spec: Dict[str, List[str]]) -> Dict[str, int]:

    output_dict = {}

    for k, v in transforms_spec.items():
        try:
            if v == Transform.UNIT:
                if k not in data:
                    output_dict[k] = ""
                else:
                    output_dict[k] = int(data[k])

            if v == Transform.TEXT:
                if k not in data:
                    output_dict[k] = 2
                else:
                    output_dict[k] = 1 if data.get(k) != "" else 2

        except ValueError:
            logger.error(f"Unable to process qcode: {k} as received non numeric value: {v}")
            output_dict[k] = 0

    for k, v in addition_spec.items():
        try:
            total = 0
            for qcode in v:
                if qcode:
                    total += output_dict[qcode]
            output_dict[k] = total

        except KeyError:
            logger.error("Unable to add qcodes during addition process")

    return output_dict


def extract_pck_period(period: str) -> str:
    if len(period) <= 4:
        return period
    return period[2:]


class MarineTransformer(SurveyTransformer):

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
        transformed_data = perform_transforms(self.survey_response.data, TRANSFORMS_SPEC, ADDITION_QCODES)
        logger.info("Data successfully transformed")

        logger.info("Creating PCK")
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        logger.info("Successfully created PCK")
        return pck_name, pck
