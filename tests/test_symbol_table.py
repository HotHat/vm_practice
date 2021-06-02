import unittest
from symbol_table import *


class TestDot(unittest.TestCase):
    def test_table(self):
        s = SymbolTable()
        s.insert('a', 123)
        s.insert('b', 456)

        s1 = SymbolTable(s)
        s1.insert('c', 123)
        s1.insert('d', 456)

        # level 1
        print(s.lookup('b'))
        print(s.lookup('c'))

        # level 2
        print(s1.lookup('c'))
        print(s1.lookup('a'))
        print(s1.lookup('a0'))
