from ast import *
from instruction import Instruction
from lua_opcode import OpCode
from register import RegisterManager
from lua_function import FuncStat, add_instruction, change_instruction
from symbol_table import Symbol


def generate_stmt(stmt: Stmt):
    if stmt.kind is StmtEnum.LOCAL_ASSIGN:
        generate_local_assign(stmt.value)
    # TODO: other stmt


def generate_chuck_stmt(chunk: Chunk):
    for stmt in chunk.stat_arr:
        generate_stmt(stmt)


def generate_const(term: Terminal):
    idx = FuncStat.instance().constant_pool.add(term)
    reg = FuncStat.instance().symbol_stack.add_temp_var()
    add_instruction(Instruction(OpCode.LOADK, reg, idx))
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


def generate_expr(expr: Expr):
    if ExprEnum.CONSTANT == expr.kind:
        return generate_const(expr.value)
    elif ExprEnum.BINOP == expr.kind:
        if BinOpEnum.AND == expr.value.operator:
            reg = generate_login_and_expr(expr.value)
            expr.false_list = expr.value.left.false_list
            return reg
        elif BinOpEnum.OR == expr.value.operator:
            reg = generate_login_or_expr(expr.value)
            expr.true_list = expr.value.left.true_list
            return reg
        return generate_binary_expr(expr.value)


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

        if ExprEnum.BINOP == val.kind and BinOpEnum.AND == val.value.operator:
            pc = FuncStat.instance().pc()
            _back_path(val.false_list, pc)

        elif ExprEnum.BINOP == val.kind and BinOpEnum.OR == val.value.operator:
            pc = FuncStat.instance().pc()
            _back_path(val.true_list, pc)

        code = Instruction(OpCode.LOADK, res.index, reg_right)
        add_instruction(code)

    # if len(left) != len(right):
    #     raise Exception("count not equal")
    # for k, v in enumerate(left):
    #     return Instruction(OpCode.LOADK, v.value, right[k], v.value)


def generate_login_and_expr(expr: BinOpExpr):
    left = generate_expr(expr.left)
    tmp = FuncStat.instance().symbol_stack.add_temp_var()
    add_instruction(Instruction(OpCode.MOVE, tmp, left))
    # B1 AND B2 => if B1 = true jump to B2
    add_instruction(Instruction(OpCode.TEST, left, 0))
    # if B1 false jump to end
    add_instruction(Instruction(OpCode.JMP, 0, 0))
    jump_index = FuncStat.instance().pc()
    # record left expr false list
    expr.left.false_list.append(jump_index)

    right = generate_expr(expr.right)
    add_instruction(Instruction(OpCode.MOVE, tmp, right))
    # record right expr true list
    jump_index = FuncStat.instance().pc()
    expr.right.false_list.append(jump_index)
    return tmp


# def __generate_login_and_or_expr(expr: BinOpExpr):
#     left = generate_expr(expr.left)
#     if BinOpEnum.AND == expr.operator:
#         FuncStat.instance().opcode.append(Instruction(OpCode.TEST, left, 0))
#     else:
#         FuncStat.instance().opcode.append(Instruction(OpCode.TEST, left, 1))
#     FuncStat.instance().opcode.append(Instruction(OpCode.JMP, 0, 0))
#     jump_index = FuncStat.instance().pc()
#     right = generate_expr(expr.right)
#     pc = FuncStat.instance().pc()
#     FuncStat.instance().change_opcode(jump_index, Instruction(OpCode.JMP, 0, pc - jump_index))
#     return right


def generate_login_or_expr(expr: BinOpExpr):
    left = generate_expr(expr.left)
    # B1 or B2 => if B1 = false jump to B2
    FuncStat.instance().opcode.append(Instruction(OpCode.TEST, left, 1))
    # if B1 true jump to end
    FuncStat.instance().opcode.append(Instruction(OpCode.JMP, 0, 0))
    # record left expr true list
    jump_index = FuncStat.instance().pc()
    expr.left.true_list.append(jump_index)

    right = generate_expr(expr.right)
    # record right expr true list
    jump_index = FuncStat.instance().pc()
    expr.right.true_list.append(jump_index)

    return right


def _back_path(lst, pc):
    for p in lst:
        FuncStat.instance().change_opcode(p, Instruction(OpCode.JMP, 0, pc - p + 1))


def generate_elif(el: ElifStmt):
    pass


def generate_if_expr(if_stmt: IfStmt):
    cond = if_stmt.cond
    test = generate_expr(cond)
    add_instruction(Instruction(OpCode.TEST, test, 0))
    add_instruction(Instruction(OpCode.JMP, 0, 0))
    cond.false_list.append(FuncStat.instance().pc())
    # then S1
    # M1
    # _back_path(cond.true_list, FuncStat.instance().pc())
    generate_block(if_stmt.block)

    if if_stmt.elif_arr or if_stmt.else_block:
        add_instruction(Instruction(OpCode.JMP, 0, 0))
        if_stmt.block.next_list.append(FuncStat.instance().pc())

    # M1
    _back_path(cond.false_list, FuncStat.instance().pc())

    cur_test = cond
    # elif block
    if if_stmt.elif_arr:
        for el in if_stmt.elif_arr:
            _back_path(cur_test.false_list, FuncStat.instance().pc())
            cur_test = el.cond
            tes = generate_expr(cur_test)
            add_instruction(Instruction(OpCode.TEST, tes, 0))
            add_instruction(Instruction(OpCode.JMP, 0, 0))
            generate_block(el.block)
            el.block.next_list.append(FuncStat.instance().pc())

    # elif blocks
    if if_stmt.elif_arr:
        for el in if_stmt.elif_arr:
            _back_path(el.block.next_list, FuncStat.instance().pc())

    # else block
    if if_stmt.else_block:
        generate_block(if_stmt.else_block)
        _back_path(if_stmt.block.next_list, FuncStat.instance().pc())
    else:
        # N
        _back_path(if_stmt.block.next_list, FuncStat.instance().pc())
        _back_path(cur_test.false_list, FuncStat.instance().pc())


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
    add_instruction(Instruction(code, left, left, right))
    return left


def generate_block(block: Block):
    chunk = block.chunk
    return generate_chuck_stmt(chunk)









