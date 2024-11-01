from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SymbolTable.symbol import Symbol, Variable, Function, Class, Scope
from tabulate import tabulate
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
        """
        if self.scope_stack:
            exited_scope = self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1] if self.scope_stack else 0
            self.printf(f"INFO -> Exiting: {exited_scope.id}, returning to scope: {self.current_scope.id}")

    def display_table(self):
        """
        A helper function to display the symbol table in a tabulated format.
        Writes the symbol table to a file symbol_table.txt.
        """
        tabulated_table = []

        for symbol in self.symbol_table:
            tabulated_table.append([
                symbol.id, symbol.type, symbol.scope.id, symbol.offset
                ])
            
        table_str = tabulate(tabulated_table, 
                             headers=["ID", "Type", "Scope", "Offset"],
                             tablefmt="fancy_grid")
        
        with open("src/SymbolTable/symbol_table.txt", "w", encoding="utf-8") as f:
            f.write(table_str)

        self.printf("INFO -> Symbol Table generated successfully")
            

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


    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        self.printf("INFO -> Visiting function")
        id = ctx.IDENTIFIER().getText() # Get the function identifier
        func = Function(id)             # Create a function symbol
        self.add_symbol(func)           # Add the function to the symbol table
        self.enter_scope(id)            # Enter a new scope with the function name
        self.visitChildren(ctx)         # Visit the children of the function
        self.exit_scope()               # Exit the function scope

    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        self.printf("INFO -> Visiting parameters")
        for param in ctx.IDENTIFIER():
            id = param.getText()                # Get the parameter identifier
            var = Symbol(id, "param")           # Create a param symbol
            self.add_symbol(var)                # Add the parameter to the symbol table


    def visitIfStmt(self, ctx:compiscriptParser.IfStmtContext):
        self.printf("INFO -> Visiting if statement")
        self.enter_scope("if block")                # Enter a new scope for the if block
        self.visitChildren(ctx.statement(0))        # Visit the children of the if statement
        self.exit_scope()                           # Exit the if block scope
        if ctx.statement(1):                        # If there is an else statement
            self.enter_scope("else block")          # Enter a new scope for the else block
            self.visitChildren(ctx.statement(1))    # Visit the children of the else statement
            self.exit_scope()                       # Exit the else block scope


    def visitForStmt(self, ctx:compiscriptParser.ForStmtContext):
        self.printf("INFO -> Visiting for statement")
        self.enter_scope("for block")               # Enter a new scope for the for block
        self.visitChildren(ctx)                     # Visit the children of the for statement
        self.exit_scope()                           # Exit the for block scope


    def visitWhileStmt(self, ctx:compiscriptParser.WhileStmtContext):
        self.printf("INFO -> Visiting while statement")
        self.enter_scope("while block")             # Enter a new scope for the while block
        self.visitChildren(ctx)                     # Visit the children of the while statement
        self.exit_scope()                           # Exit the while block scope
