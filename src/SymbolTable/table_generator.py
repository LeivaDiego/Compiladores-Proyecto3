from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SymbolTable.symbol import Symbol, Variable, Function, Class, Scope
from SymbolTable.types import DataType, AnyType, BooleanType, NumberType, StringType, NilType
from Utils.regex_controller import trim_expression
from tabulate import tabulate
from typing import List, Type

class TableGenerator(compiscriptVisitor):
    def __init__(self, logging=False):
        # Logging flag
        self.logging = logging

        # Scoping variables
        self.symbol_table: List[Symbol] = []
        self.current_scope: Scope = None
        self.scope_stack: List[Scope] = []

        # Symbol helper
        self.current_class: Class = None
        self.current_function: Function = None
        self.current_variable: Variable = None
        self.current_attribute: Variable = None

        # Helper flags
        self.in_init = False
        self.in_class = False
        self.in_function = False
        self.in_variable = False
        self.visited = False


    def printf(self, *args):
        """
        A helper function to print messages if logging is enabled.
        """
        if self.logging:
            print(*args)


    def enter_scope(self, name):
        # Get the index of the current scope
        scope_index = len(self.scope_stack)
        # Create a new scope
        self.current_scope = Scope(name, scope_index)
        # Append the new scope to the scope stack
        self.scope_stack.append(self.current_scope)
        self.printf(f"INFO -> Entering scope: {self.current_scope.id}")


    def exit_scope(self):
        # Pop the current scope from the scope stack
        exited_scope = self.scope_stack.pop()
        # Get the new current scope
        self.current_scope = self.scope_stack[-1]
        self.printf(f"INFO -> Exiting scope: {exited_scope.id}")


    def add_symbol(self, symbol: Symbol):
        # Determine if the symbol is a variable in a class initialization
        if isinstance(symbol,(Variable)) and self.in_init:
            # Variables in init have their scope set to the class scope
            symbol.scope = self.scope_stack[-2]
        elif isinstance(symbol, (Function, Class)):
            # Other symbols use the current scope
            symbol.scope = self.scope_stack[-2]
        else:
            symbol.scope = self.current_scope

        # Handle specific logic for variables
        if isinstance(symbol, Variable):
            # Set the offset and update it in the scope
            symbol.offset = self.current_scope.offset
            self.current_scope.offset += symbol.size

        # Add the symbol to the symbol table
        self.symbol_table.append(symbol)

       
        self.printf(f"INFO -> Adding {symbol.type}: {symbol.id} to scope: {symbol.scope.id}")


    def search_symbol(self, id, type: Type[Symbol]):
        # Search for the symbol in the symbol table
        for symbol in reversed(self.symbol_table):
            if symbol.id == id and isinstance(symbol, type):
                return symbol
        return None


    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.printf("INFO -> Visiting Program")
        # Enter the global scope
        self.enter_scope("global")
        # Visit the rest of the tree
        self.visitChildren(ctx)


    def visitClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        self.printf("INFO -> Visiting Class Declaration")
        # Set the class flag
        self.in_class = True

        # Get the class id
        class_id = ctx.IDENTIFIER(0).getText()
        parent_class = None

        # Check if the class inherits from another class
        if ctx.IDENTIFIER(1):
            # Get the parent class
            parent_id = ctx.IDENTIFIER(1).getText()
            parent_class = self.search_symbol(parent_id, Class)

        self.printf(f"INFO -> Creating class: {class_id}")
        # Create a new class symbol
        if parent_class is not None:
            self.printf(f"INFO -> Inheriting from: {parent_class.id}")
            self.current_class = Class(class_id, parent=parent_class)
            # Get the attributes and methods of the parent class
            self.current_class.get_parent_attributes()
        else:
            self.current_class = Class(class_id)

        # Enter the class scope
        self.enter_scope(class_id)

        # Visit the rest of the tree
        self.visitChildren(ctx)

        # Set the size of the class
        self.current_class.set_size()

        # Add the class to the symbol table
        self.add_symbol(self.current_class)

        # Exit the class scope
        self.exit_scope()

        # Reset the class flag
        self.in_class = False
        self.current_class = None


    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        self.printf("INFO -> Visiting Function Declaration")
        # Set the function flag
        self.in_function = True
        
        # Get the function id
        function_id = ctx.IDENTIFIER().getText()
        self.printf(f"INFO -> Creating function: {function_id}")
        
        # Check if the function is a constructor
        if function_id == "init" and self.in_class:
            self.printf(f"INFO -> This function is a Constructor for class: {self.current_scope.id}")
            self.in_init = True

        # Create a new function symbol
        self.current_function = Function(function_id)

        # Enter the function scope
        self.enter_scope(function_id)

        # Visit the rest of the tree
        self.visitChildren(ctx)

        # Add the function to the symbol table
        self.add_symbol(self.current_function)

        # Exit the function scope
        self.exit_scope()
        # Reset the function flag
        self.in_function = False
        self.in_init = False


    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        self.printf("INFO -> Visiting Parameters")
        
        # Get the parameters
        for param in ctx.IDENTIFIER():
            # Get the parameter id
            param_id = param.getText()
            # Create a new variable symbol
            parameter = Variable(param_id)
            # Set the data type of the parameter to AnyType
            parameter.type = "param"
            parameter.set_values(AnyType())
            # Add the parameter to the symbol table
            self.add_symbol(parameter)

    
    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        self.printf("INFO -> Visiting Variable Declaration")

        # Get the variable id
        variable_id = ctx.IDENTIFIER().getText()
        self.printf(f"INFO -> Creating variable: {variable_id}")

        # Create a new variable symbol
        self.current_variable = Variable(variable_id)

        # Visit the rest of the tree
        self.visitChildren(ctx)

        # Add the variable to the symbol table
        self.add_symbol(self.current_variable)