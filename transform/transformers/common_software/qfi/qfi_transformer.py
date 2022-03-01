import structlog

from transform.transformers.survey_transformer import SurveyTransformer
from transform.utilities.formatter import Formatter

logger = structlog.get_logger()


class QFITransformer(SurveyTransformer):
    """Perform the transforms and formatting for the QFI survey."""

    def __init__(self, response, seq_nr=0):
        super().__init__(response, seq_nr)

    def create_pck(self):
        pck_name = ""
        pck = None
        return pck_name, pck
