from symbol_type import *
from typing import Union


class Symbol:
    def __init__(self, symbol: str, symbol_type: SymbolType, detail_type: VarType):
        self.symbol = symbol
        self.symbol_type = symbol_type
        self.detail_type = detail_type


class LookupResult:
    def __init__(self, level: int, idx: int, sym: Symbol, is_top=False):
        self.level = level
        self.index = idx
        self.symbol = sym
        self.is_top = is_top

    def __str__(self):
        return f"{{level: {self.level}, index: {self.index}, " \
               f"symbol: {{symbol:{self.symbol.symbol}, " \
               f"type: {self.symbol.symbol_type}, detail:{self.symbol.detail_type}," \
               f"is_top: {self.is_top}}}}}"


class BaseSymbolTable:
    def __init__(self, parent: 'BaseSymbolTable' = None):
        self.parent = parent
        self.var_list = []
        self.table = {}

    def insert(self, symbol, value: Symbol):
        f = self.lookup(symbol)
        if f is None:
            self.var_list.append(symbol)
            self.table[symbol] = value
            # if f.symbol_type == value.symbol_type and \
            #         f.detail_type == value.detail_type:
            #     return
        else:
            raise Exception(f"{symbol} duplicate definite")

    def lookup(self, symbol) -> Union[LookupResult, None]:
        if symbol in self.table:
            return LookupResult(0, self.var_list.index(symbol), self.table[symbol], self.parent is None)
        return None
        # parent = self.parent
        # level = 1
        # while parent:
        #     result = parent.lookup(symbol)
        #     if result:
        #         return LookupResult(level, result.index, result.symbol)
        #     level += 1
        #     parent = parent.parent
        # return None


class SymbolTable:
    def __init__(self):
        self.parent = None
        self.current = BaseSymbolTable()

    def enter_block(self):
        self.parent = self.current
        self.current = BaseSymbolTable(self.parent)

    def leave_block(self):
        if self.parent is not None:
            self.current = self.parent
            self.parent = self.parent.parent

    def insert(self, symbol, value: Symbol):
        self.current.insert(symbol, value)

    def lookup(self, symbol) -> Union[LookupResult, None]:
        cur = self.current
        level = 0
        while cur:
            result = cur.lookup(symbol)
            if result:
                result.level = level
                return result
            level += 1
            cur = cur.parent
        return None

    # def get_index(self, symbol):
    #     return self.current.get_index(symbol)


class SymbolTableManager:
    __instance = None

    @staticmethod
    def get_instance() -> 'SymbolTableManager':
        if SymbolTableManager.__instance is None:
            SymbolTableManager.__instance = SymbolTableManager()
        return SymbolTableManager.__instance


def const_symbol_table():
    sym = BaseSymbolTable()
    sym.insert('nil', Symbol('nil', SymbolType.CONSTANT, VarType.NIL))
    sym.insert('true', Symbol('true', SymbolType.CONSTANT, VarType.BOOL))
    sym.insert('false', Symbol('false', SymbolType.CONSTANT, VarType.BOOL))
    sym.insert('', Symbol('', SymbolType.CONSTANT, VarType.STRING))
    return sym

