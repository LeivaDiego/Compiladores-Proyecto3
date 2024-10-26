from Analyzer.data_types import DataType, NumberType, StringType, BooleanType, NilType

class ObjectType():
    """
    Base class for all object types.

    Attributes:
        - object_type: The name of the object type.
    """
    def __init__(self, name, context):
        self.id = name
        self.context = context
        self.object_type = self.__class__.__name__.replace("Type", "").lower()
        self.scope_index = None
        self.scope_id = None

    def __str__(self):
        return f"{self.object_type} - {self.id}"
    

class VariableType(ObjectType):
    def __init__(self, name, context):
        super().__init__(name, context)
        self.data_type = None
        self.initialized = False
        self.offset = None
        self.size = 0

    def set_size(self):
        self.size = self.data_type.size
        

class FunctionType(ObjectType):
    def __init__(self, name, context):
        super().__init__(name, context)
        self.return_type = None
        self.parameters: list[VariableType] = []

    def add_parameter(self, parameter: VariableType): 
        self.parameters.append(parameter)


class ClassType(ObjectType):
    def __init__(self, name, context):
        super().__init__(name, context)
        self.parent = None
        self.attributes = list[VariableType] = []
        self.methods = list[FunctionType] = []
        self.size = 0

    def add_attribute(self, attribute: VariableType):
        self.attributes.append(attribute)
        self.size += attribute.data_type.size

    def add_method(self, method: FunctionType):
        self.methods.append(method)