from symbol_table import SymbolTable, SymbolTableStack
from constant_pool import ConstantPool
from instruction import Instruction


# class Closure:
#     pass


class Protocol:
    pass


class Closure:
    def __init__(self):
        self.opcode = []
        self.constant_pool = []
        self.closure_list = {}
        # upvaluse in lua
        self.up_values = {}
        # local variables and temporary variables
        # self.symbol_table = SymbolTable()


class FuncStat:
    __instance = None

    @staticmethod
    def instance() -> 'FuncStat':
        if FuncStat.__instance is None:
            FuncStat.__instance = FuncStat()
        return FuncStat.__instance

    def __init__(self):
        self.symbol_stack = SymbolTable()
        self.constant_pool = ConstantPool()
        self.opcode = []

    def pc(self):
        return len(self.opcode) - 1

    def change_opcode(self, pc, instruction: Instruction):
        self.opcode[pc] = instruction

    def print(self):
        print('--------Instruction array-------')
        for k, v in enumerate(self.opcode):
            print(f"{k:<5}    {v}")
        print('--------symbol stack-------')
        self.symbol_stack.print()
        print('--------constant pool-------')
        self.constant_pool.print()
        print('--------constant end pool-------')
