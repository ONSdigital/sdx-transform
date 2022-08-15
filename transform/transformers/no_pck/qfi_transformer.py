import json

from transform.transformers.survey_transformer import SurveyTransformer

qcode_mapping = {
    "10": "0a",
    "11": "0b",
    "12": "0c",
    "13": "0d",
    "14": "0e",
    "110": "1",
    "120": "2a",
    "121": "2b",
    "122": "2c",
    "130": "3",
    "140": "4a",
    "141": "4b",
    "142": "4c",
    "150": "5",
    "160": "6",
    "180": "8",
    "190": "9",
    "200": "11",
    "210": "12",
    "211": "12a",
    "220": "13",
    "230": "15",
    "240": "16",
    "250": "18",
    "260": "19",
    "270": "20",
    "271": "20a",
    "280": "21",
    "290": "23",
    "300": "24",
    "310": "26",
    "320": "27",
    "330": "28",
    "340": "29",
    "350": "31",
    "360": "32",
    "370": "34",
    "146": "146"
}


def calculate_total(x: str, y: str) -> str:
    try:
        return str(int(x) + int(y))
    except ValueError:
        return ''


class QFITransformer(SurveyTransformer):
    """
    Transformer for the Quarterly Fuels Investment Survey.
    QFI does not require a pck file but does need a bespoke name for the json file.

    The json received from EQ contains qcodes, however there is a requirement for
    the images and json to use the actual question id (short code) instead.
    These are therefore mapped in before any processing takes place.
    """

    def __init__(self, response, seq_nr=0):
        data = {qcode_mapping.get(k, k): v for k, v in response.data.items()}
        if '12a' in data and '15' in data:
            data['17'] = calculate_total(data['12a'], data['15'])
        if '20a' in data and '23' in data:
            data['25'] = calculate_total(data['20a'], data['23'])
        if '28' in data and '31' in data:
            data['33'] = calculate_total(data['28'], data['31'])

        response['data'] = data
        super().__init__(response, seq_nr)

    def get_json(self):
        json_name = f"{self.survey_response.survey_id}_{self.survey_response.ru_ref}_{self.survey_response.period}.json"
        json_file = json.dumps(self.survey_response)
        return json_name, json_file
