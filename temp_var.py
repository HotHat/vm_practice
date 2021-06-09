

class TempVar:
    __instance = None

    @staticmethod
    def instance() -> 'TempVar':
        if TempVar.__instance is None:
            TempVar.__instance = TempVar()
        return TempVar.__instance

    def __init__(self):
        self.counter = -1

    def new(self):
        self.counter += 1
        return f"{self.counter}_temp_var"

