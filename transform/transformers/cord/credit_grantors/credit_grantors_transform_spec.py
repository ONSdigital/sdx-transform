from enum import Enum


class Transform(Enum):
    NO_TRANSFORM = 1
    TEXT = 2


TRANSFORMS_SPEC = {
    "9001": Transform.NO_TRANSFORM,
    "9003": Transform.NO_TRANSFORM,
    "9005": Transform.NO_TRANSFORM,
    "9007": Transform.NO_TRANSFORM,
    "9008": Transform.NO_TRANSFORM,
    "9010": Transform.NO_TRANSFORM,
    "9012": Transform.NO_TRANSFORM,
    "9014": Transform.NO_TRANSFORM,
    "9002": Transform.NO_TRANSFORM,
    "9004": Transform.NO_TRANSFORM,
    "9006": Transform.NO_TRANSFORM,
    "9009": Transform.NO_TRANSFORM,
    "9016": Transform.NO_TRANSFORM,
    "9011": Transform.NO_TRANSFORM,
    "9013": Transform.NO_TRANSFORM,
    "9015": Transform.NO_TRANSFORM
}
