from ast import *
from instruction import Instruction
from lua_opcode import OpCode
from register import RegisterManager
from lua_function import FuncStat
from symbol_table import Symbol


def generate_chuck_stmt(chuck: Chunk):
    pass


def generate_const(term: Terminal):
    idx = FuncStat.instance().constant_pool.add(term)
    reg = FuncStat.instance().symbol_stack.add_temp_var()
    FuncStat.instance().opcode.append(Instruction(OpCode.LOADK, reg, idx))
    return reg
    # if type(term) == TermNil or type(term) == TermNumber:
    #     idx = FuncStat.instance().constant_pool.add(term)
    #     reg = FuncStat.instance().symbol_stack.add_temp_var()
    #     FuncStat.instance().opcode.append(Instruction(OpCode.LOADK, reg, idx))
    #     return reg
    # elif type(term) == TermNil:
    #     pass
    #
    # if type(term) == TermNil:
    #     reg = RegisterManager.get_instance().new()
    #     return Instruction(OpCode.LOADK, reg, 'nil')
    # elif type(term) == TermNumber:
    #     idx = FuncStat.instance().constant_pool.add(term)
    #     reg = FuncStat.instance().symbol_stack.add_temp_var()
    #     return Instruction(OpCode.LOADK, reg, idx)


def generate_expr(exp: Expr):
    if ExprEnum.CONSTANT == exp.kind:
        return generate_const(exp.value)
    elif ExprEnum.BINOP == exp.kind:
        return generate_binary_expr(exp.value)


def generate_name(name: TermName):
    # if Var.NAME == name.kind:
    FuncStat.instance().symbol_stack.insert(Symbol(name.value))
        # return Instruction(OpCode.NOP, None, None, 0)
    # elif Var.BRACKET == name.kind:
    #     pass
    # elif Var.DOT == name.kind:
    #     pass


def generate_local_assign(assign: LocalAssignStmt):
    left = assign.left.name_list
    right = assign.right.expr_list
    # left -- add local variable
    for name in left:
        generate_name(name)
    # right -- calc value and assign to left variable
    for idx, name in enumerate(left):
        res = FuncStat.instance().symbol_stack.lookup(Symbol(name.value))
        val = right[idx]
        reg_right = generate_expr(val)
        code = Instruction(OpCode.LOADK, res.index, reg_right)
        FuncStat.instance().opcode.append(code)

    # if len(left) != len(right):
    #     raise Exception("count not equal")
    # for k, v in enumerate(left):
    #     return Instruction(OpCode.LOADK, v.value, right[k], v.value)


def generate_login_and_expr(expr: BinOpExpr):
    return __generate_login_and_or_expr(expr)


def __generate_login_and_or_expr(expr: BinOpExpr):
    left = generate_expr(expr.left)
    if BinOpEnum.AND == expr.operator:
        FuncStat.instance().opcode.append(Instruction(OpCode.TEST, left, 0))
    else:
        FuncStat.instance().opcode.append(Instruction(OpCode.TEST, left, 1))
    FuncStat.instance().opcode.append(Instruction(OpCode.JMP, 0, 0))
    jump_index = FuncStat.instance().pc() - 1
    right = generate_expr(expr.right)
    pc = FuncStat.instance().pc()
    FuncStat.instance().change_opcode(jump_index, Instruction(OpCode.JMP, 0, pc - jump_index))
    return right


def generate_login_or_expr(expr: BinOpExpr):
    return __generate_login_and_or_expr(expr)


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
    elif BinOpEnum.AND == binop.operator:
        return generate_login_and_expr(binop)

    elif BinOpEnum.OR == binop.operator:
        return generate_login_or_expr(binop)

    left = generate_expr(binop.left)
    right = generate_expr(binop.right)
    # reg = FuncStat.instance().symbol_stack.add_temp_var()
    FuncStat.instance().opcode.append(Instruction(code, left, left, right))
    return left


