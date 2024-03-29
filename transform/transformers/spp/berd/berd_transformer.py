import json
from dataclasses import asdict
from typing import Union, Dict, List

from sdx_gcp.app import get_logger

from transform.transformers.response import SurveyResponse, InvalidDataException
from transform.transformers.spp.berd.collect_items import collect_list_items
from transform.transformers.spp.convert_data import convert_to_spp, extract_answers, remove_prepend_values, \
    spp_from_map, convert_civil_defence
from transform.transformers.spp.definitions import SPPResult
from transform.transformers.survey_transformer import SurveyTransformer
from transform.utilities.formatter import Formatter

logger = get_logger()


class BERDTransformer(SurveyTransformer):
    """
    Transformer for the BERD Survey.
    """
    berd_result: Dict[str, Union[str, List]]

    def __init__(self, survey_response: SurveyResponse, seq_nr=0):
        try:
            if survey_response.instrument_id == "0001":
                berd_data = convert_to_spp(collect_list_items(extract_answers(survey_response.data)))
            else:
                berd_data = spp_from_map(survey_response.data)
        except KeyError as e:
            raise InvalidDataException(e)

        spp_result = SPPResult(
            formtype=survey_response.instrument_id,
            reference=survey_response.ru_ref,
            period=survey_response.period,
            survey=survey_response.survey_id,
            responses=berd_data,
        )

        self.berd_result = asdict(spp_result)

        if survey_response.instrument_id == "0001":
            survey_response.response['data'] = self.berd_result["responses"]

        super().__init__(survey_response, seq_nr, use_sdx_image=True)

    def get_json(self):
        json_name = Formatter.response_json_name(self.survey_response.survey_id, self.survey_response.tx_id)
        self.berd_result['responses'] = remove_prepend_values(convert_civil_defence(self.berd_result['responses']))
        json_file = json.dumps(self.berd_result)
        return json_name, json_file
