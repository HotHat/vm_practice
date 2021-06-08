from symbol_table import SymbolTable


# class Closure:
#     pass


class Protocol:
    pass


class Closure:
    def __init__(self, parent: 'Closure' = None):
        self.parent = parent
        self.opcode = []
        self.constant = []
        self.closure_list = {}
        # upvaluse in lua
        self.up_values = {}
        # local variables and temporary variables
        # self.symbol_table = SymbolTable()


class CallInfo:
    def __init__(self, top, base, func, prev):
        self.top = top
        self.base = base
        self.func = func
        self.prev = prev


class CallInfoStack:
    def __init__(self):
        self.parent = None
        self.current = Closure()

    def enter_block(self):
        self.parent = self.current
        self.current = Closure(self.parent)

    def leave_block(self):
        if self.parent is not None:
            self.current = self.parent
            self.parent = self.parent.parent

    def add_const(self):
        pass


class CallInfoManager:
    __instance = None

    @staticmethod
    def instance() -> 'CallInfoManager':
        if CallInfoManager.__instance is None:
            CallInfoManager.__instance = CallInfoStack()
        return CallInfoManager.__instance
