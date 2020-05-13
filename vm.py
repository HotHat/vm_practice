from my_opcode import *


class VM:
    VM_OK = 1
    VM_COMPILE_ERROR = 2
    VM_RUNTIME_ERROR = 3

    def __init__(self):
        self.instructions = []
        self.ip = 0
        self.stack = []
        self.constants = []

    def add_opcode(self, code):
        self.instructions.append(code)

    def add_constant(self, value):
        try:
            idx = self.constants.index(value)
        except ValueError:
            self.constants.append(value)
            idx = len(self.constants) - 1
        return idx

    def run(self):
        op_len = len(self.instructions)

        while self.ip != op_len:
            code = self.instructions[self.ip]
            self.ip = self.ip + 1

            if type(code) is OpReturn:
                return self.VM_OK

            elif type(code) is OpConstant:
                index = code.get_index()
                value = self.constants[index]
                self.stack.append(value)

            elif type(code) is OpAdd:
                first = self.stack.pop()
                second = self.stack.pop()
                self.stack.append(first + second)

            elif type(code) is OpSub:
                first = self.stack.pop()
                second = self.stack.pop()
                self.stack.append(first - second)

            elif type(code) is OpMUL:
                first = self.stack.pop()
                second = self.stack.pop()
                self.stack.append(first * second)

            elif type(code) is OpDiv:
                first = self.stack.pop()
                second = self.stack.pop()
                self.stack.append(second / first)

            elif type(code) is OpEcho:
                value = self.stack.pop()
                print(value)

            else:
                return self.VM_RUNTIME_ERROR
