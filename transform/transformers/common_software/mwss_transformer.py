from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.survey_transformer import DelegatedTransformer


class MWSSTransformer(DelegatedTransformer):
    """Perform the transforms and formatting for the MWSS survey."""

    def get_pck_name(self) -> str:
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        return pck_name
