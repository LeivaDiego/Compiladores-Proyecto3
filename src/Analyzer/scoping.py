from Analyzer.objetc_types import ObjectType, VariableType, FunctionType, ClassType
from tabulate import tabulate

class Scope:
    def __init__(self, id, index, parent_scope=None):
        self.id = id
        self.index = index
        self.symbol_table = []
        self.parent_scope = parent_scope

    def lookup_symbol(self, name, type: ObjectType):
        for symbol in self.symbol_table:
            if symbol.id == name and type == symbol.object_type:
                return symbol
        return None
        

    def insert_symbol(self, symbol: ObjectType):
        if self.lookup_symbol(symbol.id, symbol.object_type):
            raise Exception(f"Symbol {symbol.id} already declared in scope {self.id}")
        
        # Add the scope index and id to the symbol
        symbol.scope_index = self.index
        symbol.scope_id = self.id

        # Append the symbol to the symbol table
        self.symbol_table.append(symbol)


    def lookup_parent(self, name, type: ObjectType):
        if self.parent_scope is None:
            return None
        else:
            return self.parent_scope.lookup_symbol(name, type)
        
    
    def update_symbol(self, symbol: ObjectType):
        for i, sym in enumerate(self.symbol_table):
            if sym.id == symbol.id and sym.object_type == symbol.object_type:
                self.symbol_table[i] = symbol
                break
    

class ScopeManager():
    def __init__(self):
        # Initialize the scope manager with a global scope
        # at index 0
        self.index = 0
        self.offset = 0
        self.global_scope = Scope("global", self.index)
        self.current_scope = self.global_scope
        # Initialize the scope stack with the global scope
        self.scope_stack: list[Scope] = [self.current_scope]
        # Initialize the main stack empty
        self.scope_register: list[Scope] = []

    def enter_scope(self, id="scope"):
        # Increment the index and depth
        self.index += 1
        # Create a new scope with the current scope as its parent
        new_scope = Scope(id, self.index, self.current_scope)
        # Append the new scope to the scope stack and set it as the current scope
        self.scope_stack.append(new_scope)
        # Set the new scope as the current scope
        self.current_scope = new_scope


    def exit_scope(self):
        # Pop the current scope from the scope stack
        finished_scope = self.scope_stack.pop()
        # Append the finished scope to the main stack
        self.scope_register.append(finished_scope)
        # Set the previous scope as the current scope
        self.current_scope = self.scope_stack[-1]


    def add_symbol(self, symbol: ObjectType):
        if isinstance(symbol, VariableType):
            symbol.offset = self.offset
            if symbol.initialized:
                self.offset += symbol.size

        self.current_scope.insert_symbol(symbol)

    def finalize_scopes(self):
        # Copy the scope stack to the stack register
        while self.scope_stack:
            finished_scope = self.scope_stack.pop()
            self.scope_register.append(finished_scope)

        # Sort the main stack by index
        self.scope_register.sort(key=lambda x: x.index)


    def visualize_symbol_tables(self):
        variables_table = []
        functions_table = []
        classes_table = []

        for scope in self.scope_register:
            for symbol in scope.symbol_table:
                # Collect variables in the symbol table
                if isinstance(symbol, VariableType):
                    variables_table.append([
                        symbol.id, symbol.initialized, symbol.data_type, symbol.size, symbol.offset
                    ])

                # Collect functions in the symbol table
                elif isinstance(symbol, FunctionType):
                    param_names = [param.id for param in symbol.parameters]
                    functions_table.append([
                        symbol.id, symbol.return_type, ", ".join(param_names)
                    ])

                # Collect classes in the symbol table
                elif isinstance(symbol, ClassType):
                    method_names = [method.id for method in symbol.methods]
                    attr_names = [attr.id for attr in symbol.attributes]
                    classes_table.append([
                        symbol.id, symbol.parent, ", ".join(attr_names), ", ".join(method_names)
                    ])


        # Format tables using tabulate
        variables_table_str = tabulate(variables_table, headers=["ID", "Initialized", "Data Type", "Size", "Offset"], tablefmt="grid")
        functions_table_str = tabulate(functions_table, headers=["ID", "Return Type", "Parameters"], tablefmt="grid")
        classes_table_str = tabulate(classes_table, headers=["ID", "Inherit", "Attributes", "Methods"], tablefmt="grid")

        # Write to file the tables
        with open("src/SymbolTables/table.txt", "w") as f:
            f.write(variables_table_str)
            f.write("\n\n")
            f.write(functions_table_str)
            f.write("\n\n")
            f.write(classes_table_str)
