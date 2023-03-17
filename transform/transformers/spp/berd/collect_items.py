from typing import List, Set

from transform.transformers.spp.definitions import Answer


def collect_list_items(answer_list: List[Answer]) -> List[Answer]:
    result_list: List[Answer] = []

    list_items: Set[str] = set()
    for answer in answer_list:
        if answer.list_item_id:
            list_items.add(answer.list_item_id)

    for answer in answer_list:
        changed = False
        for item_id in sorted(list_items):
            if is_subset_of(answer.list_item_id, item_id):
                result_list.append(
                    Answer(
                        answer.qcode,
                        answer.value,
                        item_id,
                        answer.group
                    ))
                changed = True

        if not changed:
            result_list.append(answer)

    return result_list


def is_subset_of(list_item_id: str, compare_with: str) -> bool:
    return list_item_id == compare_with[1:]
