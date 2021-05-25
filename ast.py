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


class Stmt:
    pass

    # exp: := nil | false | true | Number | String | `...´ |
    # function | prefixexp | tableconstructor | exp
    # binop
    # exp | unop
    # exp


class Expr:
    CONSTANT = 1
    PREFIX = 2
    BINOP = 3
    UNOP = 4

    def __init__(self, t, value):
        self.type = t
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


class BinOp:
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


class Constant:
    NIL = 1
    FALSE = 2
    TRUE = 3
    NUMBER = 4
    STRING = 5

    def __init__(self, t, value=None):
        self.type = t
        self.value = value

    def __str__(self):
        return str(self.value)


def gen_const_nil() -> Constant:
    return Constant(Constant.NIL)


def gen_const_false() -> Constant:
    return Constant(Constant.FALSE, False)


def gen_const_true() -> Constant:
    return Constant(Constant.FALSE, True)


def gen_const_string(s) -> Constant:
    return Constant(Constant.STRING, s)


def gen_const_number(n) -> Constant:
    return Constant(Constant.NUMBER, n)


def gen_expr_const(c:  Constant) -> Expr:
    return Expr(Expr.CONSTANT, c)


def gen_expr_prefix(c):
    return Expr(Expr.PREFIX, c)


def gen_expr_binop(kind, left: Expr, right: Expr) -> Expr:
    return Expr(Expr.BINOP, BinOp(kind, left, right))


def gen_expr_unop(value: Expr) -> Expr:
    return Expr(Expr.UNOP, value)


