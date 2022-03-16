import json

from transform.transformers.survey_transformer import SurveyTransformer


class QFITransformer(SurveyTransformer):
    """Transformer for the Quarterly Fuels Investment Survey.
    QFI does not require a pck file but does need a bespoke name for the json file."""

    def get_json(self):
        json_name = f"{self.ids.survey_id}_{self.ids.ru_ref}_{self.ids.period}.json"
        json_file = json.dumps(self.response)
        return json_name, json_file
