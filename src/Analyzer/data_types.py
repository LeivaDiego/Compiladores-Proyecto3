class DataType():
    """
    Base class for all data types.

    Attributes:
        - data_type: The name of the data type.
    """
    def __init__(self, name):
        self.data_type = name

    def __str__(self):
        return self.data_type
    
class NumberType(DataType):
    def __init__(self):
        super().__init__("num")

class StringType(DataType):
    def __init__(self):
        super().__init__("str")

class BooleanType(DataType):
    def __init__(self):
        super().__init__("bool")

class NilType(DataType):
    def __init__(self):
        super().__init__("nil")

class UndefinedType(DataType):
    def __init__(self):
        super().__init__("undefined")