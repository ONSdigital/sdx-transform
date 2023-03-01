from dataclasses import dataclass
from typing import Union, Dict, List

from transform.transformers.response import SurveyResponse
from transform.transformers.survey_transformer import SurveyTransformer


@dataclass(order=True)
class Answer:
    qcode: str
    value: Union[str, None]
    list_item_id: Union[str, None]
    group: Union[str, None]


@dataclass(order=True)
class SPP:
    question_code: str
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
        answer_id = x["answer_id"]
        value = x["value"]
        qcode: Union[str, None] = None
        group: Union[str, None] = None

        for y in data["answer_codes"]:
            if y["answer_id"] == answer_id:
                qcode = y["code"]

        if not qcode:
            # log error?
            continue

        list_item_id = x.get("list_item_id")

        for z in data["lists"]:
            if list_item_id in z["items"]:
                group = z["name"]

        if qcode[0].isalpha():
            if not list_item_id:
                list_item_id = '_list_item'
                group = "default"
            list_item_id = qcode[0] + list_item_id
            qcode = qcode[1:]

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


class BERDTransformer(SurveyTransformer):
    """
    Transformer for the BERD Survey.
    """

    def __init__(self, survey_response: SurveyResponse, seq_nr=0):
        data = convert_to_spp(extract_answers(survey_response.data))

        result: SPPResult = SPPResult(
            formtype=survey_response.instrument_id,
            reference=survey_response.ru_ref,
            period=survey_response.period,
            survey=survey_response.survey_id,
            responses=data,
        )
        survey_response.response = result
        super().__init__(survey_response, seq_nr)
