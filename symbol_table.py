from symbol_type import *
from typing import Union
from temp_var import TempVar


class Symbol:
    def __init__(self, name: str, attribute, is_temp: bool = False):
        self.name = name
        self.attribute = attribute
        self.is_temp = is_temp


def temp_symbol():
    return Symbol(TempVar.instance().new(), 'register', True)


class LookupResult:
    def __init__(self, level: int, idx: int, sym: Symbol):
        self.level = level
        self.index = idx
        self.symbol = sym

    def __str__(self):
        return f"{{level: {self.level}, index: {self.index}, " \
               f"symbol: {{symbol:{self.symbol.name}, is_temp:{self.symbol.is_temp}}}" \
               "}}"


class SymbolTable:
    def __init__(self, parent: 'SymbolTable' = None):
        self.parent = parent
        self.var_list = []

    def insert(self, name: str, attribute):
        idx = self._lookup_current_level(name)
        # current table without this symbol
        if -1 == idx:
            # pop temporary variable
            while 0 != len(self.var_list) and self.var_list[len(self.var_list)-1].is_temp:
                self.var_list.pop()
            self.var_list.append(Symbol(name, attribute))
            return len(self.var_list) - 1
        else:
            return idx
            # raise Exception(f"{symbol} duplicate definite")

    def add_temp_var(self):
        self.var_list.append(temp_symbol())
        return len(self.var_list) - 1

    def pop_temp_var(self):
        if self.var_list[-1].is_temp:
            self.var_list.pop()

    def _lookup_current_level(self, name):
        for idx, sym in enumerate(self.var_list):
            if name == sym.symbol:
                return idx
        return -1

    def lookup(self, symbol: str, level=0) -> LookupResult:
        result = None
        for idx, sym in enumerate(self.var_list):
            if symbol == sym.name:
                if self.parent is None:
                    level = -1
                result = LookupResult(level, idx, sym)

        # current level not find
        if result is None:
            # in parent level
            if self.parent is not None:
                result = self.parent.lookup(symbol, level + 1)
            else:
                result = LookupResult(-1, -1, Symbol('', ''))

        return result

    def print(self):
        for sym in self.var_list:
            print(f"symbol: {{symbol:{sym.name}, attribute: {sym.attribute}, is_temp:{sym.is_temp}}}")


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

