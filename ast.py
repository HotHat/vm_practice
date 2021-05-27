"""
Lua 5.1 Reference Manual
chunk ::= {stat [`;´]} [laststat[`;´]]

block ::= chunk

stat ::=  varlist1 `=´ explist1  |
         functioncall  |
         do block end  |
         while exp do block end  |
         repeat block until exp  |
         if exp then block {elseif exp then block} [else block] end  |
         for Name `=´ exp `,´ exp [`,´ exp] do block end  |
         for namelist in explist1 do block end  |
         function funcname funcbody  |
         local function Name funcbody  |
         local namelist [`=´ explist1]

laststat ::= return [explist1]  |  break

funcname ::= Name {`.´ Name} [`:´ Name]

varlist1 ::= var {`,´ var}

var ::=  Name  |  prefixexp `[´ exp `]´  |  prefixexp `.´ Name

namelist ::= Name {`,´ Name}

explist1 ::= {exp `,´} exp

exp ::=  nil  |  false  |  true  |  Number  |  String  |  `...´  |
         function  |  prefixexp  |  TableConstructoror  |  exp binop exp  |  unop exp

prefixexp ::= var  |  functioncall  |  `(´ exp `)´

functioncall ::=  prefixexp args  |  prefixexp `:´ Name args

args ::=  `(´ [explist1] `)´  |  TableConstructoror  |  String

function ::= function funcbody

funcbody ::= `(´ [parlist1] `)´ block end

parlist1 ::= namelist [`,´ `...´]  |  `...´

TableConstructoror ::= `{´ [fieldlist] `}´

fieldlist ::= field {fieldsep field} [fieldsep]

field ::= `[´ exp `]´ `=´ exp  |  Name `=´ exp  |  exp

fieldsep ::= `,´  |  `;´

binop ::= `+´  |  `-´  |  `*´  |  `/´  |  `^´  |  `%´  |  `..´  |

         `<´  |  `<=´  |  `>´  |  `>=´  |  `==´  |  `~=´  |
         and  |  or

unop ::= `-´  |  not  |  `#´
"""
from typing import Optional, Sequence
from enum import Enum


# --------------  terminal start ---------------
class Terminal:
    """ terminal item"""
    pass


class TermNil(Terminal):
    pass


class TermFalse(Terminal):
    pass


class TermTrue(Terminal):
    pass


class TermNumber(Terminal):
    def __init__(self, n):
        self.value = n


class TermString(Terminal):
    def __init__(self, n):
        self.value = n


class TermName(Terminal):
    def __init__(self, n):
        self.value = n


class TermEllipsis(Terminal):
    pass


def number(n):
    return Expr(TermNumber(n))


def string(s):
    return Expr(TermString(s))
# --------------  terminal start ---------------


class Chunk:
    def __init__(self, stat_arr: Sequence['Stmt'], last_stat: 'LastStmt'):
        self.stat_arr = stat_arr
        self.last_stat = last_stat

    def __str__(self):
        return f"graph {{ {self.stat_arr} {self.last_stat} }}"


class Block:
    def __init__(self, chunk: Chunk, is_root: bool = False):
        self.chunk = chunk
        self.is_root = is_root

    def __str__(self):
        if self.is_root:
            return f"graph {{ {self.chunk.__str__()} }}"
        else:
            return self.chunk.__str__()


# --------------  stmt start ---------------

class Stmt:
    """ = Stat """
    pass


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


class AssignStmt(Stmt):
    def __init__(self, left: 'VarList', right: 'ExprList'):
        self.left = left
        self.right = right


class FunctionCallStmt(Stmt):
    """
    functioncall ::=  prefixexp args  |  prefixexp `:´ Name args
    """

    def __init__(self, prefix_expr: 'PrefixExpr', colon_name: Optional[TermName], args: 'Args'):
        self.prefix_expr = prefix_expr
        self.colon_name = colon_name
        self.args = args


class DoStmt(Stmt):
    def __init__(self, block):
        self.block = block


class WhileStmt(Stmt):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class RepeatStmt(Stmt):
    def __init__(self, block: Block, exp: 'Expr'):
        self.block = block
        self.exp = exp


class IfStmt(Stmt):
    def __init__(self, cond: 'Expr', block, elif_arr: Sequence['ElifStmt'], else_block):
        self.cond = cond
        self.block = block
        self.elif_arr = elif_arr
        self.else_block = else_block


class ElifStmt(Stmt):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class ForStmt(Stmt):
    def __init__(self, init, cond, nxt, block):
        self.init = init
        self.cond = cond
        self.next = nxt
        self.block = block


class ForeachStmt(Stmt):
    def __init__(self, name_list: 'NameList', exp_list: 'ExprList', block):
        self.name_list = name_list
        self.exp_list = exp_list
        self.block = block


class FunctionStmt(Stmt):
    def __init__(self, name: 'FunctionName', args, body: Block):
        self.name = name
        self.args = args
        self.body = body


class LocalFunctionStmt(Stmt):
    def __init__(self, name: TermName, args, body: Block):
        self.name = name
        self.args = args
        self.body = body


class LocalAssignStmt(Stmt):
    def __init__(self, left: TermName, right: 'ExprList'):
        self.left = left
        self.right = right


class LastStmt(Stmt):
    RETURN = 1
    BREAK = 2

    def __init__(self, kind, exp_list: Optional['ExprList']):
        self.kind = kind
        self.exp_list = exp_list

    def is_break(self):
        return self.kind == LastStmt.BREAK

    @staticmethod
    def ret(exp_list):
        return LastStmt(LastStmt.RETURN, exp_list)

    @staticmethod
    def brk():
        return LastStmt(LastStmt.BREAK, None)


# --------------  stmt end ---------------

class FunctionName:
    """
    funcname ::= Name {`.´ Name} [`:´ Name]
    """
    def __init__(self, name: TermName, opt_name: Optional[Sequence[TermName]], colon_name: Optional[TermName]):
        self.name = name
        self.opt_name = opt_name
        self.colon_name = colon_name


class Var:
    """
    var ::=  Name  |  prefixexp `[´ exp `]´  |  prefixexp `.´ Name
    """
    NAME = 1
    BRACKET = 2
    DOT = 3

    def __init__(self, kind, prefix_exp: Optional['PrefixExpr'], exp: Optional['Expr'], name: Optional[TermName]):
        self.kind = kind
        self.prefix_exp = prefix_exp
        self.exp = exp
        self.name = name

    @staticmethod
    def name(name: TermName):
        return Var(Var.NAME, None, None, name)

    @staticmethod
    def bracket(prefix_expr: 'PrefixExpr', expr: 'Expr'):
        return Var(Var.BRACKET, prefix_expr, expr, None)

    @staticmethod
    def dot(prefix_expr: 'PrefixExpr', name: TermName):
        return Var(Var.BRACKET, prefix_expr, None, name)


def var_name(name):
    return Var(TermName(name))


class VarList:
    def __init__(self, var_list: Sequence[Var]):
        self.var_list = var_list


class NameList:
    def __init__(self, *args: 'TermName'):
        self.name_list = args


class ExprEnum(Enum):
    CONSTANT = 1
    PREFIX = 2
    BINOP = 3
    UNOP = 4
    FUNCTION = 5


class Expr:

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
        elif type(value) is FunctionExpr:
            self.kind = ExprEnum.FUNCTION

        self.value = value

    def __str__(self):
        if self.kind == ExprEnum.CONSTANT:
            return f"expr: constant, value= {self.value.__str__()}"
        elif self.kind == ExprEnum.PREFIX:
            return f"expr: prefix , value= {self.value.__str__()}"
        elif self.kind == ExprEnum.BINOP:
            return f"expr: binop, value= {self.value.__str__()}"
        else:
            # self.type == self.UNOP:
            return f"expr: unop, value= {self.value.__str__()}"


class ExprList:
    def __init__(self, *lst: Expr):
        self.expr_list = lst


class PrefixExpr:
    """
    prefixexp ::= var  |  functioncall  |  `(´ exp `)´
    """
    VAR = 1
    FUNCTION_CALL = 2
    PARENTHESES = 3

    def __init__(self, kind, var: Optional['Var'], call: Optional[FunctionCallStmt], exp: Optional[Expr]):
        self.kind = kind
        self.var = var
        self.call = call
        self.exp = exp

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


class Args:
    PARAMS = 1
    TABLE_CONSTRUCT = 2
    STRING = 3

    def __init__(self, kind, params: Optional['ExprList'], table_construct: Optional['TableContructor'],
                 term_string: Optional[TermString]):
        self.kind = kind
        self.params = params
        self.table_construct = table_construct
        self.string = term_string

    @staticmethod
    def params(p: 'ExprList'):
        return Args(Args.PARAMS, p, None, None)

    @staticmethod
    def table_construct(tb: 'TableConstructor'):
        return Args(Args.PARAMS, None, tb, None)

    @staticmethod
    def string(s: TermString):
        return Args(Args.PARAMS, None, None, s)


class FunctionExpr:
    def __init__(self, par_list: 'ParList', block: Block):
        self.par_list = par_list
        self.block = block


class ParList:
    NAME_LIST = 1
    ELLIPSIS = 2

    def __init__(self, kind, name_list: Optional['NameList'], elp: Optional[TermEllipsis]):
        self.kind = kind
        self.name_list = name_list
        self.ellipsis = elp

    @staticmethod
    def name(name_list: 'NameList', elp: Optional[TermEllipsis]):
        return ParList(ParList.NAME_LIST, name_list, elp)

    @staticmethod
    def ellipsis(elp: TermEllipsis):
        return ParList(ParList.ELLIPSIS, None, elp)


class TableConstructor:
    def __init__(self, field_list):
        self.field_list = field_list


class Field:
    BRACKET_ASSIGN = 1
    ASSIGN = 2
    EXP = 3

    def __init__(self, kind, left: Optional[Expr], left_name: Optional[TermName],
                 right: Optional[Expr]):
        self.kind = kind
        self.left = left
        self.left = left_name
        self.right = right

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


class BinOpExpr:
    def __init__(self, op: BinOpEnum, left: Expr, right: Expr):
        self.operator = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.operator} left={{{self.left.__str__()}}}, right={{{self.right.__str__()}}}"

# --------------  expression end ---------------


