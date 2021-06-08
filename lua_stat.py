from lua_callinfo import CallInfoStack
from lua_function import Closure


class LuaStat:
    def __init__(self):
        self.status = 1
        self.ip = 0
        self.open_up_value = []
        self.parent = None
        self.ci_stack = CallInfoStack(Closure())


class LuaStatManager:
    __instance = None

    @staticmethod
    def instance() -> 'LuaStatManager':
        if LuaStatManager.__instance is None:
            LuaStatManager.__instance = LuaStat()
        return LuaStatManager.__instance
