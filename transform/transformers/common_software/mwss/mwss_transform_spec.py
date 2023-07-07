from enum import Enum
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP


class Transform(Enum):
    NO_TRANSFORM = 1
    ROUND = 2
    AGGREGATE = 3
    ANY_MATCHES = 4
    MEAN = 5
    ANY_DATE = 6


class MatchType(Enum):
    CONTAINS = 1


TEMPLATE = {
    "040": "$2",
    "050": "$3",
    "060": "$4",
    "070": "$5",
    "080": "$6",
    "090": "$7",
    "100": "$8",
    "110": "$9",
    "120": "$10",
}


TRANSFORMS = {
    "$1": {
        "name": Transform.ROUND,
        "args": {
            "precision": "1",
            "direction": ROUND_HALF_UP
        }
    },
    "$2": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#40f"],
            "weight": "1"
        },
        "post": "$1"
    },
    "$3": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#50f"],
            "weight": "0.5"
        },
        "post": "$1"
    },
    "$4": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#60f"],
            "weight": "0.5"
        },
        "post": "$1"
    },
    "$5": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#70f"],
            "weight": "0.5"
        },
        "post": "$1"
    },
    "$6": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#80f"],
            "weight": "0.5"
        },
        "post": "$1"
    },
    "$7": {
        "name": Transform.ANY_MATCHES,
        "args": {
            "values": [ "90w", "90f"],
            "match": "No",
            "match_type": MatchType.CONTAINS,
            "on_true": "1",
            "on_false": "2"
        },
    },
    "$8": {
        "name": Transform.MEAN,
        "args": {
            "values": ["100f"],
        },
    },
    "$9": {
        "name": Transform.ANY_DATE,
        "args": {
            "values": ["110f"],
            "on_true": "1",
            "on_false": "2"
        },
    },
    "$10": {
        "name": Transform.MEAN,
        "args": {
            "values": ["120f"],
        },
    },
    "$11": {
        "name": Transform.MEAN,
        "args": {
            "values": ["120f"],
        },
    },
}
