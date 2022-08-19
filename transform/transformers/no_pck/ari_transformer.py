import json

from transform.transformers.survey_transformer import SurveyTransformer

qcode_mapping = {
    "2": "1.1",
    "3": "1.2",
    "4": "2.1",
    "5": "2.2",
    "6": "3.1",
    "7": "3.2",
    "8": "3.3",
    "9": "3.4",
    "10": "4.1",
    "13": "4.2",
    "146": "146"
}


class ARITransformer(SurveyTransformer):
    """
    Transformer for the Annual Railways Investment Survey.
    ARI does not require a pck file but does need a bespoke name for the json file.

    The json received from EQ contains qcodes, however there is a requirement for
    the images and json to use the actual question id (short code) instead.
    These are therefore mapped in before any processing takes place.
    """

    def __init__(self, response, seq_nr=0):
        data = {qcode_mapping.get(k, k): v for k, v in response.data.items()}
        response.data = data
        super().__init__(response, seq_nr)

    def get_json(self):
        json_name = f"{self.survey_response.survey_id}_{self.survey_response.ru_ref}_{self.survey_response.period}.json"
        json_file = json.dumps(self.survey_response)
        return json_name, json_file
