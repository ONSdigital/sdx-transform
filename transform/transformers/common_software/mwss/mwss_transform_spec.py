from enum import Enum
from decimal import ROUND_HALF_UP


class Transform(Enum):
    EXISTS = 1
    ROUND = 2
    AGGREGATE = 3
    ANY_MATCHES = 4
    MEAN = 5
    ANY_DATE = 6
    CONCAT = 7


class MatchType(Enum):
    CONTAINS = 1


TEMPLATE = {
    "040": "$AGG_40",
    "050": "$AGG_50",
    "060": "$AGG_60",
    "070": "$AGG_70",
    "080": "$AGG_80",
    "090": "$MATCH_NO_90",
    "100": "$MEAN_100",
    "110": "$DATE_110",
    "120": "$MEAN_120",
    "130": "#130",
    "131": "#131",
    "132": "#132",
    "140": "$AGG_140",
    "151": "$ROUND",
    "152": "$ROUND",
    "153": "$ROUND",
    "171": "$ROUND",
    "172": "$ROUND",
    "173": "$ROUND",
    "181": "$ROUND",
    "182": "$ROUND",
    "183": "$ROUND",
    "190": "$MATCH_NO_190",
    "200": "$EXISTS_200",
    "210": "$DATE_210",
    "220": "$MEAN_220",
    "300": "$CONCAT_300",
}


TRANSFORMS = {
    "$ROUND": {
        "name": Transform.ROUND,
        "args": {
            "precision": "1",
            "direction": ROUND_HALF_UP
        }
    },
    "$AGG_40": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#40f"],
            "weight": "1"
        },
        "post": "$ROUND"
    },
    "$AGG_50": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#50f"],
            "weight": "0.5"
        },
        "post": "$ROUND"
    },
    "$AGG_60": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#60f"],
            "weight": "0.5"
        },
        "post": "$ROUND"
    },
    "$AGG_70": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#70f"],
            "weight": "0.5"
        },
        "post": "$ROUND"
    },
    "$AGG_80": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#80f"],
            "weight": "0.5"
        },
        "post": "$ROUND"
    },
    "$MATCH_NO_90": {
        "name": Transform.ANY_MATCHES,
        "args": {
            "values": ["#90w", "#90f"],
            "match": "No",
            "match_type": MatchType.CONTAINS,
            "on_true": "1",
            "on_false": "2"
        },
    },
    "$MEAN_100": {
        "name": Transform.MEAN,
        "args": {
            "values": ["#100f"],
        },
    },
    "$DATE_110": {
        "name": Transform.ANY_DATE,
        "args": {
            "values": ["#110f"],
            "on_true": "1",
            "on_false": "2"
        },
    },
    "$MEAN_120": {
        "name": Transform.MEAN,
        "args": {
            "values": ["120f"],
        },
    },
    "$AGG_140": {
        "name": Transform.AGGREGATE,
        "args": {
            "values": ["#140m", "#140w4", "#140w5"],
            "weight": "1"
        },
        "post": "$ROUND"
    },
    "$MATCH_NO_190": {
        "name": Transform.ANY_MATCHES,
        "args": {
            "values": ["#190w4", "#190m", "#190w5"],
            "match": "No",
            "match_type": MatchType.CONTAINS,
            "on_true": "1",
            "on_false": "2"
        },
    },
    "$EXISTS_200": {
        "name": Transform.EXISTS,
        "args": {
            "on_true": "1",
            "on_false": "2"
        },
    },
    "$DATE_210": {
        "name": Transform.ANY_DATE,
        "args": {
            "values": ["#210w4", "#210w5"],
            "on_true": "1",
            "on_false": "2"
        },
    },
    "$MEAN_220": {
        "name": Transform.MEAN,
        "args": {
            "values": ["#220w4", "#220w5"],
        },
    },
    "$CONCAT_300": {
        "name": Transform.CONCAT,
        "args": {
            "values": ["#300w", "#300f", "#300m", "#300w4", "#300w5"],
            "seperator": "\n"
        },
    },
}
