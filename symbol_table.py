
class SymbolTable:
    def __init__(self, parent: 'SymbolTable' = None):
        self.parent = parent
        self.table = {}

    def insert(self, symbol, value):
        self.table[symbol] = value

    def lookup(self, symbol):
        if symbol in self.table:
            return self.table[symbol]
        if self.parent:
            return self.parent.lookup(symbol)
        return None


class ComponentSymbolTable:
    def __init__(self, parent: 'ComponentSymbolTable' = None):
        self.parent = parent
        # constant symbol table
        self.const_table = {}
        # variable symbol table
        self.var_table = {}

    def insert_const(self, symbol, value):
        self.const_table[symbol] = value

    def insert_var(self, symbol, value):
        self.var_table[symbol] = value

    def lookup_const(self, symbol):
        if symbol in self.const_table:
            return self.const_table[symbol]
        if self.parent:
            return self.parent.lookup_const(symbol)
        return None

    def lookup_var(self, symbol):
        if symbol in self.var_table:
            return self.var_table[symbol]
        if self.parent:
            return self.parent.lookup_var(symbol)
        return None
