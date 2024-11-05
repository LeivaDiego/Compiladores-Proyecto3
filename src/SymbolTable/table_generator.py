from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SymbolTable.symbol import Symbol, Variable, Function, Class, Scope
from SymbolTable.types import DataType, AnyType, BooleanType, NumberType, StringType, NilType
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

        # Helper flags
        self.in_init = False


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

       
        self.printf(f"ADDED SYMBOL -> {symbol.type}: {symbol.id} | type: {symbol.data_type.name} | size:{symbol.size} | scope: {symbol.scope.id} | offset: {symbol.offset}")


    def search_symbol(self, id, type: Type[Symbol]):
        # Search for the symbol in the symbol table
        for symbol in reversed(self.symbol_table):
            if symbol.id == id and isinstance(symbol, type):
                return symbol
        return None


    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.printf("VISIT -> Program node")
        # Enter the global scope
        self.enter_scope("global")
        # Visit the rest of the tree
        self.visitChildren(ctx)


    def visitClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        self.printf("VISIT -> Class Declaration node")
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
        self.current_class = None


    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        self.printf("VISIT -> Function Declaration node")
        
        # Get the function id
        function_id = ctx.IDENTIFIER().getText()
        self.printf(f"INFO -> Creating function: {function_id}")
        
        # Check if the function is a constructor
        if function_id == "init" and self.current_class is not None:
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
        self.in_init = False


    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        self.printf("VISIT -> Parameters node")
        
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
        self.printf("VISIT -> Variable Declaration node")

        # Get the variable id
        variable_id = ctx.IDENTIFIER().getText()
        self.printf(f"INFO -> Creating variable: {variable_id}")

        # Create a new variable symbol
        self.current_variable = Variable(variable_id)

        # Visit the rest of the tree
        self.visitChildren(ctx)

        # Add the variable to the symbol table
        self.add_symbol(self.current_variable)

    def visitExpression(self, ctx:compiscriptParser.ExpressionContext):
        self.printf(f"VISIT -> Expression node")
        self.printf(f"INFO -> Expression: {ctx.getText()}")
        # Visit the rest of the tree
        self.visitChildren(ctx)

    def visitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        self.printf("VISIT ->  Assignment node")
        
        # Check if the assignment is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid assignment")
            # Check if the assingment is a attribute initialization
            if self.in_init and self.current_class is not None:
                # Get the attribute id
                attribute_id = ctx.IDENTIFIER().getText()
                self.printf(f"INFO -> This is an attribute initialization for {attribute_id}")
                self.current_variable = Variable(attribute_id)    

        else:
            self.printf("INFO -> This is a wrapper node")

        # Visit the rest of the tree
        self.visitChildren(ctx)


    def visitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        self.printf("VISIT -> Logic Or node")
        
        # Check if the logic or is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid logic or")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Set the data type of the variable
                self.printf("INFO -> Setting data type for logic or")
                self.current_variable.set_values(BooleanType())
        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)


    def visitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        self.printf("VISIT -> Logic And node")
        
        # Check if the logic and is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid logic and")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Set the data type of the variable
                self.printf("INFO -> Setting data type for logic and")
                self.current_variable.set_values(BooleanType())
        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)


    def visitEquality(self, ctx:compiscriptParser.EqualityContext):
        self.printf("VISIT -> Equality node")
        
        # Check if the equality is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid equality")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Set the data type of the variable
                self.printf("INFO -> Setting data type for equality")
                self.current_variable.set_values(BooleanType())
        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)

    
    def visitComparison(self, ctx:compiscriptParser.ComparisonContext):
        self.printf("VISIT -> Comparison node")
        
        # Check if the comparison is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid comparison")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Set the data type of the variable
                self.printf("INFO -> Setting data type for comparison")
                self.current_variable.set_values(BooleanType())
        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)