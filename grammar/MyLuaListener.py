from grammar.LuaListener import LuaListener, TerminalNode
from grammar.LuaParser import LuaParser
from ast import *


class MyLuaListener(LuaListener):
    def __init__(self):
        self.chuck = None
        self.block_stack = []
        self.stat_stack = []
        self.ret_stat = None
        self.prefix_expr_stack = []
        self.prefix_stack = []
        self.function_call_stack = []
        self.args = None
        self.name_and_args = []
        self.name = None
        # self.var = None
        self.namelist_stack = []
        self.exprlist_stack = []
        self.exprlist = []
        self.varlist = []
        self.expr = None
        self.table_constructor = None
        self.parlist = []
        self.func_body_stack = []
        self.field_stack = []

    def get_chuck(self):
        return self.chuck

    # Enter a parse tree produced by LuaParser#chunk.
    def enterChunk(self, ctx: LuaParser.ChunkContext):
        pass

    # Exit a parse tree produced by LuaParser#chunk.
    def exitChunk(self, ctx: LuaParser.ChunkContext):
        self.chuck = Chunk(self.block_stack.pop())

    # Enter a parse tree produced by LuaParser#block.
    def enterBlock(self, ctx: LuaParser.BlockContext):
        # self.stat_stack.append([])
        print('----enter block-----')
        pass

    # Exit a parse tree produced by LuaParser#block.
    def exitBlock(self, ctx: LuaParser.BlockContext):
        print('----exit block---')
        stat = []
        ret = None
        if ctx.stat():
            for _ in ctx.stat():
                stat.append(self.stat_stack.pop())
        if ctx.retstat():
            ret = self.ret_stat.pop()

        stat.reverse()
        block = Block(stat, ret)
        self.block_stack.append(block)

    # Enter a parse tree produced by LuaParser#stat_stack.
    def enterStat(self, ctx: LuaParser.StatContext):
        self.exprlist_stack.append([])
        self.varlist.append([])
        self.parlist.append([])

    # Exit a parse tree produced by LuaParser#stat_stack.
    def exitStat(self, ctx: LuaParser.StatContext):
        print([i for i in ctx.getChildren()])
        cur_stat = self.stat_stack
        if ctx.getChildCount() == 0:
            return

        if ctx.label():
            cur_stat.append(Stmt(Label(TermName(ctx.label().NAME().getText()))))
        elif ctx.getText() == 'break':
            cur_stat.append(Stmt(Break()))
        elif ctx.getChild(0).getText() == 'goto':
            cur_stat.append(Stmt(Goto(TermName(ctx.getChild(1).getText()))))
        elif ctx.getChild(0).getText() == 'do':
            block = self.block_stack.pop()
            cur_stat.append(Stmt(DoStmt(block)))
        elif ctx.getChild(0).getText() == 'while':
            block = self.block_stack.pop()
            expr = self.exprlist_stack[-1].pop()
            cur_stat.append(Stmt(WhileStmt(expr, block)))
        elif ctx.getChild(0).getText() == 'repeat':
            expr = self.exprlist_stack[-1].pop()
            block = self.block_stack.pop()
            cur_stat.append(Stmt(RepeatStmt(block, expr)))
        elif ctx.getChild(0).getText() == 'if':
            print('------exit if--------')
            # print(self.exprlist_stack)
            # print(self.block_stack)
            elseif_count = else_count = 0
            for i in ctx.getChildren():
                if i.getText() == 'elseif':
                    elseif_count += 1
                elif i.getText() == 'else':
                    else_count += 1
            consume_block_count = 1 + elseif_count + else_count
            consume_expr_count = 1 + elseif_count

            block_list = self.block_stack[-consume_block_count:]
            expr_list = self.exprlist_stack[-1]
            print('some count:', elseif_count, else_count, len(block_list))
            elseif_stmt = []
            if elseif_count > 0:
                elseif_expr = expr_list[1:]
                elseif_block = block_list[1: 1 + len(elseif_expr)]
                for idx, _ in enumerate(elseif_expr):
                    elseif_stmt.append(ElifStmt(elseif_expr[idx], elseif_block[idx]))

            if else_count == 1:
                else_stmt = block_list[-1]
            else:
                else_stmt = None
            if_stmt = IfStmt(expr_list[0],
                             block_list[0],
                             None if len(elseif_stmt) == 0 else elseif_stmt,
                             else_stmt)

            cur_stat.append(Stmt(if_stmt))
            # pop consume block
            for i in range(consume_block_count):
                self.block_stack.pop()
            # pop consume expr
            for i in range(consume_expr_count):
                self.exprlist_stack[-1].pop()

        elif ctx.getChild(0).getText() == 'for':
            expr_list = self.exprlist_stack[-1]
            # for
            if ctx.NAME():
                name = TermName(ctx.getChild(1).getText())
                expr_count = len([i for i in ctx.exp()])
                assign = None
                cond = None
                nxt = None
                if expr_count == 3:
                    nxt = expr_list[-1]
                    cond = expr_list[-2]
                    assign = expr_list[-3]
                else:
                    cond = expr_list[-1]
                    assign = expr_list[-2]

                block = self.block_stack[-1]
                cur_stat.append(Stmt(ForStmt(name, assign, cond, nxt, block)))
                self.block_stack.pop()
                for i in range(expr_count):
                    expr_list.pop()

            else:
                # foreach
                name_list = [TermName(i.getText()) for i in ctx.namelist().NAME()]
                expr_list = self.exprlist_stack[-1]
                cur_stat.append(Stmt(ForeachStmt(NameList(*name_list), ExprList(*expr_list), self.block_stack.pop())))
                # self.block_stack.pop()
            pass
        elif ctx.getChild(0).getText() == 'function':
            name_list = [TermName(i.getText()) for i in ctx.funcname().NAME()]
            colon_name = False
            for i in ctx.funcname().getChildren():
                if i.getText() == ':':
                    colon_name = True
            opt_colon_name = None
            opt_name = []
            if colon_name:
                opt_colon_name = name_list[-1]
                if len(name_list) > 2:
                    opt_name = name_list[1:-2]
            else:
                if len(name_list) > 2:
                    opt_name = name_list[1:]
            func_name = FunctionName(name_list[0], opt_name, opt_colon_name)

            func_body = self.func_body_stack.pop()
            cur_stat.append(Stmt(FunctionStmt(func_name, func_body['args'], func_body['body'])))

        elif ctx.getChild(0).getText() == 'local':
            print('---local assign---')
            if ctx.namelist() is not None:
                name_list = [TermName(i.getText()) for i in ctx.namelist().NAME()]
                cur_stat.append(Stmt(LocalAssignStmt(NameList(*name_list), ExprList(*self.exprlist_stack[-1]))))
                self.namelist_stack = []
            else:
                print('-----exit local function------')
                name = TermName(ctx.getChild(2).getText())
                func_body = self.func_body_stack.pop()
                cur_stat.append(Stmt(LocalFunctionStmt(name, func_body['args'], func_body['body'])))
                pass
        elif ctx.functioncall() is not None:
            print('---function call ---')
            cur_stat.append(Stmt(self.function_call_stack.pop()))
        else:
            # varlist = explist
            cur_stat.append(Stmt(AssignStmt(VarList(*self.varlist[-1]), ExprList(*self.exprlist_stack[-1]))))

        # clean
        self.exprlist_stack.pop()
        self.varlist.pop()
        self.parlist.pop()
        # self.func_body_stack.pop()
        # self.function_call_stack.pop()


    # Enter a parse tree produced by LuaParser#retstat.
    def enterRetstat(self, ctx: LuaParser.RetstatContext):
        self.exprlist_stack.append([])
        self.varlist.append([])

    # Exit a parse tree produced by LuaParser#retstat.
    def exitRetstat(self, ctx: LuaParser.RetstatContext):
        self.ret_stat = ReturnStmt(ExprList(*self.exprlist_stack.pop()))
        self.varlist.pop()

    # Enter a parse tree produced by LuaParser#label.
    def enterLabel(self, ctx: LuaParser.LabelContext):
        pass

    # Exit a parse tree produced by LuaParser#label.
    def exitLabel(self, ctx: LuaParser.LabelContext):
        pass

    # Enter a parse tree produced by LuaParser#funcname.
    def enterFuncname(self, ctx: LuaParser.FuncnameContext):
        pass

    # Exit a parse tree produced by LuaParser#funcname.
    def exitFuncname(self, ctx: LuaParser.FuncnameContext):
        pass

    # Enter a parse tree produced by LuaParser#varlist.
    def enterVarlist(self, ctx: LuaParser.VarlistContext):
        pass

    # Exit a parse tree produced by LuaParser#varlist.
    def exitVarlist(self, ctx: LuaParser.VarlistContext):
        pass

    # Enter a parse tree produced by LuaParser#namelist.
    def enterNamelist(self, ctx: LuaParser.NamelistContext):
        pass

    # Exit a parse tree produced by LuaParser#namelist.
    def exitNamelist(self, ctx: LuaParser.NamelistContext):
        pass
        # for i in ctx.NAME():
        #     print(i.getText())
        #     self.namelist_stack.append(TermName(i.getText()))

    # Enter a parse tree produced by LuaParser#explist.
    def enterExplist(self, ctx: LuaParser.ExplistContext):
        # self.exprlist_stack.append([])
        pass
        # print('enter explist', ctx.getChildCount())
        # print(ctx.getChildCount())

    # Exit a parse tree produced by LuaParser#explist.
    def exitExplist(self, ctx: LuaParser.ExplistContext):
        pass
        # print('exit explist', ctx.getChildCount())
        # for expr in self.exprlist_stack:
        #     self.exprlist.append(expr)

    # Enter a parse tree produced by LuaParser#exp.
    def enterExp(self, ctx: LuaParser.ExpContext):
        # self.field_stack.append([])
        self.parlist.append([])
        pass
        # print('enter exp')

    # Exit a parse tree produced by LuaParser#exp.
    def exitExp(self, ctx: LuaParser.ExpContext):
        # print('exit exp', ctx.parentCtx, ctx.getChildCount())
        if ctx.getChild(0).getText() == 'nil':
            expr = Expr(TermNil())
        elif ctx.getChild(0).getText() == 'false':
            expr = Expr(TermFalse())
        elif ctx.getChild(0).getText() == 'true':
            expr = Expr(TermTrue())
        elif ctx.getChild(0).getText() == '...':
            expr = Expr(TermEllipsis())
        elif ctx.number() is not None:
            expr = Expr(TermNumber(ctx.getText()))
        elif ctx.string() is not None:
            expr = Expr(TermString(ctx.getText().strip('"')))
        # prefix expr
        elif ctx.prefixexp() is not None:
            expr = Expr(self.prefix_expr_stack.pop())
        # unary operation
        elif ctx.operatorUnary() is not None:
            expr = self.exprlist_stack[-1].pop()
            expr = Expr(UnOpExpr(UnOpEnum.from_symbol(ctx.operatorUnary().getText()), expr))
        # table constructor
        elif ctx.tableconstructor() is not None:
            field_list = []
            if ctx.tableconstructor().fieldlist():
                for _ in ctx.tableconstructor().fieldlist().field():
                    field_list.append(self.field_stack.pop())
            expr = Expr(TableConstructor(field_list))
        # functiondef
        elif ctx.functiondef() is not None:
            func_body = self.func_body_stack.pop()
            expr = Expr(FunctionExpr(func_body['args'], func_body['body']))
            pass
        # binary operation
        elif ctx.exp() is not None:
            # first in last out
            cur_exprlist = self.exprlist_stack[-1]
            right = cur_exprlist.pop()
            left = cur_exprlist.pop()
            expr = Expr(BinOpExpr(BinOpEnum.from_symbol(ctx.getChild(1).getText()), left, right))

        self.exprlist_stack[-1].append(expr)
        # clean
        # self.field_stack.pop()
        self.parlist.pop()

    # Enter a parse tree produced by LuaParser#prefix.
    def enterPrefix(self, ctx: LuaParser.PrefixContext):
        pass

    # Exit a parse tree produced by LuaParser#prefix.
    def exitPrefix(self, ctx: LuaParser.PrefixContext):
        pass
        # name_exp = ctx.nameOrExp()
        # if name_exp.NAME() is not None:
        #     self.prefix = prefix_name(name_exp.NAME().getText())
        # else:
        #     self.prefix = PrefixExpr.round(self.expr)
        #
        # if ctx.prefix_().getChildrenCount() != 0:
        #     if ctx.prefix_().getChild(0) == '[':
        #     elif ctx.prefix_().getChild(0) == '[':
        #     else:

        # if self.prefix_call is None:
        #     fn = PrefixExpr.var(Var.name(self.prefix_name))
        # else:
        #     fn = PrefixExpr.call(self.prefix_call)
        # self.prefix_expr = FunctionCallStmt(fn, None, self.args)

    # Enter a parse tree produced by LuaParser#nameOrExp.
    def enterNameOrExp(self, ctx: LuaParser.NameOrExpContext):
        pass

    # Exit a parse tree produced by LuaParser#nameOrExp.
    def exitNameOrExp(self, ctx: LuaParser.NameOrExpContext):
        if ctx.NAME() is not None:
            self.prefix_stack.append(prefix_name(ctx.NAME().getText()))
        else:
            self.prefix_stack.append(PrefixExpr.round(self.exprlist_stack[-1].pop()))

    # Enter a parse tree produced by LuaParser#prefix_.
    def enterPrefix_(self, ctx: LuaParser.Prefix_Context):
        pass

    # Exit a parse tree produced by LuaParser#prefix_.
    def exitPrefix_(self, ctx: LuaParser.Prefix_Context):
        if ctx.getChildCount() != 0:
            if ctx.getChild(0).getText() == '[':
                self.prefix_stack.append(prefix_bracket(self.prefix_stack.pop(), self.exprlist_stack[-1].pop()))
            elif ctx.getChild(0).getText() == '.':
                self.prefix_stack.append(prefix_dot(self.prefix_stack.pop(), TermName(ctx.NAME().getText())))
            else:
                for name_and_args in self.name_and_args:
                    self.prefix_stack.append(PrefixExpr.call(FunctionCallStmt(self.prefix_stack.pop(),
                                                                         name_and_args.opt_name, name_and_args)))
                self.name_and_args = []

    # Enter a parse tree produced by LuaParser#functioncall.
    def enterFunctioncall(self, ctx: LuaParser.FunctioncallContext):
        # self.prefix_stack.append([])
        pass

    # Exit a parse tree produced by LuaParser#functioncall.
    def exitFunctioncall(self, ctx: LuaParser.FunctioncallContext):
        if isinstance(ctx.getChild(0), TerminalNode):
            prefix_expr = prefix_name(ctx.NAME().getText())
        elif ctx.getChild(0).getText() == '(':
            prefix_expr = self.prefix_expr_stack.pop()
        elif ctx.getChild(1).getText() == '[':
            prefix_expr = prefix_bracket(self.prefix_stack.pop(), self.exprlist_stack[-1].pop())
        else:
            prefix_expr = prefix_dot(self.prefix_stack.pop(), TermName(ctx.NAME().getText()))

        for idx, name_and_args in enumerate(self.name_and_args):
            if idx == len(self.name_and_args) - 1:
                self.function_call_stack.append(FunctionCallStmt(prefix_expr, name_and_args.opt_name, name_and_args))
            else:
                prefix_expr = PrefixExpr.call(FunctionCallStmt(prefix_expr, name_and_args.opt_name, name_and_args))

        #clean
        # self.prefix_stack.pop()
        self.name_and_args = []

    # Enter a parse tree produced by LuaParser#prefixexp.
    def enterPrefixexp(self, ctx: LuaParser.PrefixexpContext):
        # self.prefix_stack.append([])
        pass

    # Exit a parse tree produced by LuaParser#prefixexp.
    def exitPrefixexp(self, ctx: LuaParser.PrefixexpContext):
        # var
        if ctx.var_() is not None:
            self.prefix_expr_stack.append(PrefixExpr.var(self.varlist[-1].pop()))
        # function call
        elif ctx.functioncall() is not None:
            self.prefix_expr_stack.append(PrefixExpr.call(self.function_call_stack.pop()))
        else:
            self.prefix_expr_stack.append(PrefixExpr.round(self.exprlist_stack.pop()))

        # clean
        # self.prefix_stack.pop()

    # Enter a parse tree produced by LuaParser#varOrExp.
    def enterVarOrExp(self, ctx: LuaParser.VarOrExpContext):
        pass

    # Exit a parse tree produced by LuaParser#varOrExp.
    def exitVarOrExp(self, ctx: LuaParser.VarOrExpContext):
        pass

    # Enter a parse tree produced by LuaParser#var_.
    def enterVar_(self, ctx: LuaParser.Var_Context):
        pass

    # Exit a parse tree produced by LuaParser#var_.
    def exitVar_(self, ctx: LuaParser.Var_Context):
        if ctx.prefix() is not None:
            if ctx.NAME() is not None:
                self.var = Var.dot(self.prefix_stack.pop(), TermName(ctx.NAME().getText()))
            else:
                self.var = Var.bracket(self.prefix_stack.pop(), self.expr)
        else:
            self.var = Var.name(TermName(ctx.NAME().getText()))

        self.varlist[-1].append(self.var)

    # Enter a parse tree produced by LuaParser#varSuffix.
    def enterVarSuffix(self, ctx: LuaParser.VarSuffixContext):
        pass

    # Exit a parse tree produced by LuaParser#varSuffix.
    def exitVarSuffix(self, ctx: LuaParser.VarSuffixContext):
        pass

    # Enter a parse tree produced by LuaParser#nameAndArgs.
    def enterNameAndArgs(self, ctx: LuaParser.NameAndArgsContext):
        print('------enter------')

    # Exit a parse tree produced by LuaParser#nameAndArgs.
    def exitNameAndArgs(self, ctx: LuaParser.NameAndArgsContext):
        self.name_and_args.append(Args.params(self.args, None if ctx.NAME() is None else TermName(ctx.NAME().getText())))

    # Enter a parse tree produced by LuaParser#args.
    def enterArgs(self, ctx: LuaParser.ArgsContext):
        pass

    # Exit a parse tree produced by LuaParser#args.
    def exitArgs(self, ctx: LuaParser.ArgsContext):
        if ctx.string() is not None:
            self.args = Args.string(self.name)
        elif ctx.getChild(0).getText() == '(':
            expr_list = []
            if ctx.explist() is None:
                self.args = Args.params(ExprList())
            else:
                for i in ctx.explist().exp():
                    expr_list.append(self.exprlist_stack[-1].pop())
                expr_list.reverse()
                self.args = Args.params(ExprList(*expr_list))
        else:
            self.args = Args.table_constructor(self.table_constructor)

    # Enter a parse tree produced by LuaParser#functiondef.
    def enterFunctiondef(self, ctx: LuaParser.FunctiondefContext):
        pass

    # Exit a parse tree produced by LuaParser#functiondef.
    def exitFunctiondef(self, ctx: LuaParser.FunctiondefContext):
        pass

    # Enter a parse tree produced by LuaParser#funcbody.
    def enterFuncbody(self, ctx: LuaParser.FuncbodyContext):
        pass

    # Exit a parse tree produced by LuaParser#funcbody.
    def exitFuncbody(self, ctx: LuaParser.FuncbodyContext):
        if ctx.parlist() is None:
            parlist = ParList.name(NameList(), None)
        else:
            parlist = self.parlist[-1].pop()

        self.func_body_stack.append({
            'args': parlist,
            'body': self.block_stack.pop()
        })

    # Enter a parse tree produced by LuaParser#parlist.
    def enterParlist(self, ctx: LuaParser.ParlistContext):
        pass

    # Exit a parse tree produced by LuaParser#parlist.
    def exitParlist(self, ctx: LuaParser.ParlistContext):
        if ctx.namelist() is not None:
            name_list = [TermName(i.getText()) for i in ctx.namelist().NAME()]
            if ctx.getChild(ctx.getChildCount() - 1).getText() == '...':
                elp = TermEllipsis()
            else:
                elp = None
            parlist = ParList.name(NameList(*name_list), elp)
        else:
            parlist = ParList.ellipsis(TermEllipsis())

        self.parlist[-1].append(parlist)

    # Enter a parse tree produced by LuaParser#tableconstructor.
    def enterTableconstructor(self, ctx: LuaParser.TableconstructorContext):
        pass

    # Exit a parse tree produced by LuaParser#tableconstructor.
    def exitTableconstructor(self, ctx: LuaParser.TableconstructorContext):
        pass

    # Enter a parse tree produced by LuaParser#fieldlist.
    def enterFieldlist(self, ctx: LuaParser.FieldlistContext):
        pass

    # Exit a parse tree produced by LuaParser#fieldlist.
    def exitFieldlist(self, ctx: LuaParser.FieldlistContext):
        pass

    # Enter a parse tree produced by LuaParser#field.
    def enterField(self, ctx: LuaParser.FieldContext):
        pass

    # Exit a parse tree produced by LuaParser#field.
    def exitField(self, ctx: LuaParser.FieldContext):
        cur_exprlist = self.exprlist_stack[-1]
        if ctx.getChild(0).getText() == '[':
            val = cur_exprlist.pop()
            key = cur_exprlist.pop()
            field = Field.bracket(key, val)
        elif ctx.NAME() is not None:
            field = Field.assign(TermName(ctx.NAME().getText()), cur_exprlist.pop())
        else:
            field = Field.exp(cur_exprlist.pop())

        self.field_stack.append(field)


    # Enter a parse tree produced by LuaParser#fieldsep.
    def enterFieldsep(self, ctx: LuaParser.FieldsepContext):
        pass

    # Exit a parse tree produced by LuaParser#fieldsep.
    def exitFieldsep(self, ctx: LuaParser.FieldsepContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorOr.
    def enterOperatorOr(self, ctx: LuaParser.OperatorOrContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorOr.
    def exitOperatorOr(self, ctx: LuaParser.OperatorOrContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorAnd.
    def enterOperatorAnd(self, ctx: LuaParser.OperatorAndContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorAnd.
    def exitOperatorAnd(self, ctx: LuaParser.OperatorAndContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorComparison.
    def enterOperatorComparison(self, ctx: LuaParser.OperatorComparisonContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorComparison.
    def exitOperatorComparison(self, ctx: LuaParser.OperatorComparisonContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorStrcat.
    def enterOperatorStrcat(self, ctx: LuaParser.OperatorStrcatContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorStrcat.
    def exitOperatorStrcat(self, ctx: LuaParser.OperatorStrcatContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorAddSub.
    def enterOperatorAddSub(self, ctx: LuaParser.OperatorAddSubContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorAddSub.
    def exitOperatorAddSub(self, ctx: LuaParser.OperatorAddSubContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorMulDivMod.
    def enterOperatorMulDivMod(self, ctx: LuaParser.OperatorMulDivModContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorMulDivMod.
    def exitOperatorMulDivMod(self, ctx: LuaParser.OperatorMulDivModContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorBitwise.
    def enterOperatorBitwise(self, ctx: LuaParser.OperatorBitwiseContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorBitwise.
    def exitOperatorBitwise(self, ctx: LuaParser.OperatorBitwiseContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorUnary.
    def enterOperatorUnary(self, ctx: LuaParser.OperatorUnaryContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorUnary.
    def exitOperatorUnary(self, ctx: LuaParser.OperatorUnaryContext):
        pass

    # Enter a parse tree produced by LuaParser#operatorPower.
    def enterOperatorPower(self, ctx: LuaParser.OperatorPowerContext):
        pass

    # Exit a parse tree produced by LuaParser#operatorPower.
    def exitOperatorPower(self, ctx: LuaParser.OperatorPowerContext):
        pass

    # Enter a parse tree produced by LuaParser#number.
    def enterNumber(self, ctx: LuaParser.NumberContext):
        pass

    # Exit a parse tree produced by LuaParser#number.
    def exitNumber(self, ctx: LuaParser.NumberContext):
        pass
        # self.number = TermNumber(ctx.getText())

    # Enter a parse tree produced by LuaParser#string.
    def enterString(self, ctx: LuaParser.StringContext):
        pass

    # Exit a parse tree produced by LuaParser#string.
    def exitString(self, ctx: LuaParser.StringContext):
        pass
        # self.str = TermString(ctx.getText().strip('"'))
        # if ctx.NORMALSTRING() is not None:
        #     self.str = ctx.NORMALSTRING().getText().strip('"')
        # elif ctx.CHARSTRING() is not None:
        #     self.str = ctx.CHARSTRING().getText()
        # else:
        #     self.str = ctx.LONGSTRING().getText()
