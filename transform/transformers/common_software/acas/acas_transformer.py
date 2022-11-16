import structlog

from transform.transformers.common_software.acas.acas_transforms import transformations
from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.survey_transformer import SurveyTransformer

logger = structlog.get_logger()


def perform_transforms(response_data: dict, transformation_dict: dict) -> dict:
    return {}


class ACASTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the ACAS survey."""

    def _format_pck(self, transformed_data):
        """Return a pck file using provided data"""
        pck = CSFormatter.get_pck(
            transformed_data,
            self.survey_response.instrument_id,
            self.survey_response.ru_ref,
            self.survey_response.ru_check,
            self.survey_response.period
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.survey_response.ru_ref, tx_id=self.survey_response.tx_id)
        bound_logger.info("Transforming data for processing")
        transformed_data = perform_transforms(self.survey_response.data, transformations)
        bound_logger.info("Data successfully transformed")

        bound_logger.info("Creating PCK")
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        bound_logger.info("Successfully created PCK")
        return pck_name, pck
