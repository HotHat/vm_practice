from ast import *
from tac import Tac
from lua_opcode import OpCode
from register import RegisterManager


def generate_chuck_stmt(chuck: Chunk):
    pass


def generate_const(term: Terminal):
    if type(term) == TermNil:
        reg = RegisterManager.get_instance().new()
        return Tac(OpCode.LOADK, reg, 'nil')
    elif type(term) == TermNumber:
        reg = RegisterManager.get_instance().new()
        return Tac(OpCode.LOADK, reg, term.value)


def generate_expr(exp: Expr):
    if ExprEnum.CONSTANT == exp.kind:
        return generate_const(exp.value)
    elif ExprEnum.BINOP == exp.kind:
        return generate_binop_expr(exp.value)


def generate_binop_expr(binop: BinOpExpr):
    code = None
    if BinOpEnum.ADD == binop.operator:
        code = OpCode.ADD
    elif BinOpEnum.SUB == binop.operator:
        code = OpCode.SUB
    elif BinOpEnum.MUL == binop.operator:
        code = OpCode.MUL
    elif BinOpEnum.DIV == binop.operator:
        code = OpCode.DIV
    elif BinOpEnum.XOR == binop.operator:
        code = OpCode.BXOR
    elif BinOpEnum.MOD == binop.operator:
        code = OpCode.MOD
    elif BinOpEnum.LT == binop.operator:
        code = OpCode.LT
    elif BinOpEnum.LTE == binop.operator:
        code = OpCode.LE
    elif BinOpEnum.GT == binop.operator:
        # translate to LE
        code = OpCode.LE
        return Tac(code, generate_expr(binop.right), generate_expr(binop.left), 'RESULT')
    elif BinOpEnum.GTE == binop.operator:
        # translate to LT
        code = OpCode.LT
        return Tac(code, generate_expr(binop.right), generate_expr(binop.left), 'RESULT')
    elif BinOpEnum.EQ == binop.operator:
        code = OpCode.EQ
    elif BinOpEnum.CONCAT == binop.operator:
        code = OpCode.CONCAT
    left = generate_expr(binop.left)
    right = generate_expr(binop.right)
    reg = RegisterManager.get_instance().new()
    return Tac(code, reg, left, right)


