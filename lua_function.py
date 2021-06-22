from symbol_table import SymbolTable, SymbolTableStack
from constant_pool import ConstantPool
from instruction import Instruction
from ast import *
from lua_opcode import OpCode
from symbol_table import Symbol


# class Closure:
#     pass
class UpVal:
    def __init__(self):
        # points to stack or to its own value
        self.v = None
        self.ref_count = 0
        self.next = None
        self.touched = True
        self.is_open = False
        self.value = None


class Protocol:
    def __init__(self):
        self.number_params = 0
        self.is_vararg = False
        self.max_stack_size = 0
        self.size_up_values = 0
        self.size_constant = 0
        self.size_code = 0
        # opcodes
        self.instruction = []
        # constants used by the function
        self.constant_pool = []
        # functions defined inside the function
        self.proto = []
        # up value information
        self.up_value_desc = []
        # local variables
        self.loc_var = []

    def add_instruction(self, instruction: Instruction):
        self.instruction.append(instruction)

    def pc(self):
        return len(self.instruction) - 1

    def change_instruction(self, pc, instruction: Instruction):
        self.instruction[pc] = instruction

    def print(self):
        for k, v in enumerate(self.instruction):
            print(f"{k:<5}    {v}")


class Closure:
    def __init__(self, proto: Protocol = None):
        self.proto = Protocol()
        # up value in lua
        self.up_values = {}

    def add_up_value(self, name, value):
        self.up_values[name] = value


class FuncStat:
    def __init__(self, block: Block):
        self.proto = Protocol()
        self.prev = None
        self.block = block
        self.pc = 0
        self.number_constant = 0
        self.number_active_var = 0
        self.number_up_value = 0

        # symbol table stack
        if self.prev is not None:
            self.symbol_table = SymbolTable(self.prev.symbol_table)
        else:
            self.symbol_table = SymbolTable()

        self.constant_pool = ConstantPool()

    def get_main_proto(self):
        if self.prev is None:
            return self.proto
        return None

    def enter_func_stat(self):
        pass

    def leave_func_stat(self):
        pass

    def generate_opcode(self):
        self.generate_block(self.block)

    def generate_block(self, block: Block):
        self.generate_chuck_stmt(block.chunk)
        self.proto.add_instruction(Instruction(OpCode.RETURN, 0, 2))

    def generate_chuck_stmt(self, chunk: Chunk):
        for stmt in chunk.stat_arr:
            self.generate_stmt(stmt)

    def generate_stmt(self, stmt: Stmt):
        if stmt.kind is StmtEnum.LOCAL_ASSIGN:
            self.generate_local_assign(stmt.value)
        # TODO: other stmt

    def generate_const(self, term: Terminal):
        idx = self.constant_pool.add(term)
        return idx

    def generate_name(self, term: TermName):
        """
        1) local variable
        2) up values
        3) top variable
        :param term:
        :return:
        """
        lookup = self.symbol_table.lookup(term.value)
        return lookup

    def _back_path(self, lst):
        pc = self.proto.pc()
        for p in lst:
            self.proto.change_instruction(p, Instruction(OpCode.JMP, 0, pc - p + 1))

    def generate_login_and_expr(self, register, expr: BinOpExpr):
        self.generate_expr(register, expr.left)
        # B1 AND B2 => if B1 = true jump to B2
        self.proto.add_instruction(Instruction(OpCode.TEST, register, 0))
        # if B1 false jump to end
        self.proto.add_instruction(Instruction(OpCode.JMP, 0, 0))
        jump_index = self.proto.pc()
        # record left expr false list
        expr.left.false_list.append(jump_index)

        self.generate_expr(register, expr.right)
        # record right expr true list
        jump_index = self.proto.pc()
        expr.right.false_list.append(jump_index)

    def generate_login_or_expr(self, register, expr: BinOpExpr):
        self.generate_expr(register, expr.left)
        # B1 or B2 => if B1 = false jump to B2
        self.proto.add_instruction(Instruction(OpCode.TEST, register, 1))
        # if B1 true jump to end
        self.proto.add_instruction(Instruction(OpCode.JMP, 0, 0))
        # record left expr true list
        expr.left.true_list.append(self.proto.pc())

        self.generate_expr(register, expr.right)
        # record right expr true list
        expr.right.true_list.append(self.proto.pc())

    def generate_equal_expr(self, register, expr: BinOpExpr):
        self._generate_equal_expr(register, OpCode.EQ, expr)

    def generate_not_equal_expr(self, register, expr: BinOpExpr):
        self._generate_not_equal_expr(register, OpCode.EQ, expr)

    def generate_less_then_expr(self, register, expr: BinOpExpr):
        self._generate_equal_expr(register, OpCode.LT, expr)

    def generate_less_equal_expr(self, register, expr: BinOpExpr):
        self._generate_equal_expr(register, OpCode.LE, expr)

    def generate_greater_then_expr(self, register, expr: BinOpExpr):
        self._generate_not_equal_expr(register, OpCode.LE, expr)

    def generate_greater_equal_expr(self, register, expr: BinOpExpr):
        self._generate_not_equal_expr(register, OpCode.LT, expr)

    def _generate_not_equal_expr(self, register, opcode: OpCode, expr: BinOpExpr):
        left_reg = self.symbol_table.add_temp_var()
        self.generate_expr(left_reg, expr.left)
        right_reg = self.symbol_table.add_temp_var()
        self.generate_expr(right_reg, expr.right)
        self.proto.add_instruction(Instruction(opcode, 0, left_reg, right_reg))
        self.proto.add_instruction(Instruction(OpCode.JMP, 0, 1))
        self.proto.add_instruction(Instruction(OpCode.LOADBOOL, register, 0, 1))
        self.proto.add_instruction(Instruction(OpCode.LOADBOOL, register, 1, 0))

    def _generate_equal_expr(self, register, opcode: OpCode, expr: BinOpExpr):
        left_reg = self.symbol_table.add_temp_var()
        self.generate_expr(left_reg, expr.left)
        right_reg = self.symbol_table.add_temp_var()
        self.generate_expr(right_reg, expr.right)
        self.proto.add_instruction(Instruction(opcode, 1, left_reg, right_reg))
        self.proto.add_instruction(Instruction(OpCode.JMP, 0, 1))
        self.proto.add_instruction(Instruction(OpCode.LOADBOOL, register, 1, 1))
        self.proto.add_instruction(Instruction(OpCode.LOADBOOL, register, 0, 0))

    def generate_binary_expr(self, register, binop: BinOpExpr):
        if BinOpEnum.ADD == binop.operator:
            pass
        elif BinOpEnum.SUB == binop.operator:
            pass
        elif BinOpEnum.MUL == binop.operator:
            pass
        elif BinOpEnum.DIV == binop.operator:
            pass
        elif BinOpEnum.XOR == binop.operator:
            pass
        elif BinOpEnum.MOD == binop.operator:
            pass
        elif BinOpEnum.LT == binop.operator:
            self.generate_less_then_expr(register, binop)
        elif BinOpEnum.LTE == binop.operator:
            self.generate_less_equal_expr(register, binop)
        elif BinOpEnum.GT == binop.operator:
            self.generate_greater_then_expr(register, binop)
        elif BinOpEnum.GTE == binop.operator:
            self.generate_greater_equal_expr(register, binop)
        elif BinOpEnum.EQ == binop.operator:
            self.generate_equal_expr(register, binop)
        elif BinOpEnum.CONCAT == binop.operator:
            pass
        elif BinOpEnum.AND == binop.operator:
            self.generate_login_and_expr(register, binop)
        elif BinOpEnum.OR == binop.operator:
            self.generate_login_or_expr(register, binop)

    def generate_expr(self, register, expr: Expr):
        if ExprEnum.CONSTANT == expr.kind:
            k = self.generate_const(expr.value)
            self.proto.add_instruction(Instruction(OpCode.LOADK, register, k))

        elif ExprEnum.BINOP == expr.kind:
            if BinOpEnum.AND == expr.value.operator:
                self.generate_login_and_expr(register, expr.value)
                expr.false_list = expr.value.left.false_list
            elif BinOpEnum.OR == expr.value.operator:
                self.generate_login_or_expr(register, expr.value)
                expr.true_list = expr.value.left.true_list
            elif expr.value.operator in [BinOpEnum.GT, BinOpEnum.GTE, BinOpEnum.LT, BinOpEnum.LTE]:
                self.generate_binary_expr(register, expr.value)
            else:
                self.generate_binary_expr(register, expr.value)

    def generate_local_assign(self, assign: LocalAssignStmt):
        left = assign.left.name_list
        right = assign.right.expr_list
        # left -- add local variable
        # for name in left:
        # right -- calc value and assign to left variable
        for idx, name in enumerate(left):
            register = self.symbol_table.insert(name.value, name)
            # res = self.symbol_table.lookup(name.value)
            val = right[idx]
            self.generate_expr(register, val)

            if ExprEnum.BINOP == val.kind and BinOpEnum.AND == val.value.operator:
                self._back_path(val.false_list)

            elif ExprEnum.BINOP == val.kind and BinOpEnum.OR == val.value.operator:
                self._back_path(val.true_list)

            # code = Instruction(OpCode.LOADK, res.index, reg_right)
            # self.add_instruction(code)

    def print(self):
        print('--------Instruction array-------')
        self.proto.print()
        print('--------symbol stack-------')
        self.symbol_table.print()
        print('--------constant pool-------')
        self.constant_pool.print()

