
import unittest
from ast import *


class TestAst(unittest.TestCase):
    def test_constant(self):
        c1 = NIL
        c2 = string('string const')
        c3 = number(1234)
        c4 = TRUE
        c5 = FALSE

        print(c1)
        print(c2)
        print(c3)
        print(c4)
        print(c5)

    def test_assign(self):
        s = AssignStmt([Name('a'), Name('b')], ExprList(Expr(TRUE), Expr(FALSE)), True)

    def test_binop_const(self):

        binop = BinOpExpr(BinOpExpr.ADD, string('abc'), FALSE)

        binop2 = BinOpExpr(BinOpExpr.SUB, binop, TRUE)

        print(binop2)

    def test_binop_var(self):
        l = Expr(prefix_name('abc'))
        r = Expr(prefix_bracket(prefix_name('table'), number(10)))

        r2 = Expr(prefix_dot(prefix_name('class'), Name('func')))

        b = BinOpExpr(BinOpExpr.ADD, l, r)
        b2 = BinOpExpr(BinOpExpr.SUB, b, r2)


if __name__ == '__main__':
    unittest.main()
