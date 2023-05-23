from typing import Union, Dict, List

from sdx_gcp.app import get_logger

from transform.transformers.spp.definitions import Answer, SPP

logger = get_logger()


QUESTION_CODE = "questioncode"
RESPONSE = "response"
INSTANCE = "instance"


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
        code = response[QUESTION_CODE]
        if code.isnumeric():
            stripped_values.append(response)
        else:
            for i in range(0, len(code)):
                q_code = code[i:]
                if q_code.isnumeric():
                    stripped = {
                        'questioncode': q_code,
                        'response': response[RESPONSE],
                        'instance': response[INSTANCE]
                    }
                    stripped_values.append(stripped)
                    break

    return stripped_values


def convert_civil_defence(responses: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
    """
    Converts qcode 200 and 300 into 'C' or 'D' depending on whether they represent Civil or Defence.
    This is ascertained by looking at the prefix of qcodes 202 and 300 within the same instance.
    """
    results = responses.copy()

    instances_of_202: Dict[int, str] = {}
    instances_of_302: Dict[int, str] = {}
    for r in results:
        if r[QUESTION_CODE] == 'c202' or r[QUESTION_CODE] == 'd202':
            instances_of_202[r[INSTANCE]] = r[QUESTION_CODE]
        elif r[QUESTION_CODE] == 'c302' or r[QUESTION_CODE] == 'd302':
            instances_of_302[r[INSTANCE]] = r[QUESTION_CODE]

    for r in results:
        if r[QUESTION_CODE] == '200':
            i = r[INSTANCE]
            if i in instances_of_202:
                r[RESPONSE] = instances_of_202[i][0:1].upper()
        elif r[QUESTION_CODE] == '300':
            i = r[INSTANCE]
            if i in instances_of_302:
                r[RESPONSE] = instances_of_302[i][0:1].upper()

    return results
