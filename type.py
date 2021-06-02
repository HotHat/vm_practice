from enum import Enum


class VarType(Enum):
    NIL = 1
    INTEGER = 2
    FLOAT = 3
    STRING = 4
    CLOSURE = 5


class ConstType(Enum):
    INTEGER = 1
    FLOAT = 2
    STRING = 3
