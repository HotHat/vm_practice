from grammar.LuaListener import LuaListener, TerminalNode
from grammar.LuaParser import LuaParser
from ast import *


class MyLuaListener(LuaListener):
    def __init__(self):
        self.chuck = None
        self.block = None
        self.block_stack = []
        self.stat_stack = []
        self.ret_stat = None
        self.prefix_expr = None
        self.prefix = None
        self.prefix_name = None
        self.prefix_call = None
        self.function_call = None
        self.args = None
        self.name_and_args = []
        self.name = None
        self.str = None
        self.number = None
        self.var = None
        self.is_namelist = False
        self.namelist = []
        self.is_exprlist_level = 0
        self.exprlist_stack = []
        self.exprlist = []
        self.is_var_list = False
        self.varlist = []
        self.expr = None
        self.table_constructor = None
        self.parlist = []
        self.func_body_stack = []

    def get_chuck(self):
        return self.chuck

    # Enter a parse tree produced by LuaParser#chunk.
    def enterChunk(self, ctx: LuaParser.ChunkContext):
        pass

    # Exit a parse tree produced by LuaParser#chunk.
    def exitChunk(self, ctx: LuaParser.ChunkContext):
        self.chuck = Chunk(self.block_stack[0])

    # Enter a parse tree produced by LuaParser#block.
    def enterBlock(self, ctx: LuaParser.BlockContext):
        print('----enter block-----')
        self.stat_stack.append([])
        self.exprlist_stack.append([])
        pass

    # Exit a parse tree produced by LuaParser#block.
    def exitBlock(self, ctx: LuaParser.BlockContext):
        cur_stat = self.stat_stack[-1]
        print('----exit block---')
        self.block = Block(cur_stat, self.ret_stat)
        self.stat_stack.pop()
        self.block_stack.append(self.block)
        self.exprlist_stack.pop()

    # Enter a parse tree produced by LuaParser#stat_stack.
    def enterStat(self, ctx: LuaParser.StatContext):
        pass

    # Exit a parse tree produced by LuaParser#stat_stack.
    def exitStat(self, ctx: LuaParser.StatContext):
        print([i for i in ctx.getChildren()])
        cur_stat = self.stat_stack[-1]
        if ctx.getChildCount() == 0:
            return

        if ctx.label():
            cur_stat.append(Stmt(Label(self.name)))
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
            print(self.exprlist_stack)
            print(self.block_stack)
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

            func_body = self.func_body_stack[-1]
            cur_stat.append(Stmt(FunctionStmt(func_name, func_body['args'], func_body['body'])))
            self.func_body_stack.pop()

        elif ctx.getChild(0).getText() == 'local':
            print('---local assign---')
            if ctx.namelist() is not None:
                cur_stat.append(Stmt(LocalAssignStmt(NameList(*self.namelist), ExprList(*self.exprlist_stack[-1]))))
                self.namelist = []
                self.exprlist_stack.pop()
            else:
                print('-----exit local function------')
                name = TermName(ctx.getChild(2).getText())
                func_body = self.func_body_stack[-1]
                cur_stat.append(Stmt(LocalFunctionStmt(name, func_body['args'], func_body['body'])))
                self.func_body_stack.pop()
                pass
        elif ctx.functioncall() is not None:
            print('---function call ---')
            cur_stat.append(Stmt(self.function_call))
        else:
            # varlist = explist
            cur_stat.append(Stmt(AssignStmt(VarList(*self.varlist), ExprList(*self.exprlist_stack[-1]))))
            self.varlist = []
            self.exprlist_stack.pop()

    # Enter a parse tree produced by LuaParser#retstat.
    def enterRetstat(self, ctx: LuaParser.RetstatContext):
        pass

    # Exit a parse tree produced by LuaParser#retstat.
    def exitRetstat(self, ctx: LuaParser.RetstatContext):
        pass

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
        self.is_var_list = True

    # Exit a parse tree produced by LuaParser#varlist.
    def exitVarlist(self, ctx: LuaParser.VarlistContext):
        self.is_var_list = False

    # Enter a parse tree produced by LuaParser#namelist.
    def enterNamelist(self, ctx: LuaParser.NamelistContext):
        pass

    # Exit a parse tree produced by LuaParser#namelist.
    def exitNamelist(self, ctx: LuaParser.NamelistContext):
        for i in ctx.NAME():
            print(i.getText())
            self.namelist.append(TermName(i.getText()))

    # Enter a parse tree produced by LuaParser#explist.
    def enterExplist(self, ctx: LuaParser.ExplistContext):
        self.exprlist_stack.append([])
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
        pass
        # print('enter exp')

    # Exit a parse tree produced by LuaParser#exp.
    def exitExp(self, ctx: LuaParser.ExpContext):
        # print('exit exp', ctx.parentCtx, ctx.getChildCount())
        if ctx.getChild(0).getText() == 'nil':
            self.expr = Expr(TermNil())
        elif ctx.getChild(0).getText() == 'false':
            self.expr = Expr(TermFalse())
        elif ctx.getChild(0).getText() == 'true':
            self.expr = Expr(TermTrue())
        elif ctx.getChild(0).getText() == '...':
            self.expr = Expr(TermEllipsis())
        elif ctx.number() is not None:
            self.expr = Expr(self.number)
        elif ctx.string() is not None:
            self.expr = Expr(self.str)
        elif ctx.prefixexp() is not None:
            self.expr = Expr(self.prefix_expr)
        # unary operation
        elif ctx.operatorUnary() is not None:
            expr = self.exprlist_stack[-1].pop()
            self.expr = Expr(UnOpExpr(UnOpEnum.from_symbol(ctx.operatorUnary().getText()), expr))
        # binary operation
        elif ctx.exp() is not None:
            # first in last out
            cur_exprlist = self.exprlist_stack[-1]
            right = cur_exprlist.pop()
            left = cur_exprlist.pop()
            self.expr = Expr(BinOpExpr(BinOpEnum.from_symbol(ctx.getChild(1).getText()), left, right))
        # TODO: missing functiondef, tableconstructor
        self.exprlist_stack[-1].append(self.expr)

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
            self.prefix = prefix_name(ctx.NAME().getText())
        else:
            self.prefix = PrefixExpr.round(self.expr)

    # Enter a parse tree produced by LuaParser#prefix_.
    def enterPrefix_(self, ctx: LuaParser.Prefix_Context):
        pass

    # Exit a parse tree produced by LuaParser#prefix_.
    def exitPrefix_(self, ctx: LuaParser.Prefix_Context):
        if ctx.getChildCount() != 0:
            if ctx.getChild(0).getText() == '[':
                self.prefix = prefix_bracket(self.prefix, self.expr)
            elif ctx.getChild(0).getText() == '.':
                self.prefix = prefix_dot(self.prefix, TermName(ctx.NAME().getText()))
            else:
                for name_and_args in self.name_and_args:
                    self.prefix = PrefixExpr.call(FunctionCallStmt(self.prefix,
                                                                   name_and_args.opt_name, name_and_args))
                self.name_and_args = []

    # Enter a parse tree produced by LuaParser#functioncall.
    def enterFunctioncall(self, ctx: LuaParser.FunctioncallContext):
        pass

    # Exit a parse tree produced by LuaParser#functioncall.
    def exitFunctioncall(self, ctx: LuaParser.FunctioncallContext):
        if isinstance(ctx.getChild(0), TerminalNode):
            prefix_expr = prefix_name(ctx.NAME().getText())
        elif ctx.getChild(0).getText() == '(':
            prefix_expr = self.prefix_expr
        elif ctx.getChild(1).getText() == '[':
            prefix_expr = prefix_bracket(self.prefix, self.expr)
        else:
            prefix_expr = prefix_dot(self.prefix, TermName(ctx.NAME().getText()))

        for idx, name_and_args in enumerate(self.name_and_args):
            if idx == len(self.name_and_args) - 1:
                self.function_call = FunctionCallStmt(prefix_expr, name_and_args.opt_name, name_and_args)
            else:
                prefix_expr = PrefixExpr.call(FunctionCallStmt(prefix_expr, name_and_args.opt_name, name_and_args))

        self.name_and_args = []

    # Enter a parse tree produced by LuaParser#prefixexp.
    def enterPrefixexp(self, ctx: LuaParser.PrefixexpContext):
        pass

    # Exit a parse tree produced by LuaParser#prefixexp.
    def exitPrefixexp(self, ctx: LuaParser.PrefixexpContext):
        if ctx.var_() is not None:
            self.prefix_expr = PrefixExpr.var(self.var)

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
                self.var = Var.dot(self.prefix, TermName(ctx.NAME().getText()))
            else:
                self.var = Var.bracket(self.prefix, self.expr)
        else:
            self.var = Var.name(TermName(ctx.NAME().getText()))

        if self.is_var_list:
            self.varlist.append(self.var)

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
            self.args = Args.params(ExprList(*self.exprlist_stack[-1]))
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
            parlist = self.parlist[-1]

        self.func_body_stack.append({
            'args': parlist,
            'body': self.block_stack.pop()
        })
        if ctx.parlist():
            self.parlist.pop()

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

        self.parlist.append(parlist)

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
        pass

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
        self.number = TermNumber(ctx.getText())

    # Enter a parse tree produced by LuaParser#string.
    def enterString(self, ctx: LuaParser.StringContext):
        pass

    # Exit a parse tree produced by LuaParser#string.
    def exitString(self, ctx: LuaParser.StringContext):
        self.str = TermString(ctx.getText().strip('"'))
        # if ctx.NORMALSTRING() is not None:
        #     self.str = ctx.NORMALSTRING().getText().strip('"')
        # elif ctx.CHARSTRING() is not None:
        #     self.str = ctx.CHARSTRING().getText()
        # else:
        #     self.str = ctx.LONGSTRING().getText()
