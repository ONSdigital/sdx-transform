from enum import Enum

BRICKS_DICT = {
    "Clay": "2",
    "Concrete": "3",
    "Sandlime": "4"
}

ADDITION_DICT = {
    "501": ["01", "11", "21"],
    "502": ["02", "12", "22"],
    "503": ["03", "13", "23"],
    "504": ["04", "14", "24"]
}

PREPEND_QCODE = "9999"


class Transform(Enum):
    PREPEND = 1
    TEXT = 2
    ADDITION = 3


TRANSFORMS_SPEC = {
    "01": Transform.PREPEND,
    "02": Transform.PREPEND,
    "03": Transform.PREPEND,
    "04": Transform.PREPEND,
    "11": Transform.PREPEND,
    "12": Transform.PREPEND,
    "13": Transform.PREPEND,
    "14": Transform.PREPEND,
    "21": Transform.PREPEND,
    "22": Transform.PREPEND,
    "23": Transform.PREPEND,
    "24": Transform.PREPEND,
    "145": Transform.TEXT,
    "146": Transform.TEXT,
    "501": Transform.ADDITION,
    "502": Transform.ADDITION,
    "503": Transform.ADDITION,
    "504": Transform.ADDITION,
}
