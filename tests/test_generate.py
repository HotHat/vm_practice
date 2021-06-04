import unittest
from ast import *
from generate import *


class TestGenerate(unittest.TestCase):
    def test_binop(self):
        bp = BinOpExpr(BinOpEnum.ADD, Expr(BinOpExpr(BinOpEnum.ADD, number(3), number(4))), number(5))
        opcode = generate_binary_expr(bp)
        print(opcode)
