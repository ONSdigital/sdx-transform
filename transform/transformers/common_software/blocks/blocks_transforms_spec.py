from typing import Dict

import structlog

from transform.settings import USE_IMAGE_SERVICE
from transform.transformers.common_software.blocks.blocks_transforms import Transform, TRANSFORMS_SPEC
from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.response import SurveyResponse
from transform.transformers.survey_transformer import SurveyTransformer

logger = structlog.get_logger()


def perform_transforms(data: Dict[str, str], transforms_spec: Dict[str, Transform]) -> Dict[str, str]:

    output_dict = {}

    for k, v in transforms_spec.items():

        try:
            if k not in data:
                continue

            if v == Transform.NO_TRANSFORM:
                output_dict[k] = int(data[k])

            elif v == Transform.TEXT:
                output_dict[k] = 1 if data[k] != "" else 0

        except ValueError:
            logger.error(f"Unable to process qcode: {k} as received non numeric value: {v}")

    return output_dict


class BlocksTransformer(SurveyTransformer):

    def __init__(self, response: SurveyResponse, seq_nr=0):
        super().__init__(response, seq_nr, use_sdx_image=USE_IMAGE_SERVICE)

    def _format_pck(self, transformed_data) -> str:
        """Return a pck file using provided data"""
        pck = CSFormatter.get_pck(
            transformed_data,
            self.survey_response.instrument_id,
            self.survey_response.ru_ref,
            self.survey_response.ru_check,
            self.survey_response.period,
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.survey_response.ru_ref, tx_id=self.survey_response.tx_id)
        bound_logger.info("Transforming data for processing")
        transformed_data = perform_transforms(self.survey_response.data, TRANSFORMS_SPEC)
        bound_logger.info("Data successfully transformed")

        bound_logger.info("Creating PCK")
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        bound_logger.info("Successfully created PCK")
        return pck_name, pck
