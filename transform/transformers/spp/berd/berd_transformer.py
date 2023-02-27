from dataclasses import dataclass
from typing import Union, Dict, List


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


def extract_answers(data: Dict) -> List[Answer]:

    answer_list = []

    for x in data["answers"]:
        answer_id = x["answer_id"]
        list_item_id = x.get("list_item_id")
        value = x["value"]
        qcode, group = None, None

        for y in data["answer_codes"]:
            if y["answer_id"] == answer_id:
                qcode = y["code"]

        for z in data["lists"]:
            if list_item_id in z["items"]:
                group = z["name"]

        answer_list.append(Answer(qcode, value, list_item_id, group))

    return answer_list


def convert_to_spp(answer_list: List[Answer]) -> List[SPP]:

    spp_list = []
    group_dict = {}

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





