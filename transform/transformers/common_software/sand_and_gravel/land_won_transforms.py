from enum import Enum


class Transform(Enum):
    UNIT = 1
    TEXT = 2


TRANSFORMS_SPEC = {
    "601": Transform.UNIT,
    "602": Transform.UNIT,
    "603": Transform.UNIT,
    "604": Transform.UNIT,
    "605": Transform.UNIT,
    "606": Transform.UNIT,
    "607": Transform.UNIT,
    "146": Transform.TEXT,
    "147": Transform.TEXT,
}

ADDITION_QCODES = {
    "608": ["601", "602", "603", "604", "605", "606", "607"]
}
