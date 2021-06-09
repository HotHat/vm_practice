from ast import TermNil, TermString, TermNumber, TermTrue, TermFalse


class ConstantPool:
    __instance = None

    @staticmethod
    def instance() -> 'ConstantPool':
        if ConstantPool.__instance is None:
            ConstantPool.__instance = ConstantPool()
        return ConstantPool.__instance

    def __init__(self):
        self.pool = []
        self.count = 0

    def add(self, item):
        try:
            self.pool.index(item)
        except ValueError:
            self.pool.append(item)
            self.count += 1
        return 0 - self.count

    def index(self, item):
        for k, v in enumerate(self.pool):
            if type(item) == type(v):
                if type(item) == TermNil or type(item) == TermTrue or type(item) == TermFalse:
                    return k
                elif type(item) == TermNumber or type(item) == TermString:
                    if item.value == v.value:
                        return k
        return None

    def print(self):
        for i in self.pool:
            print(i)
