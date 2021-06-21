from lua_function import Closure
from symbol_table import SymbolTable


class Machine:
    __instance = None

    @staticmethod
    def instance() -> 'Machine':
        if Machine.__instance is None:
            Machine.__instance = Machine()
        return Machine.__instance

    def __init__(self):
        self.main_closure = Closure()
        self.symbol_table = SymbolTable()
        self.env = {}

