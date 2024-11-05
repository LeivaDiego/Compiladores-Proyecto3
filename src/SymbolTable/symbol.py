from typing import List
from SymbolTable.types import DataType

class Symbol():
    """
    Symbol class represents a symbol in the symbol table.
    """
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.scope = None
        self.offset = None
        self.size = None
        self.data_type = None


class Variable(Symbol):
    """
    Variable class represents a variable in the symbol table
    """
    def __init__(self, id, type="var"):
        super().__init__(id, type)
        self.data_type = None

    def set_values(self, data_type: DataType):
        """
        Set the size of the variable
        """
        self.data_type = data_type
        self.size = data_type.size


class Function(Symbol):
    """
    Function class represents a function in the symbol table
    """
    def __init__(self, id, type="fun"):
        super().__init__(id, type)
        self.params: List[Variable] = []


class Class(Symbol):
    """
    Class class represents a class in the symbol table
    """
    def __init__(self, id, type="class", parent=None):
        super().__init__(id, type)
        self.methods: List[Function] = []
        self.attributes: List[Variable] = []
        self.parent = parent

    def get_parent_attributes(self):
        """
        Get the attributes of the parent class
        """
        if self.parent:
            self.attributes += self.parent.attributes
    
    def get_parent_methods(self):
        """
        Get the methods of the parent class
        """
        if self.parent:
            self.methods += self.parent.methods

    def set_size(self):
        """
        Set the size of the class
        """
        size = 0
        for attr in self.attributes:
            size += attr.data_type.size
        self.size = size

class Scope():
    """
    Scope class represents a scope in the symbol table
    """
    def __init__(self, id, index):
        self.id = id
        self.index = index
        self.offset = 0