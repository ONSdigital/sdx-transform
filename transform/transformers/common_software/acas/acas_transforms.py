from enum import Enum


class TransformType(Enum):
    DATE = 1
    CURRENCY = 2
    TEXT_FIELD = 3
    NUMBER = 4


# The following dictionary defines the transformations to perform.
# The key is the qcode, the value is a list describing the transform
# and any arguments to pass.

transformations = {
}
