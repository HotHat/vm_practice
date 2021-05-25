
import unittest
from ast import *


class TestAst(unittest.TestCase):
    def test_constant(self):
        c1 = gen_const_nil()
        c2 = gen_const_string('string const')
        c3 = gen_const_number(1234)
        c4 = gen_const_true()
        c5 = gen_const_false()

        print(c1)
        print(c2)
        print(c3)
        print(c4)
        print(c5)

    def test_binop(self):
        left = gen_expr_const(gen_const_true())
        right = gen_expr_const(gen_const_false())

        binop = gen_expr_binop(BinOp.ADD, left, right)

        binop2 = gen_expr_binop(BinOp.SUB, binop, right)

        print(binop2)


if __name__ == '__main__':
    unittest.main()
