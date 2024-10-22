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

    def __str__(self):
        return f"{self.object_type} - {self.id}"
    

class VariableType(ObjectType):
    def __init__(self, name, context):
        super().__init__(name, context)
        self.data_type = None
        self.initialized = False
        self.value = None
        self.size = None

    def set_initialized(self):
        if self.context.getChildCount() > 3:
            self.initialized = True

        

class FunctionType(ObjectType):
    def __init__(self, name, context):
        super().__init__(name, context)
        self.return_type = None
        self.parameters: list[VariableType] = []
        self.is_anon = False


class ClassType(ObjectType):
    def __init__(self, name, context):
        super().__init__(name, context)
        self.parent = None
        self.attributes = list[VariableType] = []
        self.methods = list[FunctionType] = []