import unittest
from ast import *
from generate import *


class TestGenerate(unittest.TestCase):
    def test_binop(self):
        bp = BinOpExpr(BinOpEnum.ADD, Expr(BinOpExpr(BinOpEnum.ADD, number(3), number(4))), number(5))
        opcode = generate_binary_expr(bp)
        print(opcode)

    def test_assign(self):
        var_list = VarList(Var.name(TermName("var1")))
        exp_list = ExprList(Expr(TermNil()))
        assign = AssignStmt(var_list, exp_list)
        opcode = generate_assign(assign)
        print(opcode)
