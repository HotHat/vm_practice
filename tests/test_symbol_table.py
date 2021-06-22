import unittest
from symbol_table import *


class TestDot(unittest.TestCase):
    def test_table(self):
        s = SymbolTable()
        s.insert('1_a', 1)
        s.insert('1_b', 2)

        s1 = SymbolTable(s)
        s1.insert('2_c', 3)
        s1.insert('2_d', 4)

        # level 1
        print(s.lookup('1_b'))
        print(s.lookup('1_c'))

        # level 2
        print(s1.lookup('2_c'))
        # print(s1.lookup('a'))
        # print(s1.lookup('b'))
        # print(s1.lookup('a0'))
        # level 3
        s2 = SymbolTable(s1)
        s2.insert('3_e', 3)
        s2.insert('3_f', 4)

        print('------level 3---------')
        print(s2.lookup('3_f'))
        print(s2.lookup('2_c'))
        print(s2.lookup('1_b'))
        print(s2.lookup('1_2'))



    def test_symbol_table(self):
        symbol_table = SymbolTableStack()
        symbol_table.insert(Symbol('a'))
        symbol_table.insert(Symbol('b'))

        print(symbol_table.lookup(Symbol('a')))
        print(symbol_table.lookup(Symbol('b')))
        print(symbol_table.lookup(Symbol('c')))
        #
        symbol_table.enter_block()
        symbol_table.enter_block()
        symbol_table.enter_block()
        symbol_table.insert(Symbol('aa'))
        # symbol_table.insert('bb', Symbol('bb', SymbolType.VARIABLE, VarType.STRING))
        print(symbol_table.lookup(Symbol('aa')))
        print(symbol_table.lookup(Symbol('b')))
        # print(symbol_table.lookup('c'))
        symbol_table.leave_block()
        symbol_table.leave_block()
        symbol_table.leave_block()
        #
        # print(symbol_table.lookup('aa'))
        # print(symbol_table.lookup('a'))
        # # print(symbol_table.lookup('c'))

    def test_temporary_var(self):
        tb1 = SymbolTable()
        tb1.insert(Symbol('a'))
        tb1.insert(Symbol('b'))
        tb1.add_temp_var()
        tb1.add_temp_var()
        tb1.print()
        print('------------------------------')
        tb2 = SymbolTable()
        tb2.insert(Symbol('a'))
        tb2.insert(Symbol('b'))
        tb2.add_temp_var()
        tb2.add_temp_var()
        tb2.insert(Symbol('c'))
        tb2.print()






