from typing import Union, Dict, List

import structlog

from transform.transformers.spp.definitions import Answer, SPP

logger = structlog.get_logger()


def spp_from_map(data: Dict[str, str]) -> List[SPP]:
    """
    Create a list of SPP from data in 0.0.1 format (map[qcode, value])
    """
    return [SPP(qcode, value, 0) for qcode, value in data.items()]


def extract_answers(data: Dict) -> List[Answer]:
    """
    Extracts list collector based data (0.0.3) into a list of 'Answer's.
    """

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
    """
    Converts answers to SPP objects by assigning an instance
    based on list_item_id and group
    """

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


def remove_prepend_values(responses: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
    """
    Removes any qcode prefixes and returns the updated responses.
    """

    stripped_values = []
    for response in responses:
        code = response['questioncode']
        if code.isnumeric():
            stripped_values.append(response)
        else:
            for i in range(0, len(code)):
                q_code = code[i:]
                if q_code.isnumeric():
                    stripped = {
                        'questioncode': q_code,
                        'response': response['response'],
                        'instance': response['instance']
                    }
                    stripped_values.append(stripped)
                    break

    return stripped_values
