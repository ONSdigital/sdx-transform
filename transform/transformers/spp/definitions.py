from dataclasses import dataclass
from typing import Union, List


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
