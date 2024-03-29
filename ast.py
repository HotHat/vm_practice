"""
Lua 5.3 Reference Manual
https://www.lua.org/manual/5.3/manual.html
"""
from typing import Optional, Sequence
from enum import Enum


class DotLangTag:
    def get_tag(self):
        if self.tag is None:
            self.tag = tag_number()
        return self.tag

    def get_tag_name(self):
        pass


# --------------  terminal start ---------------

class Terminal:
    """ terminal item"""
    pass


class TermNil(Terminal, DotLangTag):
    def __init__(self):
        self.tag = None

    def __str__(self):
        return f"{self.get_tag()}[label=\"nil\"]"


class TermFalse(Terminal, DotLangTag):
    def __init__(self):
        self.tag = None

    def __str__(self):
        return f"{self.get_tag()}[label=\"false\"]"


class TermTrue(Terminal, DotLangTag):
    def __init__(self):
        self.tag = None

    def __str__(self):
        return f"{self.get_tag()}[label=\"true\"]"


class TermNumber(Terminal, DotLangTag):
    def __init__(self, n):
        self.value = n
        self.tag = None

    def __str__(self):
        return f"{self.get_tag()}[label=\"{self.value}\"]"


class TermString(Terminal, DotLangTag):
    def __init__(self, n):
        self.value = n
        self.tag = None

    def __str__(self):
        return f"{self.get_tag()}[label=\"{self.value}\"]"


class TermName(Terminal, DotLangTag):
    def __init__(self, n):
        self.value = n
        self.tag = None

    def __str__(self):
        return f"{self.get_tag()}[label=\"{self.value}\"]"


class TermEllipsis(Terminal, DotLangTag):
    def __init__(self):
        self.tag = None

    def __str__(self):
        return f"{self.get_tag()}[label=\"...\"]"


def number(n):
    return Expr(TermNumber(n))


def string(s):
    return Expr(TermString(s))


# --------------  terminal start ---------------


class Block(DotLangTag):
    def __init__(self, stat_arr: Sequence['Stmt'], ret_stat: Optional['ReturnStmt'] = None):
        self.stat_arr = stat_arr
        self.ret_stat = ret_stat
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"block\"]"

    def __str__(self):
        tag = self.get_tag()
        stat_arr_s = "\n".join([f"{tag}->{stat.get_tag()}" for stat in self.stat_arr])
        stat_arr_ss = "\n".join([f"{stat.__str__()}" for stat in self.stat_arr])
        ls = lss = ''
        if self.ret_stat is not None:
            ls = f"{tag}->{self.ret_stat.get_tag()}\n"
            lss = f"{self.ret_stat.__str__()}\n"

        return f"{self.get_tag_name()}\n" \
               f"{stat_arr_s}\n" \
               f"{ls}" \
               f"{stat_arr_ss}" \
               f"{lss}"


class Chunk(DotLangTag):
    def __init__(self, block: Block, is_root: bool = False):
        self.block = block
        self.is_root = is_root
        self.true_list = []
        self.false_list = []
        self.next_list = []
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"chunk\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.block.__str__()}"


# --------------  stmt start ---------------
class StmtEnum(Enum):
    ASSIGN = 1
    FUNCTION_CALL = 2
    DO = 3
    WHILE = 5
    REPEAT = 4
    IF = 5
    FOR = 6
    FOREACH = 7
    FUNCTION = 8
    LOCAL_FUNCTION = 9
    LOCAL_ASSIGN = 10


class Stmt(DotLangTag):
    """ = Stat """

    def __init__(self, value):
        if type(value) is AssignStmt:
            self.kind = StmtEnum.ASSIGN
        elif type(value) is FunctionCallStmt:
            self.kind = StmtEnum.FUNCTION_CALL
        elif type(value) is DoStmt:
            self.kind = StmtEnum.DO
        elif type(value) is WhileStmt:
            self.kind = StmtEnum.WHILE
        elif type(value) is RepeatStmt:
            self.kind = StmtEnum.REPEAT
        elif type(value) is IfStmt:
            self.kind = StmtEnum.IF
        elif type(value) is ForStmt:
            self.kind = StmtEnum.FOR
        elif type(value) is ForeachStmt:
            self.kind = StmtEnum.FOREACH
        elif type(value) is FunctionStmt:
            self.kind = StmtEnum.FUNCTION
        elif type(value) is LocalFunctionStmt:
            self.kind = StmtEnum.LOCAL_FUNCTION
        elif type(value) is LocalAssignStmt:
            self.kind = StmtEnum.LOCAL_ASSIGN

        self.value = value
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n{tag}->{self.value.get_tag()}\n{self.value.__str__()}"


class AssignStmt(Stmt, DotLangTag):
    def __init__(self, left: 'VarList', right: 'ExprList'):
        self.left = left
        self.right = right
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"assign\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.left.get_tag()}\n" \
               f"{tag}->{self.right.get_tag()}\n" \
               f"{self.left.__str__()}\n" \
               f"{self.right.__str__()}"


class FunctionCallStmt(Stmt, DotLangTag):
    """
    functioncall ::=  prefixexp args  |  prefixexp `:´ Name args
    """

    def __init__(self, prefix_expr: 'PrefixExpr', colon_name: Optional[TermName], args: 'Args'):
        self.prefix_expr = prefix_expr
        self.colon_name = colon_name
        self.args = args
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"function_call\"]"

    def __str__(self):
        tag = self.get_tag()
        cpd = cps = ''
        if self.colon_name is not None:
            cpd = f"{tag}->{self.colon_name.get_tag()}\n"
            cps = f"{self.colon_name.__str__()}\n"
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.prefix_expr.get_tag()}\n" \
               f"{self.prefix_expr.__str__()}\n" \
               f"{cpd}" \
               f"{tag}->{self.args.get_tag()}\n" \
               f"{cps}" \
               f"{self.args.__str__()}"


class DoStmt(Stmt, DotLangTag):
    def __init__(self, block):
        self.block = block
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"do_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.block.__str__()}\n"


class WhileStmt(Stmt):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"while_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.cond.get_tag()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.cond.__str__()}\n" \
               f"{self.block.__str__()}"


class RepeatStmt(Stmt):
    def __init__(self, block: Block, exp: 'Expr'):
        self.block = block
        self.expr = exp
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"repeat_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{tag}->{self.expr.get_tag()}\n" \
               f"{self.block.__str__()}\n" \
               f"{self.expr.__str__()}"


class IfStmt(Stmt):
    def __init__(self, cond: 'Expr', block: Block, elif_arr: Optional[Sequence['ElifStmt']], else_block: Optional[Block]):
        self.cond = cond
        self.block = block
        self.elif_arr = elif_arr
        self.else_block = else_block
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"if_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        elif_opt = elif_opts = ''
        else_opt = else_opts = ''

        if self.elif_arr is not None:
            elif_opt = "\n".join([f"{tag}->{it.get_tag()}\n" for it in self.elif_arr])
            elif_opts = "\n".join([f"{it.__str__()}\n" for it in self.elif_arr])
        if self.else_block is not None:
            else_opt = f"{tag}->{self.else_block.get_tag()}\n"
            else_opts = f"{self.else_block.__str__()}\n"

        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.cond.get_tag()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.cond.__str__()}\n" \
               f"{self.block.__str__()}\n" \
               f"{elif_opt}" \
               f"{elif_opts}" \
               f"{else_opt}" \
               f"{else_opts}"


class ElifStmt(Stmt):
    def __init__(self, cond: 'Expr', block: Block):
        self.cond = cond
        self.block = block
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"else_if\"]"

    def __str__(self):
        tag = self.get_tag()

        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.cond.get_tag()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.cond.__str__()}\n" \
               f"{self.block.__str__()}\n"


class ForStmt(Stmt):
    def __init__(self, name: TermName, assign: 'Expr', cond: 'Expr', nxt: Optional['Expr'], block: Block):
        self.name = name
        self.assign = assign
        self.cond = cond
        self.next = nxt
        self.block = block
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"for_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        next_opt = next_opts = ''

        if self.next is not None:
            next_opt = f"{tag}->{self.next.get_tag()}\n"
            next_opts = f"{self.next.__str__()}\n"

        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.name.get_tag()}\n" \
               f"{tag}->{self.assign.get_tag()}\n" \
               f"{tag}->{self.cond.get_tag()}\n" \
               f"{next_opt}" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.name.__str__()}\n" \
               f"{self.assign.__str__()}\n" \
               f"{self.cond.__str__()}\n" \
               f"{next_opts}" \
               f"{self.block.__str__()}"


class ForeachStmt(Stmt, DotLangTag):
    def __init__(self, name_list: 'NameList', exp_list: 'ExprList', block: Block):
        self.name_list = name_list
        self.exp_list = exp_list
        self.block = block
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"foreach_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.name_list.get_tag()}\n" \
               f"{tag}->{self.exp_list.get_tag()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.name_list.__str__()}\n" \
               f"{self.exp_list.__str__()}\n" \
               f"{self.block.__str__()}"


class FunctionStmt(Stmt, DotLangTag):
    def __init__(self, name: 'FunctionName', args, body: Block):
        self.name = name
        self.args = args
        self.body = body
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"function_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.name.get_tag()}\n" \
               f"{tag}->{self.args.get_tag()}\n" \
               f"{tag}->{self.body.get_tag()}\n" \
               f"{self.name.__str__()}\n" \
               f"{self.args.__str__()}\n" \
               f"{self.body.__str__()}"


class LocalFunctionStmt(Stmt, DotLangTag):
    def __init__(self, name: TermName, args: 'ParList', body: Block):
        self.name = name
        self.args = args
        self.body = body
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"local_function_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.name.get_tag()}\n" \
               f"{tag}->{self.args.get_tag()}\n" \
               f"{tag}->{self.body.get_tag()}\n" \
               f"{self.name.__str__()}\n" \
               f"{self.args.__str__()}\n" \
               f"{self.body.__str__()}"


class LocalAssignStmt(Stmt, DotLangTag):
    def __init__(self, left: 'NameList', right: 'ExprList'):
        self.left = left
        self.right = right
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"local_assign\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.left.get_tag()}\n" \
               f"{tag}->{self.right.get_tag()}\n" \
               f"{self.left.__str__()}\n" \
               f"{self.right.__str__()}"


class ReturnStmt(Stmt):
    RETURN = 1
    BREAK = 2

    def __init__(self, exp_list: Optional['ExprList']):
        self.exp_list = exp_list
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"return_stmt\"]"

    def __str__(self):
        tag = self.get_tag()
        name = self.get_tag_name()
        return f"{name}\n" \
               f"{tag}->{self.exp_list.get_tag()}\n" \
               f"{self.exp_list.__str__()}"


    def is_break(self):
        return self.kind == ReturnStmt.BREAK

    @staticmethod
    def ret(exp_list):
        return ReturnStmt(ReturnStmt.RETURN, exp_list)

    @staticmethod
    def brk():
        return ReturnStmt(ReturnStmt.BREAK, None)


# --------------  stmt end ---------------

class FunctionName(DotLangTag):
    """
    funcname ::= Name {`.´ Name} [`:´ Name]
    """

    def __init__(self, name: TermName, opt_name: Optional[Sequence[TermName]] = None,
                 colon_name: Optional[TermName] = None):
        self.name = name
        self.opt_name = opt_name
        self.colon_name = colon_name
        self.tag = None

    def get_tag_name(self):
        name = self.name.value
        if self.opt_name:
            name = f"{name}.{'.'.join([tn.value for tn in self.opt_name])}"
        if self.colon_name:
            name = f"{name}:{self.colon_name.value}"
        return f"{self.get_tag()}[label=\"{name}\"]"

    def __str__(self):
        return f"{self.get_tag_name()}"


class Var(DotLangTag):
    """
    name ::=  Name  |  prefixexp `[´ expr `]´  |  prefixexp `.´ Name
    """
    NAME = 1
    BRACKET = 2
    DOT = 3

    def __init__(self, kind, prefix_exp: Optional['PrefixExpr'], exp: Optional['Expr'], name: Optional[TermName]):
        self.kind = kind
        self.prefix_exp = prefix_exp
        self.exp = exp
        self.name = name
        self.tag = None

    def get_tag_name(self):
        if self.kind == Var.NAME:
            return f"{self.get_tag()}[label=\"name\"]"
        elif self.kind == Var.BRACKET:
            return f"{self.get_tag()}[label=\"bracket\"]"
        else:
            return f"{self.get_tag()}[label=\"dot\"]"

    def __str__(self):
        tag = self.get_tag()
        if self.kind == Var.NAME:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.name.get_tag()}\n{self.name.__str__()}"
        elif self.kind == Var.BRACKET:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.prefix_exp.get_tag()}\n" \
                   f"{tag}->{self.exp.get_tag()}\n" \
                   f"{self.prefix_exp.__str__()}\n" \
                   f"{self.exp.__str__()}"
        elif self.kind == Var.DOT:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.prefix_exp.get_tag()}\n" \
                   f"{tag}->{self.name.get_tag()}\n" \
                   f"{self.prefix_exp.__str__()}\n" \
                   f"{self.name.__str__()}"

    @staticmethod
    def name(name: TermName):
        return Var(Var.NAME, None, None, name)

    @staticmethod
    def bracket(prefix_expr: 'PrefixExpr', expr: 'Expr'):
        return Var(Var.BRACKET, prefix_expr, expr, None)

    @staticmethod
    def dot(prefix_expr: 'PrefixExpr', name: TermName):
        return Var(Var.DOT, prefix_expr, None, name)


def var_name(name):
    return Var(TermName(name))


class VarList(DotLangTag):
    def __init__(self, *var_list: Var):
        self.var_list = var_list
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"var_list\"]"

    def __str__(self):
        tag = self.get_tag()
        pre = "\n".join([f"{tag}->{var.get_tag()}" for var in self.var_list])
        sub = "\n".join([var.__str__() for var in self.var_list])
        return f"{self.get_tag_name()}\n{pre}\n{sub}"


class NameList(DotLangTag):
    def __init__(self, *args: 'TermName'):
        self.name_list = args
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"name_list\"]"

    def __str__(self):
        tag = self.get_tag()
        pre = "\n".join([f"{tag}->{name.get_tag()}" for name in self.name_list])
        sub = "\n".join([name.__str__() for name in self.name_list])
        return f"{self.get_tag_name()}\n{pre}\n{sub}"


class ExprEnum(Enum):
    CONSTANT = 1
    PREFIX = 2
    BINOP = 3
    UNOP = 4
    FUNCTION = 5


class Expr(DotLangTag):
    def __init__(self, value):
        if type(value) is TermNil:
            self.kind = ExprEnum.CONSTANT
        elif type(value) is TermFalse:
            self.kind = ExprEnum.CONSTANT
        elif type(value) is TermTrue:
            self.kind = ExprEnum.CONSTANT
        elif type(value) is TermNumber:
            self.kind = ExprEnum.CONSTANT
        elif type(value) is TermString:
            self.kind = ExprEnum.CONSTANT
        elif type(value) is TermEllipsis:
            self.kind = ExprEnum.CONSTANT
        elif type(value) is PrefixExpr:
            self.kind = ExprEnum.PREFIX
        elif type(value) is BinOpExpr:
            self.kind = ExprEnum.BINOP
        elif type(value) is UnOpExpr:
            self.kind = ExprEnum.UNOP
        elif type(value) is FunctionExpr:
            self.kind = ExprEnum.FUNCTION

        self.value = value
        self.true_list = []
        self.false_list = []
        self.next_list = []
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"expr\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n{tag}->{self.value.get_tag()}\n{self.value.__str__()}"


class ExprList(DotLangTag):
    def __init__(self, *lst: Expr):
        self.expr_list = lst
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"exp_list\"]"

    def __str__(self):
        tag = self.get_tag()
        pre = "\n".join([f"{tag}->{exp.get_tag()}" for exp in self.expr_list])
        sub = "\n".join([exp.__str__() for exp in self.expr_list])
        return f"{self.get_tag_name()}\n{pre}\n{sub}"


class PrefixExpr(DotLangTag):
    """
    prefixexp ::= name  |  functioncall  |  `(´ expr `)´
    """
    VAR = 1
    FUNCTION_CALL = 2
    PARENTHESES = 3

    def __init__(self, kind, var: Optional['Var'], call: Optional[FunctionCallStmt], exp: Optional[Expr]):
        self.kind = kind
        self.var = var
        self.call = call
        self.exp = exp
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"prefix\"]"

    def __str__(self):
        tag = self.get_tag()
        if self.kind == PrefixExpr.VAR:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.var.get_tag()}\n{self.var.__str__()}"
        elif self.kind == PrefixExpr.FUNCTION_CALL:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.call.get_tag()}\n" \
                   f"{self.call.__str__()}"
        elif self.kind == PrefixExpr.PARENTHESES:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.exp.get_tag()}\n" \
                   f"{self.exp.__str__()}"

    @staticmethod
    def var(var: 'Var'):
        return PrefixExpr(PrefixExpr.VAR, var, None, None)

    @staticmethod
    def call(call):
        return PrefixExpr(PrefixExpr.FUNCTION_CALL, None, call, None)

    @staticmethod
    def round(exp):
        return PrefixExpr(PrefixExpr.PARENTHESES, None, None, exp)


def prefix_name(name):
    return PrefixExpr.var(Var.name(TermName(name)))


def prefix_bracket(prefix_expr: PrefixExpr, expr: Expr):
    return PrefixExpr.var(Var.bracket(prefix_expr, expr))


def prefix_dot(prefix_expr: PrefixExpr, name: 'TermName'):
    return PrefixExpr.var(Var.dot(prefix_expr, name))


class Args(DotLangTag):
    PARAMS = 1
    TABLE_CONSTRUCT = 2
    STRING = 3

    def __init__(self, kind, params: Optional['ExprList'], table_constructor: Optional['TableContructor'],
                 term_string: Optional[TermString], opt_name: Optional[TermName]):
        self.kind = kind
        self.params = params
        self.table_constructor = table_constructor
        self.string = term_string
        self.opt_name = opt_name
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"args\"]"

    def __str__(self):
        tag = self.get_tag()
        if self.kind == Args.PARAMS:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.params.get_tag()}\n" \
                   f"{self.params.__str__()}"
        elif self.kind == Args.TABLE_CONSTRUCT:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.table_constructor.get_tag()}\n" \
                   f"{self.table_constructor.__str__()}"
        elif self.kind == Args.STRING:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.string.get_tag()}\n" \
                   f"{self.string.__str__()}"

    @staticmethod
    def params(p: 'ExprList', name: Optional[TermName] = None):
        return Args(Args.PARAMS, p, None, None, name)

    @staticmethod
    def table_constructor(tb: 'TableConstructor'):
        return Args(Args.PARAMS, None, tb, None, None)

    @staticmethod
    def string(s: TermString):
        return Args(Args.PARAMS, None, None, s, None)


class FunctionExpr(DotLangTag):
    def __init__(self, par_list: 'ParList', block: Block):
        self.par_list = par_list
        self.block = block
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"function_expr\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n" \
               f"{tag}->{self.par_list.get_tag()}\n" \
               f"{tag}->{self.block.get_tag()}\n" \
               f"{self.par_list.__str__()}\n" \
               f"{self.block.__str__()}\n"


class ParList(DotLangTag):
    NAME_LIST = 1
    ELLIPSIS = 2

    def __init__(self, kind, name_list: Optional['NameList'], elp: Optional[TermEllipsis]):
        self.kind = kind
        self.name_list = name_list
        self.ellipsis = elp
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"par_list\"]"

    def __str__(self):
        tag = self.get_tag()
        if self.kind == ParList.NAME_LIST:
            opt = opts = ''
            if self.ellipsis is not None:
                opt = f"{tag}->{self.ellipsis.get_tag()}\n"
                opts = f"{self.ellipsis.__str__()}\n"
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.name_list.get_tag()}\n" \
                   f"{opt}" \
                   f"{self.name_list.__str__()}\n" \
                   f"{opts}"

        elif self.kind == ParList.ELLIPSIS:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.ellipsis.get_tag()}\n" \
                   f"{self.ellipsis.__str__()}"

    @staticmethod
    def name(name_list: 'NameList', elp: Optional[TermEllipsis] = None):
        return ParList(ParList.NAME_LIST, name_list, elp)

    @staticmethod
    def ellipsis(elp: TermEllipsis):
        return ParList(ParList.ELLIPSIS, None, elp)


class TableConstructor(DotLangTag):
    def __init__(self, field_list: Optional[Sequence['Field']]):
        self.field_list = field_list
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"table constructor\"]"

    def __str__(self):
        tag = self.get_tag()
        field_arr_s = "\n".join([f"{tag}->{field.get_tag()}" for field in self.field_list])
        for field in self.field_list:
            field_arr_s += f"\n{field.__str__()}"
        return f"{self.get_tag_name()}\n" \
               f"{field_arr_s}"


class Field(DotLangTag):
    BRACKET_ASSIGN = 1
    ASSIGN = 2
    EXP = 3

    def __init__(self, kind, left: Optional[Expr], left_name: Optional[TermName],
                 right: Optional[Expr]):
        self.kind = kind
        self.left = left
        self.left_name = left_name
        self.right = right
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"field\"]"

    def __str__(self):
        tag = self.get_tag()
        if self.kind == Field.BRACKET_ASSIGN:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.left.get_tag()}\n" \
                   f"{tag}->{self.right.get_tag()}\n" \
                   f"{self.left.__str__()}\n" \
                   f"{self.right.__str__()}"
        elif self.kind == Field.ASSIGN:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.left_name.get_tag()}\n" \
                   f"{tag}->{self.right.get_tag()}\n" \
                   f"{self.left_name.__str__()}\n" \
                   f"{self.right.__str__()}"
        else:
            return f"{self.get_tag_name()}\n" \
                   f"{tag}->{self.right.get_tag()}\n" \
                   f"{self.right.__str__()}"

    @staticmethod
    def bracket(left: Expr, right: Expr):
        return Field(Field.BRACKET_ASSIGN, left, None, right)

    @staticmethod
    def assign(left: TermName, right: Expr):
        return Field(Field.ASSIGN, None, left, right)

    @staticmethod
    def exp(right: Expr):
        return Field(Field.EXP, None, None, right)


# --------------  expression start ---------------
class BinOpEnum(Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    XOR = 5
    MOD = 6
    LT = 7
    LTE = 8
    GT = 9
    GTE = 10
    EQ = 11
    CONCAT = 12
    ASSIGN_XOR = 13
    AND = 14
    OR = 15

    @staticmethod
    def from_symbol(sym: str):
        if sym == '+':
            return BinOpEnum.ADD
        elif sym == '-':
            return BinOpEnum.SUB
        elif sym == '*':
            return BinOpEnum.MUL
        elif sym == '/':
            return BinOpEnum.DIV
        elif sym == '//':
            return BinOpEnum.MOD
        elif sym == '%':
            return BinOpEnum.MOD
        elif sym == '==':
            return BinOpEnum.EQ
        else:
            raise Exception('error binop symbol')


class BinOpExpr(DotLangTag):
    def __init__(self, op: BinOpEnum, left: Expr, right: Expr):
        self.operator = op
        self.left = left
        self.right = right
        self.false_list = []
        self.true_list = []
        self.next_list = []
        # for dot lang
        self.tag = None
        self.tag_name = self.operator

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"{self.operator.name}\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n{tag}->{self.left.get_tag()}\n{tag}->{self.right.get_tag()}\n" \
               f"{self.left.__str__()}\n{self.right.__str__()}"


class UnOpEnum(Enum):
    MINUS = 1
    NOT = 2
    SHARP = 3
    TILDE = 4

    @staticmethod
    def from_symbol(sym: str):
        if sym == '-':
            return UnOpEnum.MINUS
        elif sym == 'not':
            return UnOpEnum.NOT
        elif sym == '#':
            return UnOpEnum.SHARP
        elif sym == '~':
            return UnOpEnum.TILDE
        else:
            raise Exception('error unop symbol')


class UnOpExpr(DotLangTag):
    def __init__(self, op: UnOpEnum, expr: Expr):
        self.operator = op
        self.expr = expr
        self.false_list = []
        self.true_list = []
        self.next_list = []
        # for dot lang
        self.tag = None
        self.tag_name = self.operator

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"{self.operator.name}\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n{tag}->{self.expr.get_tag()}\n{self.expr.__str__()}"


class Label(DotLangTag):
    def __init__(self, label: TermName):
        self.label = label
        # for dot lang
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"{self.label}\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n"


class Break(DotLangTag):
    def __init__(self):
        # for dot lang
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"break\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n"


class Goto(DotLangTag):
    def __init__(self, label: TermName):
        self.label = label
        # for dot lang
        self.tag = None

    def get_tag_name(self):
        return f"{self.get_tag()}[label=\"goto\"]"

    def __str__(self):
        tag = self.get_tag()
        return f"{self.get_tag_name()}\n{tag}->{self.label.get_tag()}\n{self.label.__str__()}"


# --------------  expression end ---------------


TAG_NUMBER = 1


def tag_number():
    global TAG_NUMBER
    tag = TAG_NUMBER
    TAG_NUMBER = TAG_NUMBER + 1
    return tag
