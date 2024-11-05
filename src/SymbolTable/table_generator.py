from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SymbolTable.symbol import Symbol, Variable, Function, Class, Scope, ExprTerm
from SymbolTable.types import AnyType, BooleanType, NumberType, StringType, NilType, InstanceType
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
        self.multi_term = False
        self.in_assignment = False

    def display_table(self):
        formatted_symbols = []

        # Table headers
        headers = ["ID", "Type", "Scope", "Scope Index", "Data Type", "Size", "Offset"]

        # format the symbols for display
        self.printf("INFO -> Formatting symbols for display")
        for symbol in self.symbol_table:
            symbol_data = [
                symbol.id,
                symbol.type,
                symbol.scope.id,
                symbol.scope.index,
                symbol.data_type.name if symbol.data_type is not None else "-",
                symbol.size if symbol.size is not None else "-",
                symbol.offset if symbol.offset is not None else "-"
            ]
            # Append the formatted symbol to the list
            formatted_symbols.append(symbol_data)

        # Create a table with the formatted symbols and headers
        # using the tabulate library
        display_table = tabulate(formatted_symbols, headers, tablefmt="fancy_grid")

        with open("src/SymbolTable/symbol_table.txt", "w", encoding="utf8") as f:
            f.write(display_table)

        print("SUCCESS -> Symbol table has been written to src/SymbolTable/symbol_table.txt")


        

        


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

        # Print the added symbol
        if isinstance(symbol, Variable):
            self.printf(f"ADDED SYMBOL -> {symbol.type}: {symbol.id} | type: {symbol.data_type.name} | size:{symbol.size} | scope: {symbol.scope.id} | offset: {symbol.offset}")
            # Reset the current variable
            self.current_variable = None

        elif isinstance(symbol, Function):
            self.printf(f"ADDED SYMBOL -> {symbol.type}: {symbol.id} | scope: {symbol.scope.id}")
            # Reset the current function
            self.current_function = None

        elif isinstance(symbol, Class):
            self.printf(f"ADDED SYMBOL -> {symbol.type}: {symbol.id} | size: {symbol.size} | scope: {symbol.scope.id}")
            # Reset the current class
            self.current_class = None

        
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
                # Visit the rest of the tree
                self.visitChildren(ctx)
                self.in_assignment = True

        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)

        # Check if the assignment is a attribute initialization
        if self.in_assignment:
            self.printf("INFO -> Finished attribute initialization")
            # Add the attribute to the class
            self.current_class.attributes.append(self.current_variable)
            # Add the attribute to the symbol table
            self.add_symbol(self.current_variable)
            # Reset the assignment flag
            self.in_assignment = False
        

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


    def visitTerm(self, ctx:compiscriptParser.TermContext):
        self.printf("VISIT -> Term node")
        # Check if the term is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid term")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Set the data type of the variable
                nodes = ctx.getChildren()
                # Set multiple data types for the variable flag

                if ctx.getChildCount() > 1:
                    self.multi_term = True

                    for node in nodes:
                        if node.getText() == "-":
                            self.printf("INFO -> Found - operator, Setting data type for term")
                            self.current_variable.set_values(NumberType())
                            return
                        
                        elif node.getText() == "+":
                            self.printf("INFO -> Found + operator need to check if it is a string concatenation")

                # Check if the variable is a string
                self.visitChildren(ctx)
                self.current_variable.resolve_expr_type()

                # Reset the multi term flag
                self.multi_term = False

        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)


    def visitFactor(self, ctx:compiscriptParser.FactorContext):
        self.printf("VISIT -> Factor node")
        
        # Check if the factor is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid factor")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Set the data type of the variable
                self.printf("INFO -> Setting data type for factor")
                self.current_variable.set_values(NumberType())
        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)


    def visitUnary(self, ctx:compiscriptParser.UnaryContext):
        self.printf("VISIT -> Unary node")
        
        # Check if the unary is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid unary")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Check if its negation or negative
                self.printf("INFO -> Setting data type for unary")
                # If the unary is a negative operator set the data type to number
                if ctx.getChild(0).getText() == "-":
                    self.current_variable.set_values(NumberType())
                # If the unary is a negation operator set the data type to boolean
                elif ctx.getChild(0).getText() == "!":
                    self.current_variable.set_values(BooleanType())
                
        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)


    def visitCall(self, ctx:compiscriptParser.CallContext):
        self.printf("VISIT -> Call node")
        
        # Check if the call is not a wrapper node
        if ctx.getChildCount() > 1:
            self.printf("INFO -> This is a valid call")
            # Check if we are in a valid assignment context
            if self.current_variable is not None:
                # Set the data type of the variable to AnyType 
                # since we don't know the return type
                self.printf("INFO -> Setting data type for call")
                self.current_variable.set_values(AnyType())
        else:
            self.printf("INFO -> This is a wrapper node")
            # Visit the rest of the tree
            self.visitChildren(ctx)


    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        self.printf("VISIT -> Primary node")
        # Get the primary text
        primary_text = ctx.getText()
        if primary_text != "this":
            # Check if the primary is in a valid assignment context
            if self.current_variable is not None:
                # Check if the primary is multiple terms
                if self.multi_term:
                    self.printf("INFO -> This is a multiple term primary")
                    # Check if the primary is a string
                    if ctx.STRING():
                        self.printf("INFO -> This is a string")
                        string_term = ExprTerm(StringType())
                        self.current_variable.expr_terms.append(string_term)

                    # Check if the primary is a number
                    elif ctx.NUMBER():
                        self.printf("INFO -> This is a number")
                        number_term = ExprTerm(NumberType())
                        self.current_variable.expr_terms.append(number_term)

                    # Check if the primary is a boolean
                    elif primary_text in ["true", "false"]:
                        self.printf("INFO -> This is a boolean")
                        boolean_term = ExprTerm(BooleanType())
                        self.current_variable.expr_terms.append(boolean_term)

                    # Check if the primary is a nil
                    elif primary_text == "nil":
                        self.printf("INFO -> This is a nil")
                        nil_term = ExprTerm(NilType())
                        self.current_variable.expr_terms.append(nil_term)

                    # Check if the primary is an identifier
                    elif ctx.IDENTIFIER():
                        self.printf("INFO -> This is an identifier")
                        symbol = self.search_symbol(primary_text, Symbol)
                        if symbol:
                            identifier_term = ExprTerm(symbol.data_type)
                            self.current_variable.expr_terms.append(identifier_term)
                        else:
                            raise Exception(f"Identifier {primary_text} not found")

                else:
                    # If the primary is not multiple terms set the data type of the variable
                    self.printf("INFO -> This is a single term primary")
                    # Check if the primary is a string
                    if ctx.STRING():
                        self.current_variable.set_values(StringType())

                    # Check if the primary is a number
                    elif ctx.NUMBER():
                        self.current_variable.set_values(NumberType())

                    # Check if the primary is a boolean
                    elif primary_text in ["true", "false"]:
                        self.current_variable.set_values(BooleanType())

                    # Check if the primary is a nil
                    elif primary_text == "nil":
                        self.current_variable.set_values(NilType())

                    # Check if the primary is an identifier
                    elif ctx.IDENTIFIER():
                        symbol = self.search_symbol(primary_text, Symbol)
                        if symbol:
                            self.current_variable.set_values(symbol.data_type)
                        else:
                            raise Exception(f"Identifier {primary_text} not found")

                    # Check if primary is a instantiation
                    elif ctx.instantiation():
                        # Visit the rest of the tree
                        self.visitChildren(ctx)

                    # Check for expressions
                    elif ctx.expression():
                        # Visit the rest of the tree
                        self.visitChildren(ctx)
                    
                    else:
                        raise Exception(f"No type found for primary {primary_text}")
                    
        else:
            self.printf("INFO -> Skipping primary node since it is a 'this' keyword")
                

    def visitInstantiation(self, ctx:compiscriptParser.InstantiationContext):
        self.printf("VISIT -> Instantiation node")

        # Get the instantiation id
        instantiation_id = ctx.IDENTIFIER().getText()

        self.printf(f"INFO -> Creating instantiation: {instantiation_id}")

        # Check if the instantiation is in a valid assignment context
        if self.current_variable is not None:
            # Check if the instantiation is a class
            class_symbol = self.search_symbol(instantiation_id, Class)
            if class_symbol:
                self.current_variable.data_type = InstanceType()
                self.current_variable.size = class_symbol.size
            else:
                raise Exception(f"Class {instantiation_id} not found")