from objetc_types import ObjectType, VariableType, FunctionType, ClassType


class Scope:
    def __init__(self, id, depth, parent_scope=None):
        self.id = id
        self.depth = depth
        self.variables: list[VariableType] = []
        self.functions: list[FunctionType] = []
        self.classes: list[ClassType] = []
        self.parent_scope = parent_scope

    def lookup_symbol(self, name, type: ObjectType):
        if type == VariableType:
            for var in self.variables:
                if var.id == name:
                    return var
                
        elif type == FunctionType:
            for func in self.functions:
                if func.id == name:
                    return func
                
        elif type == ClassType:
            for cls in self.classes:
                if cls.id == name:
                    return cls
        else:
            return None
        

    def add_symbol(self, symbol: ObjectType):
        if isinstance(symbol, VariableType):
            self.variables.append(symbol)

        elif isinstance(symbol, FunctionType):
            self.functions.append(symbol)

        elif isinstance(symbol, ClassType):
            self.classes.append(symbol)


    def lookup_parent(self, name, type: ObjectType):
        if self.parent_scope is None:
            return None
        else:
            return self.parent_scope.lookup_symbol(name, type)
        
    
    def update_symbol(self, symbol: ObjectType):
        if isinstance(symbol, VariableType):
            for i, var in enumerate(self.variables):
                if var.id == symbol.id:
                    self.variables[i] = symbol
                    break

        elif isinstance(symbol, FunctionType):
            for i, func in enumerate(self.functions):
                if func.id == symbol.id:
                    self.functions[i] = symbol
                    break

        elif isinstance(symbol, ClassType):
            for i, cls in enumerate(self.classes):
                if cls.id == symbol.id:
                    self.classes[i] = symbol
                    break


    def __str__(self):
        return f"Scope {self.id} at depth {self.depth}"
    

class ScopeManager():
    def __init__(self):
        self.current_scope = Scope("global", 0)
        self.scope_stack: list[Scope] = []
        self.main_stack: list[Scope] = []
        self.depth = 0

    def enter_scope(self, id):
        self.depth += 1
        new_scope = Scope(id, self.depth, self.current_scope)
        self.scope_stack.append(new_scope)
        self.main_stack.append(new_scope)
        self.current_scope = new_scope

    def exit_scope(self):
        self.depth -= 1
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]

    def lookup_symbol(self, name, type: ObjectType):
        return self.current_scope.lookup_symbol(name, type)
    
    def lookup_parent(self, name, type: ObjectType):
        return self.current_scope.lookup_parent(name, type)
    
    def add_symbol(self, symbol: ObjectType):
        self.current_scope.add_symbol(symbol)

    def update_symbol(self, symbol: ObjectType):
        self.current_scope.update_symbol(symbol)

    def __str__(self):
        return f"Current scope: {self.current_scope}"