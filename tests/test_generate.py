import unittest
from ast import *
from lua_function import FuncStat
from generate import *


class TestGenerate(unittest.TestCase):
    def test_binop(self):
        bp = BinOpExpr(BinOpEnum.ADD, Expr(BinOpExpr(BinOpEnum.ADD, number(3), number(4))), number(5))
        opcode = generate_binary_expr(bp)
        print(opcode)
        print(FuncStat.instance().print())

    def test_const(self):
        opcode = generate_const(TermNumber("123456"))
        print(opcode)
        print(FuncStat.instance().print())

    def test_assign(self):
        var_list = NameList(Var.name(TermName("var1")))
        exp_list = ExprList(Expr(TermNumber(123)))
        assign = LocalAssignStmt(var_list, exp_list)
        generate_local_assign(assign)

        var_list = VarList(Var.name(TermName("var2")))
        exp_list = ExprList(Expr(TermNumber(456)))
        assign = LocalAssignStmt(var_list, exp_list)
        generate_local_assign(assign)
        print(FuncStat.instance().print())

    def test_local_assign_binary(self):
        # local var1 = 3+4+5
        bp = BinOpExpr(BinOpEnum.ADD, Expr(BinOpExpr(BinOpEnum.ADD, number(3), number(4))), number(5))
        var_list = NameList(TermName("var1"))
        exp_list = ExprList(Expr(bp))
        assign = LocalAssignStmt(var_list, exp_list)
        generate_local_assign(assign)
        print(FuncStat.instance().print())

    def test_and(self):
        bp = BinOpExpr(BinOpEnum.AND,
                       Expr(TermFalse()),
                       Expr(BinOpExpr(BinOpEnum.AND, Expr(TermTrue()), Expr(TermFalse())))
                       )
        generate_login_and_expr(bp)
        FuncStat.instance().print()

    def test_or(self):
        bp = BinOpExpr(BinOpEnum.AND, Expr(TermTrue()), Expr(TermFalse()))
        # bp = BinOpExpr(BinOpEnum.OR,
        #                Expr(BinOpExpr(BinOpEnum.AND, Expr(TermTrue()), Expr(TermFalse()))),
        #                Expr(TermFalse()))
        generate_login_or_expr(bp)
        FuncStat.instance().print()

    def test_and_or(self):
        bp = BinOpExpr(BinOpEnum.AND,
                       Expr(BinOpExpr(BinOpEnum.OR, Expr(TermTrue()), Expr(TermFalse()))),
                       Expr(TermFalse()))
        generate_login_and_expr(bp)
        FuncStat.instance().print()


