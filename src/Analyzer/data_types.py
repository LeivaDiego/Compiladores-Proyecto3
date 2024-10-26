class DataType():
    # Tipo any y vale berga
    """
    Base class for all data types.

    Attributes:
        - data_type: The name of the data type.
    """
    def __init__(self, name="any"):
        self.data_type = name
        self.size = 10

    def __str__(self):
        return self.data_type
    
class NumberType(DataType):
    def __init__(self):
        super().__init__("num")
        self.size = 8

class StringType(DataType):
    def __init__(self):
        super().__init__("str")

class BooleanType(DataType):
    def __init__(self):
        super().__init__("bool")
        self.size = 2

class NilType(DataType):
    def __init__(self):
        super().__init__("nil")
        self.size = 2