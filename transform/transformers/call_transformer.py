import json
from typing import Final

from sdx_gcp import RequestsResponse
from sdx_gcp.app import get_logger

from transform.settings import sdx_app, TRANSFORMER_SERVICE_URL
from transform.transformers.response import SurveyResponse

logger = get_logger()

END_POINT: Final = "pck"


def get_pck(survey_response: SurveyResponse) -> bytes:

    logger.info("Calling sdx-transformer...")
    survey_data = json.dumps(survey_response.data)
    endpoint = END_POINT
    tx_id = survey_response.tx_id
    response: RequestsResponse = sdx_app.http_post(
        TRANSFORMER_SERVICE_URL,
        endpoint,
        survey_data,
        params={
            "tx_id": tx_id,
            "survey_id": survey_response.survey_id,
            "period_id": survey_response.period,
            "ru_ref": survey_response.ru_ref,
            "form_type": survey_response.instrument_id,
        }
    )

    return response.content
