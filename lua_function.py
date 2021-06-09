from symbol_table import SymbolTable, SymbolTableStack
from constant_pool import ConstantPool


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

    def print(self):
        print('--------symbol stack-------')
        for i in self.opcode:
            print(i)
        print('--------symbol stack-------')
        self.symbol_stack.print()
        print('--------constant pool-------')
        self.constant_pool.print()
        print('--------constant end pool-------')
