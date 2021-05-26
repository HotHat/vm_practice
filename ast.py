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
         function  |  prefixexp  |  tableconstructor  |  exp binop exp  |  unop exp

prefixexp ::= var  |  functioncall  |  `(´ exp `)´

functioncall ::=  prefixexp args  |  prefixexp `:´ Name args

args ::=  `(´ [explist1] `)´  |  tableconstructor  |  String

function ::= function funcbody

funcbody ::= `(´ [parlist1] `)´ block end

parlist1 ::= namelist [`,´ `...´]  |  `...´

tableconstructor ::= `{´ [fieldlist] `}´

fieldlist ::= field {fieldsep field} [fieldsep]

field ::= `[´ exp `]´ `=´ exp  |  Name `=´ exp  |  exp

fieldsep ::= `,´  |  `;´

binop ::= `+´  |  `-´  |  `*´  |  `/´  |  `^´  |  `%´  |  `..´  |

         `<´  |  `<=´  |  `>´  |  `>=´  |  `==´  |  `~=´  |
         and  |  or

unop ::= `-´  |  not  |  `#´
"""
from collections.abc import Sequence
from typing import Optional


class Expr:
    CONSTANT = 1
    PREFIX = 2
    BINOP = 3
    UNOP = 4
    FUNCTION = 5

    def __init__(self, value):
        if type(value) is Constant:
            self.kind = Expr.CONSTANT
        elif type(value) is PrefixExpr:
            self.kind = Expr.PREFIX
        elif type(value) is BinOpExpr:
            self.kind = Expr.BINOP
        elif type(value) is FunctionExpr:
            self.kind = Expr.FUNCTION

        self.value = value

    def __str__(self):
        if self.type == self.CONSTANT:
            return f"expr: constant, value= {self.value.__str__()}"
        elif self.type == self.PREFIX:
            return f"expr: prefix , value= {self.value.__str__()}"
        elif self.type == self.BINOP:
            return f"expr: binop, value= {self.value.__str__()}"
        else:
            # self.type == self.UNOP:
            return f"expr: unop, value= {self.value.__str__()}"


class ExprList:
    def __init__(self, *lst: Expr):
        self.expr_list = lst


class FunctionCall:
    """
    functioncall ::=  prefixexp args  |  prefixexp `:´ Name args
    """
    def __init__(self, prefix_expr: 'PrefixExpr', colon_name: Optional['Name'], args):
        self.prefix_expr = prefix_expr
        self.colon_name = colon_name
        self.args = args


class PrefixExpr(Expr):
    """
    prefixexp ::= var  |  functioncall  |  `(´ exp `)´
    """
    VAR = 1
    FUNCTION_CALL = 2
    PARENTHESES = 3

    def __init__(self, value):
        if type(value) is Var:
            self.kind = PrefixExpr.VAR
        elif type(value) is FunctionCall:
            self.kind = PrefixExpr.FUNCTION_CALL
        elif type(value) is Expr:
            self.kind = PrefixExpr.PARENTHESES

        self.value = value


class BinOpExpr(Expr):
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

    def __init__(self, op, left: Expr, right: Expr):
        self.operator = op
        self.left = left
        self.right = right

    def __kind_str(self, op):
        op_map = {
            self.ADD: 'ADD',
            self.SUB: 'SUB',
            self.MUL: 'MUL',
            self.DIV: 'DIV',
            self.XOR: 'XOR',
            self.MOD: 'MOD',
            self.LT: 'LT',
            self.LTE: 'LTE',
            self.GT: 'GT',
            self.GTE: 'GTE',
            self.EQ:  'EQ',
            self.CONCAT: 'CONCAT',
            self.ASSIGN_XOR: 'ASSIGN_XOR'
        }
        return op_map[op]

    def __str__(self):
        return f"{self.__kind_str(self.operator)} left={{{self.left.__str__()}}}, right={{{self.right.__str__()}}}"


class FunctionExpr(Expr):
    pass


class Name:
    def __init__(self, name):
        self.name = name


def var_name(name):
    return Var(Name(name))


def prefix_name(name):
    return PrefixExpr(Var(Name(name)))


class NameList:
    def __init__(self, *args: Name):
        self.name_list = args


class FunctionName:
    """
    funcname ::= Name {`.´ Name} [`:´ Name]
    """
    def __init__(self, name: Name, opt_name: Optional[Sequence[Name]], colon_name: Optional[Name]):
        self.name = name
        self.opt_name = opt_name
        self.colon_name = colon_name


class Constant:
    NIL = 1
    FALSE = 2
    TRUE = 3
    NUMBER = 4
    STRING = 5
    ELLIPSIS = 6

    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

    def __str__(self):
        return str(self.value)


NIL = Expr(Constant(Constant.NIL, 'nil'))
FALSE = Expr(Constant(Constant.FALSE, 'false'))
TRUE = Expr(Constant(Constant.TRUE, 'true'))
ELLIPSIS = Expr(Constant(Constant.ELLIPSIS, '...'))


def number(n):
    return Expr(Constant(Constant.NUMBER, n))


def string(s):
    return Expr(Constant(Constant.STRING, s))


class BlockStmt:
    def __init__(self, chunk):
        self.chunk = chunk


class Stmt:
    pass


class ChunkStmt:
    def __init__(self, stat_arr: Sequence[Stmt], last_stat):
        self.stat_arr = stat_arr
        self.last_stat = last_stat


class FunctionStmt(Stmt):
    def __init__(self, name, args, body, is_local):
        self.name = name
        self.args = args
        self.body = body
        self.is_local = is_local


class ElifStmt(Stmt):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class IfStmt(Stmt):
    def __init__(self, cond: Expr, block, elif_arr: Sequence[ElifStmt], else_block):
        self.cond = cond
        self.block = block
        self.elif_arr = elif_arr
        self.else_block = else_block


class WhileStmt(Stmt):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class ForStmt(Stmt):
    def __init__(self, init, cond, nxt, block):
        self.init = init
        self.cond = cond
        self.next = nxt
        self.block = block


class AssignStmt(Stmt):
    def __init__(self, left, right: ExprList, is_local):
        self.left = left
        self.right = right
        self.is_local = is_local


class Var:
    """
    var ::=  Name  |  prefixexp `[´ exp `]´  |  prefixexp `.´ Name
    """
    NAME = 1
    BRACKET = 2
    DOT = 3

    def __init__(self, value):
        if type(value) is Name:
            self.kind = Var.NAME
        elif type(value) is BracketVar:
            self.kind = Var.BRACKET
        elif type(value) is DotVar:
            self.kind = Var.DOT

        self.value = value


class VarList:
    def __init__(self, var_list: Sequence[Var]):
        self.var_list = var_list


class BracketVar(Var):
    def __init__(self, prefix_expr: Expr, expr: Expr):
        self.prefix_expr = prefix_expr
        self.name = expr


def prefix_bracket(prefix_expr: Expr, expr: Expr):
    return PrefixExpr(Var(BracketVar(prefix_expr, expr)))


class DotVar(Var):
    """
    var ::=  Name  |  prefixexp `[´ exp `]´  |  prefixexp `.´ Name
    """
    def __init__(self, prefix_expr, name: Name):
        self.prefix_expr = prefix_expr
        self.name = name


def prefix_dot(prefix_expr: Expr, name: Name):
    return PrefixExpr(Var(DotVar(prefix_expr, name)))

