from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Callable


class TransformType(Enum):
    DATE = 1
    CURRENCY = 2
    TEXT_FIELD = 3
    NUMBER = 4


class DerivedTransformType(Enum):
    ADDITION = 1
    NON_ZEROS = 2


@dataclass(order=True)
class DerivedTransform:
    transform_type: DerivedTransformType
    parent_qcodes: List[str]


initial_transformations: Dict[str, TransformType] = {
    '11': TransformType.DATE,
    '12': TransformType.DATE,
    '150': TransformType.CURRENCY,
    '151': TransformType.CURRENCY,
    '152': TransformType.CURRENCY,
    '153': TransformType.CURRENCY,
    '154': TransformType.CURRENCY,
    '155': TransformType.CURRENCY,
    '156': TransformType.CURRENCY,
    '159': TransformType.CURRENCY,
    '160': TransformType.CURRENCY,
    '161': TransformType.CURRENCY,
    '162': TransformType.CURRENCY,
    '163': TransformType.CURRENCY,
    '164': TransformType.CURRENCY,
    '165': TransformType.CURRENCY,
    '166': TransformType.CURRENCY,
    '167': TransformType.CURRENCY,
    '168': TransformType.CURRENCY,
    '169': TransformType.CURRENCY,
    '170': TransformType.CURRENCY,
    '171': TransformType.CURRENCY,
    '172': TransformType.CURRENCY,
    '173': TransformType.CURRENCY,
    '200': TransformType.CURRENCY,
    '201': TransformType.CURRENCY,
    '202': TransformType.CURRENCY,
    '203': TransformType.CURRENCY,
    '204': TransformType.CURRENCY,
    '205': TransformType.CURRENCY,
    '206': TransformType.CURRENCY,
    '207': TransformType.CURRENCY,
    '208': TransformType.CURRENCY,
    '209': TransformType.CURRENCY,
    '210': TransformType.CURRENCY,
    '211': TransformType.CURRENCY,
    '212': TransformType.CURRENCY,
    '213': TransformType.CURRENCY,
    '214': TransformType.CURRENCY,
    '215': TransformType.CURRENCY,
    '218': TransformType.CURRENCY,
    '219': TransformType.CURRENCY,
    '220': TransformType.CURRENCY,
    '221': TransformType.CURRENCY,
    '225': TransformType.TEXT_FIELD,
    '226': TransformType.CURRENCY,
    '227': TransformType.CURRENCY,
    '228': TransformType.TEXT_FIELD,
    '229': TransformType.CURRENCY,
    '230': TransformType.CURRENCY,
    '231': TransformType.TEXT_FIELD,
    '232': TransformType.CURRENCY,
    '233': TransformType.CURRENCY,
    '234': TransformType.TEXT_FIELD,
    '235': TransformType.CURRENCY,
    '236': TransformType.CURRENCY,
    '300': TransformType.CURRENCY,
    '301': TransformType.CURRENCY,
    '302': TransformType.CURRENCY,
    '303': TransformType.CURRENCY,
    '304': TransformType.CURRENCY,
    '305': TransformType.CURRENCY,
    '306': TransformType.CURRENCY,
    '307': TransformType.CURRENCY,
    '308': TransformType.CURRENCY,
    '309': TransformType.CURRENCY,
    '310': TransformType.CURRENCY,
    '311': TransformType.CURRENCY,
    '315': TransformType.CURRENCY,
    '316': TransformType.CURRENCY,
    '317': TransformType.CURRENCY,
    '318': TransformType.CURRENCY,
    '319': TransformType.CURRENCY,
    '320': TransformType.CURRENCY,
    '321': TransformType.CURRENCY,
    '322': TransformType.CURRENCY,
    '400': TransformType.CURRENCY,
    '401': TransformType.CURRENCY,
    '402': TransformType.CURRENCY,
    '403': TransformType.CURRENCY,
    '404': TransformType.CURRENCY,
    '405': TransformType.CURRENCY,
    '406': TransformType.CURRENCY,
    '407': TransformType.CURRENCY,
    '408': TransformType.CURRENCY,
    '409': TransformType.CURRENCY,
    '410': TransformType.CURRENCY,
    '411': TransformType.CURRENCY,
    '412': TransformType.CURRENCY,
    '413': TransformType.CURRENCY,
    '414': TransformType.CURRENCY,
    '415': TransformType.CURRENCY,
    '416': TransformType.CURRENCY,
    '417': TransformType.CURRENCY,
    '418': TransformType.CURRENCY,
    '419': TransformType.CURRENCY,
    '420': TransformType.CURRENCY,
    '421': TransformType.CURRENCY,
    '500': TransformType.CURRENCY,
    '501': TransformType.CURRENCY,
    '502': TransformType.CURRENCY,
    '503': TransformType.CURRENCY,
    '504': TransformType.CURRENCY,
    '505': TransformType.CURRENCY,
    '506': TransformType.CURRENCY,
    '507': TransformType.CURRENCY,
    '508': TransformType.CURRENCY,
    '509': TransformType.CURRENCY,
    '510': TransformType.CURRENCY,
    '511': TransformType.CURRENCY,
    '512': TransformType.CURRENCY,
    '513': TransformType.CURRENCY,
    '514': TransformType.CURRENCY,
    '515': TransformType.CURRENCY,
    '516': TransformType.CURRENCY,
    '517': TransformType.CURRENCY,
    '518': TransformType.CURRENCY,
    '519': TransformType.CURRENCY,
    '601': TransformType.CURRENCY,
    '602': TransformType.CURRENCY,
    '603': TransformType.CURRENCY,
    '604': TransformType.CURRENCY,
    '605': TransformType.CURRENCY,
    '606': TransformType.CURRENCY,
    '607': TransformType.CURRENCY,
    '608': TransformType.CURRENCY,
    '609': TransformType.CURRENCY,
    '610': TransformType.CURRENCY,
    '611': TransformType.CURRENCY,
    '612': TransformType.CURRENCY,
    '613': TransformType.CURRENCY,
    '614': TransformType.CURRENCY,
    '615': TransformType.CURRENCY,
    '616': TransformType.CURRENCY,
    '617': TransformType.CURRENCY,
    '618': TransformType.CURRENCY,
    '700': TransformType.CURRENCY,
    '701': TransformType.CURRENCY,
    '702': TransformType.CURRENCY,
    '703': TransformType.CURRENCY,
    '704': TransformType.CURRENCY,
    '705': TransformType.CURRENCY,
    '706': TransformType.CURRENCY,
    '707': TransformType.CURRENCY,
    '708': TransformType.CURRENCY,
    '709': TransformType.CURRENCY,
    '710': TransformType.CURRENCY,
    '711': TransformType.CURRENCY,
    '712': TransformType.CURRENCY,
    '713': TransformType.CURRENCY,
    '714': TransformType.CURRENCY,
    '715': TransformType.CURRENCY,
    '800': TransformType.CURRENCY,
    '801': TransformType.CURRENCY,
    '802': TransformType.CURRENCY,
    '803': TransformType.CURRENCY,
    '804': TransformType.CURRENCY,
    '805': TransformType.CURRENCY,
    '806': TransformType.CURRENCY,
    '807': TransformType.CURRENCY,
    '811': TransformType.TEXT_FIELD,
    '812': TransformType.CURRENCY,
    '813': TransformType.CURRENCY,
    '814': TransformType.TEXT_FIELD,
    '815': TransformType.CURRENCY,
    '816': TransformType.CURRENCY,
    '817': TransformType.TEXT_FIELD,
    '818': TransformType.CURRENCY,
    '819': TransformType.CURRENCY,
    '820': TransformType.TEXT_FIELD,
    '821': TransformType.CURRENCY,
    '822': TransformType.CURRENCY,
    '823': TransformType.TEXT_FIELD,
    '824': TransformType.CURRENCY,
    '825': TransformType.CURRENCY,
    '826': TransformType.TEXT_FIELD,
    '827': TransformType.CURRENCY,
    '828': TransformType.CURRENCY,
    '901': TransformType.CURRENCY,
    '904': TransformType.NUMBER,
    '905': TransformType.NUMBER,
    '146': TransformType.TEXT_FIELD
}


derived_transformations: Dict[str, DerivedTransform] = {
    "158": DerivedTransform(
        DerivedTransformType.ADDITION,
        ["150", "151", "152", "153", "154", "155", "156"])
}

replacement_transformations: Dict[str, Dict[str, Callable[[str], int]]] = {
    "9977": {
        "902": lambda v: 1 if v == "Yes" else 2,
        "903": lambda v: 1 if v == "No" else 2,
    }
}