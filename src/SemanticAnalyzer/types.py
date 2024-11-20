class DataType():
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        return self.name

class InstanceType(DataType):
    def __init__(self, name="instance", size=0):
        super().__init__(name, size)
        
class AnyType(DataType):
    def __init__(self, name="any", size=8):
        super().__init__(name, size)

class NumberType(DataType):
    def __init__(self, name="num", size=4):
        super().__init__(name, size)

class StringType(DataType):
    def __init__(self, name="str", size=4):
        super().__init__(name, size)

class BooleanType(DataType):
    def __init__(self, name="bool", size=1):
        super().__init__(name, size)

class NilType(DataType):
    def __init__(self, name="nil", size=1):
        super().__init__(name, size)