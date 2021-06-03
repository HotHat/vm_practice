

class RegisterManager:
    __instance = None

    @staticmethod
    def get_instance() -> 'RegisterManager':
        if RegisterManager.__instance is None:
            RegisterManager.__instance = RegisterManager()
        return RegisterManager.__instance

    def __init__(self):
        self.register_arr = []
        self.count = -1

    def new(self):
        self.count = self.count + 1
        return self.count

    def get(self, idx: int):
        return self.register_arr[idx]
