import unittest
from symbol_table import *


class TestDot(unittest.TestCase):
    def test_table(self):
        s = BaseSymbolTable()
        s.insert('a', 123)
        s.insert('b', 456)

        s1 = BaseSymbolTable(s)
        s1.insert('c', 123)
        s1.insert('d', 456)

        # level 1
        print(s.lookup('b'))
        print(s.lookup('c'))

        # level 2
        print(s1.lookup('c'))
        print(s1.lookup('a'))
        print(s1.lookup('a0'))

    def test_const(self):
        sym = const_symbol_table()
        print(sym.lookup(''))
        print(sym.lookup('false'))
        print(sym.lookup('true'))
        print(sym.lookup('nil'))
        print(sym.lookup('123'))
        print(sym.lookup('this is string'))

    def test_symbol_table(self):
        symbol_table = SymbolTable()
        symbol_table.insert('a', Symbol('a', SymbolType.VARIABLE, VarType.STRING))
        symbol_table.insert('b', Symbol('b', SymbolType.VARIABLE, VarType.STRING))

        print(symbol_table.lookup('a'))
        print(symbol_table.lookup('b'))
        print(symbol_table.lookup('c'))
        #
        symbol_table.enter_block()
        symbol_table.enter_block()
        symbol_table.enter_block()
        symbol_table.insert('aa', Symbol('aa', SymbolType.VARIABLE, VarType.STRING))
        # symbol_table.insert('bb', Symbol('bb', SymbolType.VARIABLE, VarType.STRING))
        print(symbol_table.lookup('aa'))
        print(symbol_table.lookup('b'))
        # print(symbol_table.lookup('c'))
        symbol_table.leave_block()
        symbol_table.leave_block()
        symbol_table.leave_block()
        #
        # print(symbol_table.lookup('aa'))
        # print(symbol_table.lookup('a'))
        # # print(symbol_table.lookup('c'))



