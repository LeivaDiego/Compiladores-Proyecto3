class Symbol():
    """
    Symbol class represents a symbol in the symbol table.
    """
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.scope = None
        self.offset = None

class Variable(Symbol):
    """
    Variable class represents a variable in the symbol table
    """
    def __init__(self, id, type="var"):
        super().__init__(id, type)

class Function(Symbol):
    """
    Function class represents a function in the symbol table
    """
    def __init__(self, id, type="fun"):
        super().__init__(id, type)
        self.params = []

class Class(Symbol):
    """
    Class class represents a class in the symbol table
    """
    def __init__(self, id, type="class"):
        super().__init__(id, type)
        self.methods = []

class Scope():
    """
    Scope class represents a scope in the symbol table
    """
    def __init__(self, id, index):
        self.id = id
        self.index = index