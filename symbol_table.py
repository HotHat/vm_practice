from symbol_type import *
from typing import Union
from temp_var import TempVar


class Symbol:
    def __init__(self, symbol: str, is_temp: bool = False):
        self.symbol = symbol
        self.is_temp = is_temp


def temp_symbol():
    return Symbol(TempVar.instance().new(), True)


class LookupResult:
    def __init__(self, level: int, idx: int, sym: Symbol, is_top=False):
        self.level = level
        self.index = idx
        self.symbol = sym
        self.is_top = is_top

    def __str__(self):
        return f"{{level: {self.level}, index: {self.index}, " \
               f"symbol: {{symbol:{self.symbol.symbol}, is_temp:{self.symbol.is_temp}}}" \
               f"is_top: {self.is_top}}}"


class SymbolTable:
    def __init__(self, parent: 'SymbolTable' = None):
        self.parent = parent
        self.var_list = []

    def insert(self, symbol: Symbol):
        f = self.lookup(symbol)
        if f is None:
            # pop temporary variable
            while 0 != len(self.var_list) and self.var_list[len(self.var_list)-1].is_temp:
                self.var_list.pop()
            self.var_list.append(symbol)
        else:
            pass
            # raise Exception(f"{symbol} duplicate definite")

    def add_temp_var(self):
        self.var_list.append(temp_symbol())
        return len(self.var_list) - 1

    def lookup(self, symbol) -> Union[LookupResult, None]:
        for idx, sym in enumerate(self.var_list):
            if symbol.symbol == sym.symbol:
                return LookupResult(0, idx, sym, self.parent is None)
        return None

    def print(self):
        for sym in self.var_list:
            print(f"symbol: {{symbol:{sym.symbol}, is_temp:{sym.is_temp}}}")


class SymbolTableStack:
    def __init__(self):
        self.parent = None
        self.current = SymbolTable()

    def enter_block(self):
        self.parent = self.current
        self.current = SymbolTable(self.parent)

    def leave_block(self):
        if self.parent is not None:
            self.current = self.parent
            self.parent = self.parent.parent

    def insert(self, symbol):
        self.current.insert(symbol)

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

