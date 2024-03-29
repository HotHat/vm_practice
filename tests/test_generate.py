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
        FuncStat.instance().print()

    def test_and(self):
        bp = BinOpExpr(BinOpEnum.AND,
                       Expr(TermFalse()),
                       Expr(TermFalse())
                       # Expr(BinOpExpr(BinOpEnum.AND, Expr(TermTrue()), Expr(TermFalse())))
                       )
        generate_login_and_expr(bp)
        FuncStat.instance().print()

    def test_local_assign_and(self):
        # local var1 = false and true
        bp = BinOpExpr(BinOpEnum.AND,
                       Expr(TermFalse()),
                       # Expr(TermTrue())
                       Expr(BinOpExpr(BinOpEnum.AND, Expr(TermTrue()), Expr(TermFalse())))
                       )
        var_list = NameList(TermName("var1"))
        exp_list = ExprList(Expr(bp))
        assign = LocalAssignStmt(var_list, exp_list)
        generate_local_assign(assign)
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

    def test_if(self):
        cond = Expr(TermTrue())
        var_list = NameList(TermName("name"))
        exp_list = ExprList(Expr(TermTrue()))
        assign = LocalAssignStmt(var_list, exp_list)
        block = Block(Chunk([Stmt(assign)]))
        if_stmt = IfStmt(cond, block, None, None)
        generate_if_expr(if_stmt)
        FuncStat.instance().print()

    def test_if_else(self):
        cond = Expr(TermTrue())
        var_list = NameList(TermName("var_block"))
        exp_list = ExprList(Expr(TermTrue()))
        assign = LocalAssignStmt(var_list, exp_list)
        # then block
        block = Block(Chunk([Stmt(assign)]))

        var2_list = NameList(TermName("else_block"))
        exp2_list = ExprList(Expr(TermFalse()))
        assign2 = LocalAssignStmt(var2_list, exp2_list)
        # else block
        block2 = Block(Chunk([Stmt(assign2)]))
        
        if_stmt = IfStmt(cond, block, None, block2)
        generate_if_expr(if_stmt)
        FuncStat.instance().print()

    def test_if_elif(self):
        cond = Expr(TermTrue())
        var_list = NameList(TermName("then_block"))
        exp_list = ExprList(Expr(TermTrue()))
        assign = LocalAssignStmt(var_list, exp_list)
        # then block
        block = Block(Chunk([Stmt(assign)]))

        elif_cond = Expr(TermTrue())
        elif_var_list = NameList(TermName("then_block"))
        elif_exp_list = ExprList(Expr(TermTrue()))
        elif_assign = LocalAssignStmt(elif_var_list, elif_exp_list)

        # else block
        elif_block = Block(Chunk([Stmt(elif_assign)]))
        elif_block = ElifStmt(elif_cond, elif_block)

        # else block2
        elif_cond2 = Expr(TermTrue())
        elif_var_list2 = NameList(TermName("then_block2"))
        elif_exp_list2 = ExprList(Expr(TermTrue()))
        elif_assign2 = LocalAssignStmt(elif_var_list2, elif_exp_list2)

        # else block
        elif_block2 = Block(Chunk([Stmt(elif_assign2)]))
        elif_block2 = ElifStmt(elif_cond2, elif_block2)

        if_stmt = IfStmt(cond, block, [elif_block, elif_block2], None)
        generate_if_expr(if_stmt)
        FuncStat.instance().print()

