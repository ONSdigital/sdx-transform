import json
from dataclasses import dataclass, asdict
from typing import Union, Dict, List

import structlog

from transform.settings import USE_IMAGE_SERVICE
from transform.transformers.response import SurveyResponse, InvalidDataException
from transform.transformers.survey_transformer import SurveyTransformer
from transform.utilities.formatter import Formatter

logger = structlog.get_logger()


@dataclass(order=True)
class Answer:
    qcode: str
    value: Union[str, None]
    list_item_id: Union[str, None]
    group: Union[str, None]


@dataclass(order=True)
class SPP:
    questioncode: str
    response: Union[str, None]
    instance: int


@dataclass(order=True)
class SPPResult:
    formtype: str
    reference: str
    period: str
    survey: str
    responses: List[SPP]


def extract_answers(data: Dict) -> List[Answer]:

    answer_list: List[Answer] = []

    for x in data["answers"]:

        answer_id = x.get("answer_id")
        value = str(x.get("value", ""))

        qcode: Union[str, None] = None
        group: Union[str, None] = None

        for y in data["answer_codes"]:
            if y["answer_id"] == answer_id:
                qcode = y["code"]
                break

        if not qcode:
            logger.error(f"Missing QCode for BERD, answer_id: {answer_id}")
            continue

        list_item_id = x.get("list_item_id")

        for z in data["lists"]:
            if list_item_id in z["items"]:
                group = z["name"]

        if not qcode.isnumeric():
            for i in range(0, len(qcode)):
                if qcode[i].isalpha():
                    if not list_item_id:
                        list_item_id = '_list_item'
                        group = "default"
                    list_item_id = qcode[i] + list_item_id
                    break

        answer_list.append(Answer(qcode, value, list_item_id, group))

    return answer_list


def convert_to_spp(answer_list: List[Answer]) -> List[SPP]:

    spp_list: List[SPP] = []
    group_dict: Dict[str, List[str]] = {}

    for answer in answer_list:
        instance = 0
        if answer.group:
            if answer.group not in group_dict:
                group_dict[answer.group] = []

        if answer.list_item_id:
            instance_list = group_dict[answer.group]
            if answer.list_item_id not in instance_list:
                instance_list.append(answer.list_item_id)
            instance = instance_list.index(answer.list_item_id) + 1

        spp = SPP(answer.qcode, answer.value, instance)
        spp_list.append(spp)

    return spp_list


def remove_prepend_values(reponses: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
    stripped_values = []
    for i in range(0, len(reponses)):
        code = reponses[i]['questioncode']
        if not code.isnumeric():
            for j in range(0, len(code)):
                if code[j:].isnumeric():
                    new = {
                        'questioncode': code[j:],
                        'response': reponses[i]['response'],
                        'instance': reponses[i]['instance']
                    }
                    stripped_values.append(new)
                    break

    return stripped_values


class BERDTransformer(SurveyTransformer):
    """
    Transformer for the BERD Survey.
    """
    berd_result: Dict[str, Union[str, List]]

    def __init__(self, survey_response: SurveyResponse, seq_nr=0):
        try:
            berd_data = convert_to_spp(extract_answers(survey_response.data))
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

        survey_response.response['data'] = self.berd_result["responses"]
        super().__init__(survey_response, seq_nr, use_sdx_image=USE_IMAGE_SERVICE)

    def get_json(self):
        json_name = Formatter.response_json_name(self.survey_response.survey_id, self.survey_response.tx_id)
        self.berd_result['responses'] = remove_prepend_values(self.berd_result['responses'])
        json_file = json.dumps(self.berd_result)
        return json_name, json_file
