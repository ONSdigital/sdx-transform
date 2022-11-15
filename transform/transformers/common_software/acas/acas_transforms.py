from enum import Enum


class Transform(Enum):
    VALUE = 1
    CURRENCY = 2
    TEXT_FIELD = 3
    RADIO = 4
    COMMENT = 6


# The following dictionary defines the transformations to perform.
# The key is the qcode, the value is a list describing the transform
# and any arguments to pass.

transformations = {}
