from symbol_table import SymbolTable


# class Closure:
#     pass


class Protocol:
    pass


class Closure:
    def __init__(self):
        self.opcode = []
        self.constant = []
        self.closure_list = {}
        # upvaluse in lua
        self.up_values = {}
        # local variables and temporary variables
        # self.symbol_table = SymbolTable()


class FuncStat:
    pass
