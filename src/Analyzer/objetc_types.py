class ObjectType():
    """
    Base class for all object types.

    Attributes:
        - object_type: The name of the object type.
    """
    def __init__(self, name, context):
        self.object_type = name
        self.id = None
        self.context = context

    def __str__(self):
        return self.object_type
    

class VariableType(ObjectType):
    def __init__(self):
        super().__init__("variable")
        self.data_type = None
        self.initialized = False
        self.value = None
        self.size = None


class FunctionType(ObjectType):
    def __init__(self):
        super().__init__("function")
        self.return_type = None
        self.parameters: list[VariableType] = []
        self.is_anon = False


class ClassType(ObjectType):
    def __init__(self):
        super().__init__("class")
        self.parent = None
        self.attributes = list[VariableType] = []
        self.methods = list[FunctionType] = []