class DataType():
    def __init__(self, name, size, value=None):
        self.name = name
        self.size = size
        self.value = value

    def __str__(self):
        return self.name

class InstanceType(DataType):
    def __init__(self, name="instance", size=0, class_ref=None):
        super().__init__(name, size)
        self.class_ref = class_ref
        
class AnyType(DataType):
    def __init__(self, name="any", size=8):
        super().__init__(name, size)

class NumberType(DataType):
    def __init__(self, name="num", size=4, value=None):
        super().__init__(name, size, value)

class StringType(DataType):
    def __init__(self, name="str", size=4, value=None):
        super().__init__(name, size, value)

class BooleanType(DataType):
    def __init__(self, name="bool", size=1, value=None):
        super().__init__(name, size, value)

class NilType(DataType):
    def __init__(self, name="nil", size=1):
        super().__init__(name, size)