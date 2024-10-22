from Analyzer.objetc_types import ObjectType, VariableType, FunctionType, ClassType
from tabulate import tabulate

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
        self.current_scope = None
        self.scope_stack: list[Scope] = []
        self.main_stack: list[Scope] = []
        self.depth = 0

    def enter_scope(self, id="global"):
        # If there is no current scope, create a global scope
        if self.current_scope is None:
            new_scope = Scope(id, self.depth)
        # Otherwise, create a new scope with the current scope as its parent
        else:
            self.depth += 1
            new_scope = Scope(id, self.depth, self.current_scope)
        
        # Append the new scope to the scope stack and set it as the current scope
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


    def visualize_symbol_tables(self):
        variables_table = []
        functions_table = []
        classes_table = []

        # Iterate over all scopes in the main scope stack
        for scope in self.main_stack:
            # Collect variables
            for variable in scope.variables:
                variables_table.append([
                    variable.id, variable.data_type, variable.initialized, variable.value, variable.size
                ])

            # Collect functions
            for function in scope.functions:
                param_names = [param.id for param in function.parameters]
                functions_table.append([
                    function.id, function.return_type, ", ".join(param_names), function.is_anon
                ])

            # Collect classes
            for cls in scope.classes:
                method_names = [method.id for method in cls.methods]
                attr_names = [attr.id for attr in cls.attributes]
                classes_table.append([
                    cls.id, cls.parent, ", ".join(attr_names), ", ".join(method_names)
                ])

        # Format tables using tabulate
        variables_table_str = tabulate(variables_table, headers=["ID", "Data Type", "Initialized", "Value", "Size"], tablefmt="grid")
        functions_table_str = tabulate(functions_table, headers=["ID", "Return Type", "Parameters", "Anonymous"], tablefmt="grid")
        classes_table_str = tabulate(classes_table, headers=["ID", "Parent", "Attributes", "Methods"], tablefmt="grid")

        # Write to file the tables
        with open("src/SymbolTables/variable_table.txt", "w") as f:
            f.write(variables_table_str)
        
        with open("src/SymbolTables/functions_table.txt", "w") as f:
            f.write(functions_table_str)

        with open("src/SymbolTables/classes_table.txt", "w") as f:
            f.write(classes_table_str)