from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SymbolTable.symbol import Symbol, Variable, Function, Class, Scope
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

        # Symbol variables
        self.current_symbol: Symbol = None

        # Helper flags
        self.in_init = False
        self.in_class = False
        self.in_function = False
        self.in_variable = False


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

        # Print a message indicating the type of symbol added
        symbol_type = type(symbol).__name__.lower()
        self.printf(f"INFO -> Adding {symbol_type}: {symbol.id} to scope: {symbol.scope.id}")


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
        self.in_class = True
        class_id = ctx.IDENTIFIER(0).getText()
        parent_class = None

        # Check if the class inherits from another class
        if ctx.IDENTIFIER(1):
            parent_id = ctx.IDENTIFIER(1).getText()
            parent_class = self.search_symbol(parent_id, Class)

        self.printf(f"INFO -> Creating class: {class_id}")
        # Create a new class symbol
        if parent_class is not None:
            self.printf(f"INFO -> Inheriting from: {parent_class.id}")
            self.current_symbol = Class(class_id, parent=parent_class)
            # Get the attributes and methods of the parent class
            self.current_symbol.get_parent_attributes()
            self.current_symbol.get_parent_methods()
        else:
            self.current_symbol = Class(class_id)


        # Enter the class scope
        self.enter_scope(class_id)

        # Visit the rest of the tree
        self.visitChildren(ctx)

        # Set the size of the class
        self.current_symbol.set_size()

        # Add the class to the symbol table
        self.add_symbol(self.current_symbol)

        # Exit the class scope
        self.exit_scope()

        # Reset the current symbol and class flag
        self.current_symbol = None
        self.in_class = False