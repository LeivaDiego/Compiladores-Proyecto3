from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SymbolTable.symbol import Symbol, Variable, Function, Class, Scope
from typing import List

class TableGenerator(compiscriptVisitor):
    """
    TableGenerator class is a visitor class that generates the symbol table.
    Each symbol is added to the symbol table with its scope and offset.

    Args:
        log (bool): A flag to enable logging

    Attributes:
        logging (bool): A flag to enable logging
        symbol_table (List[Symbol]): A list of symbols in the symbol table
        current_scope (Scope): The current scope
        scope_stack (List[Scope]): A stack to keep track of active scopes 
        scope_counter (int): A counter to keep track of scopes indexes
        offset (int): An offset to keep track of symbols in the symbol table
    """
    def __init__(self, log=False):
        self.logging = log
        self.symbol_table: List[Symbol] = []
        self.current_scope: Scope = None
        self.scope_stack: List[Scope] = []
        self.scope_counter = 0
        self.offset = 0

    def printf(self, *args):
        """
        A helper function to print messages if logging is enabled.
        """
        if self.logging:
            print(*args)

    def add_symbol(self, symbol: Symbol):
        """
        A helper function to add a symbol to the symbol table.
        Updates the symbol's scope and offset. 
        Increments the offset by 1.

        Args:
            symbol (Symbol): A symbol to add to the symbol table

        Returns:
            None
        """
        symbol.scope = self.current_scope
        symbol.offset = self.offset
        self.symbol_table.append(symbol)
        self.offset += 1
        self.printf(f"INFO -> Added symbol: ID = {symbol.id}, Type = {symbol.type}, Scope = {symbol.scope.id}, Offset = {symbol.offset}")

    def enter_scope(self, name=None):
        """
        A helper function to enter a new scope.
        Updates the current scope and increments the scope counter.
        appends the current scope to the scope stack.

        Args:
            name (str): The name of the scope (default=None)

        Returns:
            None
        """
        self.scope_counter += 1
        self.current_scope = Scope(name, self.scope_counter)
        self.scope_stack.append(self.current_scope)
        self.printf(f"INFO -> Entering scope: {self.current_scope.id}")

    def exit_scope(self):
        """
        A helper function to exit the current scope.
        Updates the current scope to the previous scope in the scope stack.
        Pops the current scope from the scope stack.

        Returns:
            None
        """
        if self.scope_stack:
            exited_scope = self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1] if self.scope_stack else 0
            self.printf(f"INFO -> Exiting: {exited_scope.id}, returning to scope: {self.current_scope.id}")


    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.printf("INFO -> Visiting program")
        self.enter_scope("global")  # Enter the global scope
        self.visitChildren(ctx)

    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        self.printf("INFO -> Visiting variable declaration")
        id = ctx.IDENTIFIER().getText() # Get the variable identifier
        var = Variable(id)              # Create a variable symbol
        self.add_symbol(var)            # Add the variable to the symbol table
        self.visitChildren(ctx)         # Visit the children of the variable declaration