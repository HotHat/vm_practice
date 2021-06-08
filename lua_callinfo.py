from lua_function import Closure


class CallInfo:
    def __init__(self, top, base, func, prev):
        self.top = top
        self.base = base
        self.func = func
        self.prev = prev


class CallInfoStack:
    def __init__(self, main: Closure):
        self.stack = []
        self.current = main

    def push(self):
        self.current = Closure()
        self.stack.append(self.current)

    def pop(self):
        if 0 == len(self.stack):
            raise Exception('call info stack is empty')
        self.current = self.stack.pop()

    def top(self):
        return self.stack[len(self.stack) - 1]
