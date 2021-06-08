from ast import *
from instruction import Instruction
from lua_opcode import OpCode
from register import RegisterManager


def generate_chuck_stmt(chuck: Chunk):
    pass


def generate_const(term: Terminal):
    if type(term) == TermNil:
        reg = RegisterManager.get_instance().new()
        return Instruction(OpCode.LOADK, reg, 'nil', reg)
    elif type(term) == TermNumber:
        reg = RegisterManager.get_instance().new()
        return Instruction(OpCode.LOADK, reg, term.value, reg)


def generate_expr(exp: Expr):
    if ExprEnum.CONSTANT == exp.kind:
        return generate_const(exp.value)
    elif ExprEnum.BINOP == exp.kind:
        return generate_binary_expr(exp.value)


def generate_var(var: Var):
    if Var.NAME == var.kind:
        # add symbol table
        return Instruction(OpCode.NOP, None, None, 0)
    elif Var.BRACKET == var.kind:
        pass
    elif Var.DOT == var.kind:
        pass


def generate_assign(assign: AssignStmt):
    left = assign.left.var_list
    right = assign.right.expr_list
    if len(left) != len(right):
        raise Exception("count not equal")
    for k, v in enumerate(left):
        return Instruction(OpCode.LOADK, v.value, right[k], v.value)


def generate_binary_expr(binop: BinOpExpr):
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
        reg = RegisterManager.get_instance().new()
        return Instruction(code, generate_expr(binop.right), generate_expr(binop.left), reg)
    elif BinOpEnum.GTE == binop.operator:
        # translate to LT
        code = OpCode.LT
        reg = RegisterManager.get_instance().new()
        return Instruction(code, generate_expr(binop.right), generate_expr(binop.left), reg)
    elif BinOpEnum.EQ == binop.operator:
        code = OpCode.EQ
    elif BinOpEnum.CONCAT == binop.operator:
        code = OpCode.CONCAT
    left = generate_expr(binop.left)
    right = generate_expr(binop.right)
    reg = RegisterManager.get_instance().new()
    return Instruction(code, left, right, reg)


