from enum import Enum


class VarType(Enum):
    NIL = 1
    BOOL = 2
    INTEGER = 3
    FLOAT = 4
    STRING = 5
    CLOSURE = 6


class ConstType(Enum):
    NIL = 1
    BOOL = 2
    INTEGER = 3
    FLOAT = 4
    STRING = 5


class SymbolType(Enum):
    CONSTANT = 1
    VARIABLE = 2
    CLOSURE = 3


class Symbol:
    def __init__(self, symbol, symbol_type, detail_type):
        self.symbol = symbol
        self.symbol_type = symbol_type
        self.detail_type = detail_type

