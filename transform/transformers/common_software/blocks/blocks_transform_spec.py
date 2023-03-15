from enum import Enum


class Transform(Enum):
    NO_TRANSFORM = 1
    TEXT = 2


TRANSFORMS_SPEC = {
    "101": Transform.NO_TRANSFORM,
    "102": Transform.NO_TRANSFORM,
    "103": Transform.NO_TRANSFORM,
    "104": Transform.NO_TRANSFORM,
    "111": Transform.NO_TRANSFORM,
    "112": Transform.NO_TRANSFORM,
    "113": Transform.NO_TRANSFORM,
    "114": Transform.NO_TRANSFORM,
    "121": Transform.NO_TRANSFORM,
    "122": Transform.NO_TRANSFORM,
    "123": Transform.NO_TRANSFORM,
    "124": Transform.NO_TRANSFORM,
    "145": Transform.TEXT,
    "146": Transform.TEXT
}
