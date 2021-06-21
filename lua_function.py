from symbol_table import SymbolTable, SymbolTableStack
from constant_pool import ConstantPool
from instruction import Instruction
from ast import Block


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

    def pc(self):
        return len(self.instruction) - 1

    def change_instruction(self, pc, instruction: Instruction):
        self.instruction[pc] = instruction


class Closure:
    def __init__(self, proto: Protocol = None):
        self.proto = Protocol()
        # up value in lua
        self.up_values = {}

    def add_up_value(self, name, value):
        self.up_values[name] = value


class FuncStat:
    # __instance = None
    #
    # @staticmethod
    # def instance(block: Block) -> 'FuncStat':
    #     if FuncStat.__instance is None:
    #         FuncStat.__instance = FuncStat(block)
    #     return FuncStat.__instance

    def __init__(self, block: Block):
        self.proto = Protocol()
        self.prev = None
        self.block = block
        self.pc = 0
        self.number_constant = 0
        self.number_active_var = 0
        self.number_up_value = 0

        self.symbol_stack = SymbolTable()
        self.constant_pool = ConstantPool()
        self.instruction = []

    def pc(self):
        return len(self.instruction) - 1

    def change_opcode(self, pc, instruction: Instruction):
        self.instruction[pc] = instruction

    def print(self):
        print('--------Instruction array-------')
        for k, v in enumerate(self.instruction):
            print(f"{k:<5}    {v}")
        print('--------symbol stack-------')
        self.symbol_stack.print()
        print('--------constant pool-------')
        self.constant_pool.print()
        print('--------constant end pool-------')


def add_instruction(instruction: Instruction):
    FuncStat.instance().instruction.append(instruction)


def change_instruction(pc, instruction: Instruction):
    FuncStat.instance().change_opcode(pc, instruction)

