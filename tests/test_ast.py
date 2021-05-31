import unittest
from ast import *
from graphviz import Source


class TestAst(unittest.TestCase):
    def setUp(self) -> None:
        self.source = Source

    def test_constant(self):
        c1 = TermNil()
        c2 = TermString('it is string')
        c3 = TermNumber(1234)
        c4 = TermTrue()
        c5 = TermFalse()
        c6 = TermEllipsis()

        print(c1)
        print(c2)
        print(c3)
        print(c4)
        print(c5)
        print(c6)

    def test_assign(self):
        pass

    def test_binop_const(self):
        bp = BinOpExpr(BinOpEnum.ADD, number(6), number(5))
        print(bp)

    def test_exp_list(self):
        b1 = Expr(BinOpExpr(BinOpEnum.ADD, number(1), number(2)))
        # self.assertEqual(1, 2)
        b2 = Expr(BinOpExpr(BinOpEnum.ADD, number(3), number(4)))
        pl = ExprList(b1, b2)
        s = pl.__str__()
        print(s)

    def test_function_name(self):
        fn = FunctionName(TermName("dog"))
        print(fn)

        fn1 = FunctionName(TermName("dog"), [TermName("run"), TermName("jump")])
        print(fn1)

        fn2 = FunctionName(TermName("dog"), [TermName("run"), TermName("jump")], TermName("eat"))
        print(fn2)

    def test_var(self):
        v1 = Var.name(TermName("var_name"))
        v2 = Var.bracket(prefix_name("var"), Expr(TermNumber(5)))
        v3 = Var.dot(prefix_name("dog"), TermName("run"))
        print(v1)
        print('------------------')
        print(v2)
        print('------------------')
        print(v3)

    def pp(self, s, is_source=False):
        s = f"digraph G {{{s}}}"
        if is_source:
            print(s)
        else:
            Source(s, filename="test.gv", format="png").view()

    def test_var_list(self):
        v1 = Var.name(TermName("var_name"))
        v2 = Var.bracket(prefix_name("var"), Expr(TermNumber(5)))
        v3 = Var.dot(prefix_name("dog"), TermName("run"))
        vl = VarList(v1, v2, v3)
        print(vl)

    def test_name_list(self):
        n1 = TermName("name1")
        n2 = TermName("name2")
        n3 = TermName('name3')
        nl = NameList(n1, n2, n3)
        print(nl)

    def test_function_call(self):
        pe = prefix_name("function_name")
        args = Args.params(ExprList(Expr(Var.name(TermName("argv1"))),
                                    Expr(Var.name(TermName("argv2"))),
                                    Expr(Var.name(TermName("argv3")))))
        opn = TermName("option_name")
        fc = FunctionCallStmt(pe, opn, args)

        self.pp(fc)

    def test_function_expr(self):
        pe = prefix_name("function_name")
        args = Args.params(ExprList(Expr(Var.name(TermName("argv1"))),
                                    Expr(Var.name(TermName("argv2"))),
                                    Expr(Var.name(TermName("argv3")))))
        opn = TermName("option_name")
        fc = FunctionCallStmt(pe, opn, args)

        fn = FunctionExpr(ParList.name(NameList(TermName("args1"), TermName("args2"))), Block(Chunk([Stmt(fc)])))

        self.pp(fn)

    def test_block(self):
        pe = prefix_name("function_name")
        args = Args.params(ExprList(Expr(Var.name(TermName("argv1"))),
                                    Expr(Var.name(TermName("argv2")))))
        opn = TermName("option_name")
        fc = FunctionCallStmt(pe, opn, args)

        pe2 = prefix_name("function_name")
        args2 = Args.params(ExprList(Expr(Var.name(TermName("argv1"))),
                                     Expr(Var.name(TermName("argv2")))))
        opn2 = TermName("option_name")
        fc2 = FunctionCallStmt(pe2, opn2, args2)

        # self.pp(fc, True)
        block = Block(Chunk([Stmt(fc), Stmt(fc2)]))
        # self.pp(block, True)
        self.pp(block)

    def test_var_one(self):
        var_list = VarList(Var.name(TermName("var1")))
        exp_list = ExprList(Expr(TermNil()))
        a = AssignStmt(var_list, exp_list)
        self.pp(a)

    def test_var_more(self):
        var_list = VarList(Var.name(TermName("var1")), Var.name(TermName("var2")), Var.name(TermName("var3")))
        exp_list = ExprList(Expr(TermNil()), Expr(TermNumber(123)), Expr(TermNumber(456)))
        a = AssignStmt(var_list, exp_list)
        self.pp(a)

    def test_if_without_elseif_else(self):
        conf = Expr(TermTrue())
        var_list = VarList(Var.name(TermName("var1")))
        exp_list = ExprList(Expr(TermNil()))
        assign = AssignStmt(var_list, exp_list)
        block = Block(Chunk([Stmt(assign)]))
        if_stmt = IfStmt(conf, block, None, None)
        self.pp(if_stmt)

    def test_if_without_else(self):
        conf = Expr(TermTrue())
        var_list = VarList(Var.name(TermName("var1")))
        exp_list = ExprList(Expr(TermNil()))
        assign = AssignStmt(var_list, exp_list)
        block = Block(Chunk([Stmt(assign)]))

        var_list2 = VarList(Var.name(TermName("var2")))
        exp_list2 = ExprList(Expr(TermNil()))
        assign2 = AssignStmt(var_list2, exp_list2)
        block2 = Block(Chunk([Stmt(assign2)]))
        conf2 = Expr(TermTrue())
        else_if_stmt = ElifStmt(conf2, block2)

        if_stmt = IfStmt(conf, block, [else_if_stmt], None)

        self.pp(if_stmt)
        # self.pp(if_stmt, True)

    def test_if_full(self):
        conf = Expr(TermTrue())
        var_list = VarList(Var.name(TermName("var1")))
        exp_list = ExprList(Expr(TermNil()))
        assign = AssignStmt(var_list, exp_list)
        block = Block(Chunk([Stmt(assign)]))

        var_list2 = VarList(Var.name(TermName("var2")))
        exp_list2 = ExprList(Expr(TermNil()))
        assign2 = AssignStmt(var_list2, exp_list2)
        block2 = Block(Chunk([Stmt(assign2)]))
        conf2 = Expr(TermTrue())
        else_if_stmt = ElifStmt(conf2, block2)

        var_list3 = VarList(Var.name(TermName("var3")))
        exp_list3 = ExprList(Expr(TermNil()))
        assign3 = AssignStmt(var_list3, exp_list3)
        block3 = Block(Chunk([Stmt(assign3)]))

        if_stmt = IfStmt(conf, block, [else_if_stmt], block3)

        self.pp(if_stmt)
        # self.pp(if_stmt, True)


if __name__ == '__main__':
    unittest.main()
