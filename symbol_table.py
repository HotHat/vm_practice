from symbol_type import *
from typing import Union


class SymbolTable:
    def __init__(self, parent: 'SymbolTable' = None):
        self.parent = parent
        self.table = {}

    def insert(self, symbol, value: Symbol):
        f = self.lookup(symbol)
        if f is not None:
            if f.symbol_type == value.symbol_type and \
                    f.detail_type == value.detail_type:
                return

        self.table[symbol] = value

    def lookup(self, symbol) -> Union[Symbol, None]:
        if symbol in self.table:
            return self.table[symbol]
        if self.parent:
            return self.parent.lookup(symbol)
        return None


def const_symbol_table():
    sym = SymbolTable()
    sym.insert('nil', Symbol('nil', SymbolType.CONSTANT, ConstType.NIL))
    sym.insert('true', Symbol('true', SymbolType.CONSTANT, ConstType.BOOL))
    sym.insert('false', Symbol('false', SymbolType.CONSTANT, ConstType.BOOL))
    sym.insert('', Symbol('', SymbolType.CONSTANT, ConstType.STRING))
    return sym

# class ComponentSymbolTable:
#     def __init__(self, parent: 'ComponentSymbolTable' = None):
#         self.parent = parent
#         # constant symbol table
#         self.const_table = {}
#         # variable symbol table
#         self.var_table = {}
#
#     def insert_const(self, symbol, value):
#         self.const_table[symbol] = value
#
#     def insert_var(self, symbol, value):
#         self.var_table[symbol] = value
#
#     def lookup_const(self, symbol):
#         if symbol in self.const_table:
#             return self.const_table[symbol]
#         if self.parent:
#             return self.parent.lookup_const(symbol)
#         return None
#
#     def lookup_var(self, symbol):
#         if symbol in self.var_table:
#             return self.var_table[symbol]
#         if self.parent:
#             return self.parent.lookup_var(symbol)
#         return None
