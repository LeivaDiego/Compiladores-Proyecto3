from SemanticAnalyzer.types import DataType, NilType

class Symbol():
    """
    Symbol class represents a symbol in the symbol table.
    """
    def __init__(self, id, type):
        self.id = id                        # The name of the symbol
        self.type = type                    # The type of the symbol (var, fun, class, param, etc.)
        self.scope: Scope = None            # The scope the symbol is in
        self.offset = None                  # The offset of the symbol in the memory
        self.size = None                    # The size of the symbol in the memory (for variables and classes)
        self.data_type: DataType = None     # The data type of the symbol (for variables)
        self.return_type: DataType = None   # The return type of the symbol (for functions)

    def __str__(self):
        return self.id

class Variable(Symbol):
    """
    Variable class represents a variable in the symbol table
    """
    def __init__(self, id, type="var"):
        super().__init__(id, type)

    def set_type(self, data_type: DataType):
        """
        Set the data type of the variable
        """
        self.data_type = data_type
        self.size = data_type.size

    def __str__(self):
        return f"{self.type}: {self.id} | type: {self.data_type} | size: {self.size} | scope: {self.scope.id} | offset: {self.offset}"


class Function(Symbol):
    """
    Function class represents a function in the symbol table
    """
    def __init__(self, id, type="fun"):
        super().__init__(id, type)
        self.parameters = []
        self.returns: list[DataType] = []      # The return types of the function
        self.return_type = NilType()           # The return type of the function

    def __str__(self):
        return f"{self.type}: {self.id} | return type: {self.return_type} | scope: {self.scope.id}"


class Class(Symbol):
    """
    Class class represents a class in the symbol table
    """
    def __init__(self, id, type="class", parent=None):
        super().__init__(id, type)
        self.attributes: list[Variable] = []        # The attributes of the class
        self.methods: list[Function] = []           # The methods of the class
        self.parent = parent                        # The parent class of the class
        self.completed = False                      # Whether the class has been fully defined or not

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
            # Add the parent methods to the child class
            # but only if the method is not already defined in the child class
            for method in self.parent.methods:
                if method.id not in [m.id for m in self.methods]:
                    self.methods.append(method)

    
    def set_size(self):
        """
        Set the size of the class based on the size of its attributes
        """
        size = 0
        for attr in self.attributes:
            size += attr.data_type.size
        self.size = size

    def search_attribute(self, id):
        """
        Search for an attribute in the class and its parents
        """
        for attr in self.attributes:
            if attr.id == id:
                return attr
        if self.parent:
            return self.parent.search_attribute(id)
        return None

    def __str__(self):
        return f"{self.type}: {self.id} | size: {self.size} | scope: {self.scope.id}"


# --------------------------------------------------------------------- #
# Scoping Model
class Scope():
    """
    Scope class represents a scope in the symbol table
    """
    def __init__(self, id, index):
        self.id = id
        self.index = index
        self.offset = 0