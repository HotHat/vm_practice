from grammar.LuaListener import LuaListener, TerminalNode
from grammar.LuaParser import LuaParser
from ast import *


class MyLuaListener(LuaListener):
    def __init__(self):
        self.chuck = None
        self.block = None
        self.stat = []
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
        self.var = None
        self.is_namelist = False
        self.namelist = []
        self.is_exprlist = False
        self.exprlist = []
        self.expr = None
        self.table_constructor = None

    def get_chuck(self):
        return self.chuck

    # Enter a parse tree produced by LuaParser#chunk.
    def enterChunk(self, ctx: LuaParser.ChunkContext):
        pass

    # Exit a parse tree produced by LuaParser#chunk.
    def exitChunk(self, ctx: LuaParser.ChunkContext):
        self.chuck = Chunk(self.block)

    # Enter a parse tree produced by LuaParser#block.
    def enterBlock(self, ctx: LuaParser.BlockContext):
        pass

    # Exit a parse tree produced by LuaParser#block.
    def exitBlock(self, ctx: LuaParser.BlockContext):
        self.block = Block(self.stat, self.ret_stat)

    # Enter a parse tree produced by LuaParser#stat.
    def enterStat(self, ctx: LuaParser.StatContext):
        pass

    # Exit a parse tree produced by LuaParser#stat.
    def exitStat(self, ctx: LuaParser.StatContext):
        # pass
        # self.stat.append(Stmt(FunctionCallStmt(self.prefix_expr, None, self.args)))
        # print(ctx.getRuleIndex())
        # print(ctx.invokingState)
        # local assign
        count = ctx.getChildCount()
        if ctx.getChild(0).getText() == 'local' and ctx.namelist() is not None:
            self.stat.append(Stmt(LocalAssignStmt(NameList(*self.namelist), ExprList(*self.exprlist))))
        if ctx.functioncall() is not None:
            self.stat.append(Stmt(self.function_call))

        # l = ctx.getChildren()
        # print()
        # for i in l:
        #     print(type(i))

        # print(ctx.namelist())
        # print(ctx.explist())
        # print(ctx.block())


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
        pass

    # Exit a parse tree produced by LuaParser#varlist.
    def exitVarlist(self, ctx: LuaParser.VarlistContext):
        pass

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
        self.is_exprlist = True

    # Exit a parse tree produced by LuaParser#explist.
    def exitExplist(self, ctx: LuaParser.ExplistContext):
        self.is_exprlist = True

    # Enter a parse tree produced by LuaParser#exp.
    def enterExp(self, ctx: LuaParser.ExpContext):
        pass

    # Exit a parse tree produced by LuaParser#exp.
    def exitExp(self, ctx: LuaParser.ExpContext):
        if self.is_exprlist:
            if ctx.string():
                self.exprlist.append(Expr(TermString(self.str)))
        pass

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
                self.var = Var.dot(self.prefix, self.name)
            else:
                self.var = Var.bracket(self.prefix, self.name)

        self.var = Var.name(self.name)

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
            self.args = Args.params(ExprList(*self.exprlist))
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
        pass

    # Enter a parse tree produced by LuaParser#parlist.
    def enterParlist(self, ctx: LuaParser.ParlistContext):
        pass

    # Exit a parse tree produced by LuaParser#parlist.
    def exitParlist(self, ctx: LuaParser.ParlistContext):
        pass

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
        pass

    # Enter a parse tree produced by LuaParser#string.
    def enterString(self, ctx: LuaParser.StringContext):
        pass

    # Exit a parse tree produced by LuaParser#string.
    def exitString(self, ctx: LuaParser.StringContext):
        if ctx.NORMALSTRING() is not None:
            self.str = ctx.NORMALSTRING().getText().strip('"')
        elif ctx.CHARSTRING() is not None:
            self.str = ctx.CHARSTRING().getText()
        else:
            self.str = ctx.LONGSTRING().getText()
