class DataType():
    """
    Base class for all data types.

    Attributes:
        - data_type: The name of the data type.
    """
    def __init__(self, name):
        self.data_type = name
        self.size = 8

    def __str__(self):
        return self.data_type
    
class NumberType(DataType):
    def __init__(self):
        super().__init__("num")
        self.size = 4

class StringType(DataType):
    def __init__(self, value):
        super().__init__("str")
        self.size = len(value)

class BooleanType(DataType):
    def __init__(self):
        super().__init__("bool")
        self.size = 1

class NilType(DataType):
    def __init__(self):
        super().__init__("nil")
        self.size = 0