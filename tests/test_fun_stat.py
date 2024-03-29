import unittest
from ast import *
from lua_function import FuncStat
from generate import *


class TestFunStat(unittest.TestCase):

    @staticmethod
    def run_stmt(stmt):
        stmt = Stmt(stmt)
        blk = Block(Chunk([stmt]))
        fun_stat = FuncStat(blk)
        fun_stat.generate_opcode()
        fun_stat.print()

    def test_assign(self):
        name_list = NameList(TermName("var1"))
        exp_list = ExprList(Expr(TermNumber(1234)))
        assign = LocalAssignStmt(name_list, exp_list)
        self.run_stmt(assign)

    def test_and(self):
        bp = BinOpExpr(BinOpEnum.AND,
                       Expr(TermTrue()),
                       Expr(TermFalse())
                       )
        var_list = NameList(TermName("var1"))
        exp_list = ExprList(Expr(bp))
        assign = LocalAssignStmt(var_list, exp_list)
        self.run_stmt(assign)

    def test_add(self):
        bp = BinOpExpr(BinOpEnum.ADD,
                       Expr(BinOpExpr(BinOpEnum.ADD,
                           Expr(PrefixExpr.var(Var.name(TermName('a')))),
                           Expr(PrefixExpr.var(Var.name(TermName('b')))),
                           )),
                           Expr(PrefixExpr.var(Var.name(TermName('a')))),
                       )
        var_list = NameList(TermName("var1"))
        exp_list = ExprList(Expr(bp))
        assign = LocalAssignStmt(var_list, exp_list)
        self.run_stmt(assign)

    def test_add_1(self):
        bp = BinOpExpr(BinOpEnum.ADD,
                       Expr(BinOpExpr(BinOpEnum.SUB,
                                       Expr(TermNumber(1)),
                                       Expr(TermNumber(2)))),
                       Expr(TermNumber(3)))

        var_list = NameList(TermName("var1"))
        exp_list = ExprList(Expr(bp))
        assign = LocalAssignStmt(var_list, exp_list)
        self.run_stmt(assign)




