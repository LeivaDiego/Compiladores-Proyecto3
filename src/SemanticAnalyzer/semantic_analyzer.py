from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SemanticAnalyzer.symbols import Symbol, Variable, Function, Class, Scope
from SemanticAnalyzer.types import StringType, BooleanType, NumberType, NilType, AnyType, InstanceType
from tabulate import tabulate

class SemanticAnalyzer(compiscriptVisitor):
    def __init__(self, logging=False):
        self.logging = logging # Flag to enable logging
        print("Starting Semantic Analysis...")
        
        # Scoping and symbol table
        self.current_scope: Scope = None        # The current scope
        self.scope_stack: list[Scope] = []      # The scope stack
        self.symbol_table: list[Symbol] = []    # The symbol table

        # Symbol helpers
        self.current_variable: Variable = None  # The current variable
        self.current_function: Function = None  # The current function
        self.current_class: Class = None        # The current class

        # Scope counters 
        self.for_qty = 0                        # The quantity of for loops
        self.while_qty = 0                      # The quantity of while loops
        self.if_qty = 0                         # The quantity of if statements
        self.else_qty = 0                       # The quantity of else statements

        # Helper flags
        self.in_init = False                     # Flag to check if we are in a class initializer
        self.in_class_assignment = False         # Flag to check if we are in an assignment
        self.method_flag = False                 # Flag to check if we are in a class method
        self.in_print = False                    # Flag to check if we are in a print statement
        self.super_call = False                  # Flag to check if we are in a super call


    def log(self, message):
        if self.logging:
            print(f"    {message}")

    def display_table(self):
        print("Generating symbol table...")
        formatted_symbols = []

        # Table headers
        headers = ["ID", "Type", "Scope", "Scope Index", "Data Type", "Size", "Offset"]

        # format the symbols for display
        self.log("INFO -> Formatting symbols for display")
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

        with open("src/SemanticAnalyzer/symbol_table.txt", "w", encoding="utf8") as f:
            f.write(display_table)

        print("SUCCESS -> Symbol table has been written to src/SymbolTable/symbol_table.txt\n")


    def enter_scope(self, id):
        # Get the index of the current scope and create a new scope
        self.current_scope = Scope(id, len(self.scope_stack))
        # Push the current scope to the scope stack
        self.scope_stack.append(self.current_scope)
        # Log the scope entry
        self.log(f"INFO -> Entering scope: {self.current_scope.id}")


    def exit_scope(self):
        # Pop the current scope from the scope stack
        exited_scope = self.scope_stack.pop()
        # Get the new current scope
        self.current_scope = self.scope_stack[-1]
        # Log the scope exit
        self.log(f"INFO -> Exiting scope: {exited_scope.id}")


    def add_symbol(self, symbol:Symbol):
        # Set the scope of the symbol
        # Check if the symbol is an attribute of a class
        if isinstance(symbol, Variable) and symbol.type == "attr":
            # If it is, set the scope to the current class
            # instead of the current scope
            symbol.scope = self.scope_stack[-2]
            symbol.offset = symbol.scope.offset
            self.scope_stack[-2].offset += symbol.size

        elif isinstance(symbol, Variable):
            # If the symbol is a variable, set the scope to the current scope
            symbol.scope = self.current_scope
            symbol.offset = self.current_scope.offset
            self.current_scope.offset += symbol.size

        else:
            # If the symbol is not a variable, nor an attribute 
            # set the scope to the current scope and leave the offset as is
            symbol.scope = self.current_scope

        # Add the symbol to the symbol table
        self.symbol_table.append(symbol)

        # Log the symbol addition
        self.log(f"ADDED SYMBOL -> {symbol}")


    def search_symbol(self, id, type: Symbol):
        # Search for the symbol in the symbol table
        # starting from the current scope and going up 
        # the scope stack
        valid_scopes = set(self.scope_stack)    # The valid scopes to search

        # Iterate over the symbol table in reverse order
        for symbol in reversed(self.symbol_table):
            # Check if the symbol is in the valid scopes and has the correct type
            if symbol.id == id and symbol.scope in valid_scopes and isinstance(symbol, type):
                return symbol
            
        # If the symbol is not found return None
        return None
    
    def lookup_symbol(self, id, type: Symbol):
        for symbol in reversed(self.symbol_table):
            if symbol.id == id and isinstance(symbol, type) and symbol.scope == self.current_scope:
                return symbol
            
        # If the symbol is not found return None
        return None
    

    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.log("VISIT -> Program node")
        # Enter the global scope
        self.enter_scope("global")
        # visit the children of the program node
        self.visitChildren(ctx)
        print("SUCCESS -> Semantic Analysis completed\n")


    def visitDeclaration(self, ctx:compiscriptParser.DeclarationContext):
        self.log("VISIT -> Declaration node")

        # Search for the declaration type
        # Check if the declaration is a class declaration
        if ctx.classDecl():
            self.visitClassDecl(ctx.classDecl())

        # Check if the declaration is a function declaration
        elif ctx.funDecl():
            self.visitFunDecl(ctx.funDecl())

        # Check if the declaration is a variable declaration
        elif ctx.varDecl():
            self.visitVarDecl(ctx.varDecl())

        # Check if the declaration is a statement
        elif ctx.statement():
            self.visitStatement(ctx.statement())

        else:
            # The declaration is not a valid declaration
            raise Exception(f"Invalid declaration: {ctx.getText()}")
        

    def visitClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        self.log("VISIT -> ClassDecl node")
        # Get the class identifier
        class_id = ctx.IDENTIFIER(0).getText()
        parent_class = None # The parent class if exists
        self.in_class_assignment = True

        self.log(f"INFO -> Class declaration for: {class_id}")

        # Check if the class inherits from another class
        if ctx.IDENTIFIER(1):
            # Get the parent class identifier
            parent_id = ctx.IDENTIFIER(1).getText()
            self.log(f"INFO -> Inherits from class: {parent_id}")
            parent_class = self.search_symbol(parent_id, Class)

            if parent_class is None:
                raise Exception(f"Parent class {parent_id} not found in symbol table")

        # Create a new class symbol
        if parent_class is not None:
            self.log(f"INFO -> Creating class symbol with parent attributes and methods")
            self.current_class = Class(class_id, parent=parent_class)

        else:
            # The class is standalone without a parent
            self.log(f"INFO -> Creating standalone class symbol")
            self.current_class = Class(class_id)

        # Enter the class scope
        self.enter_scope(class_id)

        # Visit the class body
        for function in ctx.function():
            # Visit each function in the class body
            self.log(f"INFO -> Visiting function in class body")
            self.visitFunction(function)

        # Set the size of the class based on the size of its attributes
        self.current_class.set_size()

        # Exit the class scope
        self.exit_scope()
        
        # Before adding the class to the symbol table
        # Check if the class is already declared in the current scope
        symbol = self.lookup_symbol(class_id, Class)
        if symbol is not None:
            raise Exception(f"Class {class_id} already declared in scope {self.current_scope.id}")

        # If the class is not already declared
        # Add the class symbol to the symbol table
        self.add_symbol(self.current_class)

        # Reset the current class
        self.current_class = None
        self.in_class_assignment = False


    def visitFunDecl(self, ctx:compiscriptParser.FunDeclContext):
        self.log("VISIT -> FunDecl node")
        # Visit the function node
        self.visitFunction(ctx.function())


    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        self.log("VISIT -> Function node")
        # Get the function identifier
        fun_id = ctx.IDENTIFIER().getText()
        self.log(f"INFO -> Creating function: {fun_id}")

        # Check if the function is a constructor
        if fun_id == "init" and self.current_class is not None:
            self.log(f"INFO -> This function is a constructor for class: {self.current_class.id}")
            self.in_init = True
            self.method_flag = True
        
        elif self.current_class is not None and self.in_class_assignment:
            # We are inside a class and the function is not a constructor
            # This means the function is a method of the class
            self.log(f"INFO -> This function is a method for class: {self.current_class.id}")
            self.method_flag = True

        # Create a new function symbol
        self.current_function = Function(fun_id)

        # Enter the function scope
        self.enter_scope(fun_id)

        # Check if the function has parameters
        if ctx.parameters():
            # Visit the parameters node
            self.visitParameters(ctx.parameters())

        # Visit the block node
        self.visitBlock(ctx.block())

        # Exit the function scope
        self.exit_scope()
        # Before adding the function to the symbol table
        # Check if the function is already declared in the current scope
        symbol = self.lookup_symbol(fun_id, Function)
        if symbol is not None:
            raise Exception(f"Function {fun_id} already declared in scope {self.current_scope.id}")
        
        # If the function is a method of a class
        if self.method_flag:
            # Add the method to the current class
            self.current_class.methods.append(self.current_function)
            self.method_flag = False

        # Add the function symbol to the symbol table
        self.add_symbol(self.current_function)

        # Reset the current function
        self.current_function = None
        self.in_init = False


    def visitBlock(self, ctx:compiscriptParser.BlockContext):
        self.log("VISIT -> Block node")
        # We don't need to enter a new scope for the block
        # because the block is not a scope by itself
        # we just need to visit the children of the block node
        self.visitChildren(ctx)

    
    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        self.log("VISIT -> VarDecl node")
        # Get the variable identifier
        var_id = ctx.IDENTIFIER().getText()
        self.log(f"INFO -> Variable declaration for: {var_id}")

        # Create a new variable symbol
        self.current_variable = Variable(var_id)

        # Check if the variable has an assignment
        if ctx.expression():
            # Visit the expression node
            type = self.visitExpression(ctx.expression())
            # Set the type of the variable
            self.current_variable.set_type(type)
            self.log(f"INFO -> Variable type set to: {type}")

        else:
            # If the variable doesn't have an assignment we can't infer the type
            # set the type to any
            self.log(f"INFO -> Variable type set to any")
            self.current_variable.set_type(AnyType())

        # Before adding the variable to the symbol table
        # Check if the variable is already declared in the current scope
        symbol = self.lookup_symbol(var_id, Variable)
        if symbol is not None:
            raise Exception(f"Variable {var_id} already declared in scope {self.current_scope.id}")

        # Add the variable symbol to the symbol table
        self.add_symbol(self.current_variable)


    def visitExpression(self, ctx:compiscriptParser.ExpressionContext):
        self.log("VISIT -> Expression node")
        self.log(f"INFO -> Expression: {ctx.getText()}")

        # Check if the expression is an assignment
        if ctx.assignment():
            return self.visitAssignment(ctx.assignment())
        # Check if the expression is a anonymous function
        elif ctx.funAnon():
            return self.visitFunAnon(ctx.funAnon())
        else:
            # The expression is not a valid expression
            raise Exception(f"Invalid expression: {ctx.getText()}")
        

    def visitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        self.log("VISIT -> Assignment node")

        # Check if the assignment isn't a wrapper node
        if ctx.getChildCount() > 1:
            # Get the variable id
            var_id = ctx.IDENTIFIER().getText()
            # Check if we are inside a class
            if self.in_init and self.current_class is not None and ctx.call():
                # We are initializing a class attribute
                self.log(f"INFO -> This is a initialization for class attr {var_id}")
                # Create a new variable symbol for the attribute
                attribute = Variable(var_id, type="attr")
                # Visit the assignment node
                data_type = self.visitAssignment(ctx.assignment())
                # Set the type of the attribute
                attribute.set_type(data_type)
                # Add the attribute to the current class
                self.current_class.attributes.append(attribute)
                # Add the attribute to the symbol table
                self.add_symbol(attribute)
            
            # Check if the assignment is for a class attribute
            elif ctx.call() and self.current_class is not None:
                self.log(f"INFO -> Assignment for a class attr {var_id}")
                # Visit the call node to validate the attribute
                self.visitCall(ctx.call())
                return self.visitAssignment(ctx.assignment())
                
            elif ctx.call():
                # We are calling a function or a class attribute
                self.log(f"INFO -> Call for function or class attribute {var_id}")
                # Get the type of the function or class attribute
                type = self.visitCall(ctx.call())
                # reset the multi expression flag
                self.ssion = False

        else:
            # The assignment is a wrapper node, skip it
            # and visit the logic_or node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitLogic_or(ctx.logic_or())

    
    def visitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        self.log("VISIT -> Logic_or node")

        # Check if the logic_or isn't a wrapper node
        if ctx.getChildCount() > 1:
            self.ssion = True
            logic_ands = []
            for logic_and in ctx.logic_and():
                self.log(f"INFO -> logic_and node: {logic_and.getText()}")
                logic_ands.append(self.visitLogic_and(logic_and))
            
            # Check if all the logic_and nodes are boolean type
            for logic_and in logic_ands:
                if not isinstance(logic_and, BooleanType) and not isinstance(logic_and, AnyType):
                    raise Exception(f"Invalid type for logic_or node got: {logic_and}, expected: bool")

            # The logic_or is a boolean type
            return BooleanType()
        
        else:
            # The logic_or is a wrapper node, skip it
            # and visit the logic_and node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitLogic_and(ctx.logic_and(0))


    def visitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        self.log("VISIT -> Logic_and node")

        # Check if the logic_and isn't a wrapper node
        if ctx.getChildCount() > 1:
            self.ssion = True
            equalities = []
            for equality in ctx.equality():
                self.log(f"INFO -> equality node: {equality.getText()}")
                equalities.append(self.visitEquality(equality))
            # check if all the equality nodes are boolean type
            for equality in equalities:
                if not isinstance(equality, BooleanType) and not isinstance(equality, AnyType):
                    raise Exception(f"Invalid type for logic_and node got: {equality}, expected: bool")

            # The logic_and is a boolean type
            return BooleanType()
        
        else:
            # The logic_and is a wrapper node, skip it
            # and visit the equality node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitEquality(ctx.equality(0))


    def visitEquality(self, ctx:compiscriptParser.EqualityContext):
        self.log("VISIT -> Equality node")

        # Check if the equality isn't a wrapper node
        if ctx.getChildCount() > 1:
            self.ssion = True
            comparisons = []
            for comparison in ctx.comparison():
                self.log(f"INFO -> Comparison node: {comparison.getText()}")
                comparisons.append(self.visitComparison(comparison))
            # Check if all the comparison nodes are of the same type
            # all comparisons must be of the same type
            type_set = {}
            for comparison in comparisons:
                if not isinstance(comparison, AnyType):
                    type_set[type(comparison)] = comparison
                    
            if len(type_set) > 1:
                multi_message = " | ".join([f"{value}" for _ , value in type_set.items()])
                raise Exception(f"Invalid type for equality node, got multiple types: {multi_message}")
            
            # The equality is a boolean type
            return BooleanType()

        else:
            # The equality is a wrapper node, skip it
            # and visit the comparison node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitComparison(ctx.comparison(0))


    def visitComparison(self, ctx:compiscriptParser.ComparisonContext):
        self.log("VISIT -> Comparison node")

        # Check if the comparison isn't a wrapper node
        if ctx.getChildCount() > 1:
            self.ssion = True
            terms = []
            # Get the term nodes
            for term in ctx.term():
                self.log(f"INFO -> Term node: {term.getText()}")
                terms.append(self.visitTerm(term))

            # Check if all the term nodes are of number type
            for term in terms:
                if not isinstance(term, NumberType) and not isinstance(term, AnyType):
                    raise Exception(f"Invalid type for comparison node got: {term}, expected: num")

            # The comparison is a boolean type
            return BooleanType()

        else:
            # The comparison is a wrapper node, skip it
            # and visit the term node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitTerm(ctx.term(0))

    
    def visitTerm(self, ctx:compiscriptParser.TermContext):
        self.log("VISIT -> Term node")

        # Check if the term isn't a wrapper node
        if ctx.getChildCount() > 1:
            self.ssion = True
            # Get the operators
            term_operators = []
            minus = False

            # get the + - operators from the term
            for i in range(1, len(ctx.children), 2):
                term_operators.append(ctx.children[i].getText())

            # Check if there are - operators
            # This means the term is a subtraction and must be of number type
            if "-" in term_operators:
                minus = True

            factors = []
            # Get the factor nodes
            for factor in ctx.factor():
                self.log(f"INFO -> Factor node: {factor.getText()}")
                factors.append(self.visitFactor(factor))

            # Check if all the factor nodes are of number type if there are - operators
            if minus:
                # Check if we are in a print statement
                # The operator - is not valid in a print statement
                if self.in_print:
                    raise Exception(f"Invalid operator - in print statement")

                for factor in factors:
                    if not isinstance(factor, NumberType) and not isinstance(factor, AnyType):
                        raise Exception(f"Invalid type for term node got: {factor}, expected: num")
                    
                # The term is a number type
                return NumberType()
                
            else:
                # If there are no - operators, the term may be of number or string type
                # Check if theres a string in the factors
                if any(isinstance(factor, StringType) for factor in factors):
                    # If there's a string, the term is a string type
                    return StringType()
                else:
                    # If there's no string, the term is a number type
                    return NumberType()
        else:
            # The term is a wrapper node, skip it
            # and visit the factor node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitFactor(ctx.factor(0))


    def visitFactor(self, ctx:compiscriptParser.FactorContext):
        self.log("VISIT -> Factor node")

        # Check if the factor isn't a wrapper node
        if ctx.getChildCount() > 1:
            self.ssion = True
            # Get the unary nodes
            unaries = []
            for unary in ctx.unary():
                self.log(f"INFO -> Unary node: {unary.getText()}")
                unaries.append(self.visitUnary(unary))

            # Check if all the unary nodes are of number type
            for unary in unaries:
                if not isinstance(unary, NumberType) and not isinstance(unary, AnyType):
                    raise Exception(f"Invalid type for factor node got: {unary}, expected: num")
                
            # The factor is a number type
            return NumberType()

        else:
            # The factor is a wrapper node, skip it
            # and visit the unary node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitUnary(ctx.unary(0))


    def visitUnary(self, ctx:compiscriptParser.UnaryContext):
        self.log("VISIT -> Unary node")

        # Check if the unary isn't a wrapper node
        if ctx.getChildCount() > 1:
            # Check if the unary is a negation operator
            if ctx.getChild(0).getText() in ["!", "-"]:
                # Get the negation operator
                negation = ctx.getChild(0).getText()
                # Visit the unary node
                unray_type = self.visitUnary(ctx.unary())
                # Check if the negation operator is valid for the unary type
                if negation == "!":
                    self.log(f"INFO -> Negation operator: {negation}")
                    # Check if the unary type is a boolean
                    if not isinstance(unray_type, BooleanType) and not isinstance(unray_type, AnyType):
                        raise Exception(f"Invalid type for negation operator: {negation}, got: {unray_type}, expected: bool")
                    
                    # The unary is a boolean type
                    return BooleanType()
                
                elif negation == "-":
                    self.log(f"INFO -> Negation operator: {negation}")
                    # Check if the unary type is a number
                    if not isinstance(unray_type, NumberType) and not isinstance(unray_type, AnyType):
                        raise Exception(f"Invalid type for negation operator: {negation}, got: {unray_type}, expected: num")
                    
                    # The unary is a number type
                    return NumberType()

            else:
                # If isnt a negation operator, its not a valid unary operator
                raise Exception(f"Invalid unary operator: {ctx.getChild(0).getText()}")

        else:
            # The unary is a wrapper node, skip it
            # and visit the primary node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitCall(ctx.call())


    
    def visitCall(self, ctx:compiscriptParser.CallContext):
        self.log("VISIT -> Call node")

        # Check if the call isn't a wrapper node
        if ctx.getChildCount() > 1:
            self.ssion = True
            
            call_type = self.visitPrimary(ctx.primary())

            # Check if the call is a plain function call
            if ctx.getChild(1).getText() == "(":
                
                # Check if the function call has arguments
                if ctx.arguments():
                    args = self.visitArguments(ctx.arguments(0))

                    # Get the function identifier
                    if ctx.primary().IDENTIFIER():
                        # Get the function reference
                        function_id = ctx.primary().IDENTIFIER().getText()
                        for symbol in self.symbol_table:
                            # Check if the symbol exists in the symbol table
                            if symbol.id == function_id and isinstance(symbol, Function):
                                # Check if the arguments match the function parameters
                                if len(args) != len(symbol.parameters):
                                    raise Exception(f"Invalid number of arguments for function {function_id}, got: {len(args)}, expected: {len(symbol.parameters)}")
                                break

                return call_type
       
            # Check if the call is a class attribute call
            elif ctx.getChild(1).getText() == ".":
                # Get the attribute identifier
                attribute = ctx.IDENTIFIER(0).getText()
                self.log(f"INFO -> Attribute: {attribute}")

                # Check if the call is inside a class
                if self.in_class_assignment:
                    # Search for the attribute in the current class
                    symbol = self.current_class.search_attribute(attribute)
                    
                    if symbol is None:
                        self.log("INFO -> Attribute not found in current class")
                        self.log("         Searching for method...")
                        # If the attribute is not found in the current class
                        # Try searching for a method
                        symbol = self.current_class.search_method(attribute)
                        
                        if symbol is None:
                            # Before raising an exception, check if its a recursive call
                            # If it is, we assume the return type is any
                            if attribute == self.current_function.id:
                                return AnyType()
                            
                            # At this point the method is not found in the class and is not recursive
                            raise Exception(f"Method {attribute} not found in class {self.current_class.id}")
                        
                        self.log(f"INFO -> Method found: {symbol}")
                        return symbol.return_type
                    
                    else:
                        return symbol.data_type

                # Check if the call is a class method call and outside a class
                elif ctx.getChild(3):
                    # Get the method identifier
                    method_id = ctx.IDENTIFIER(0).getText()
                    self.log(f"INFO -> Method: {method_id}")

                    # Search if the method is part of the instance
                    if ctx.primary().IDENTIFIER():
                        # Get the class instance
                        class_id = ctx.primary().IDENTIFIER().getText()
                        class_instance = self.search_symbol(class_id, Variable)
                        # Search for the class in the symbol table
                        class_symbol = self.search_symbol(class_instance.data_type.class_ref.id, Class)

                        if class_symbol is not None:
                            method = class_symbol.search_method(method_id)
                            if method is not None:
                                return method.return_type
                            else:
                                raise Exception(f"Method '{method_id}' not found in instance '{class_id}' of class {class_symbol.id}")
                        else:
                            raise Exception(f"Instance '{class_id}' not found in symbol table")

                    # Search for the method in the symbol table
                    for symbol in self.symbol_table:
                        # Check if the symbol exists in the symbol table
                        if symbol.id == method and isinstance(symbol, Function):
                            return symbol.return_type
                        
                    # At this point the method is not found in the symbol table
                    raise Exception(f"Method {method} not found in symbol table")
            
                else:
                    # We are outside of a class, search for the attribute in the symbol table
                    for symbol in self.symbol_table:
                        # Check if the symbol exists in the symbol table
                        if symbol.id == attribute and isinstance(symbol, Variable):
                            return symbol.data_type
                        
                    # At this point the attribute is not found in the symbol table
                    raise Exception(f"Attribute {attribute} not found in symbol table")
                
        else:
            # The call is a wrapper node, skip it
            # and visit the primary node
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitPrimary(ctx.primary())


    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        self.log("VISIT -> Primary node")

        # Check if the primary is a terminal node
        if ctx.getChildCount() == 1:
            primary_str = ctx.getText()

            # Check if the primary is a value
            if self.current_variable is not None and not self.ssion:
                # We can assume the primary is the value of the variable
                # Check if the primary is a number
                if ctx.NUMBER():
                    # Get the number
                    number = ctx.NUMBER().getText()
                    self.log(f"VALUE -> Number: {number}")

                # Check if the primary is a string
                elif ctx.STRING():
                    # Get the string
                    string = ctx.STRING().getText()
                    self.log(f"VALUE -> String: {string}")

                # Check if the primary is a boolean
                elif primary_str in ["true", "false"]:
                    # Get the boolean
                    boolean = primary_str
                    self.log(f"VALUE -> Boolean: {boolean}")
                    
                # Check if the primary is a nil
                elif primary_str == "nil":
                    # Get the nil
                    nil = primary_str
                    self.log(f"VALUE -> Nil: {nil}")
                    
            # Check if the primary is a number
            if ctx.NUMBER():
                # Get the number
                number = ctx.NUMBER().getText()
                self.log(f"INFO -> Number: {number}")
                return NumberType()

            # Check if the primary is a string
            elif ctx.STRING():
                # Get the string
                string = ctx.STRING().getText()
                self.log(f"INFO -> String: {string}")
                return StringType()

            # Check if the primary is a boolean
            elif primary_str in ["true", "false"]:
                # Get the boolean
                boolean = primary_str
                self.log(f"INFO -> Boolean: {boolean}")
                return BooleanType()

            # Check if the primary is a nil
            elif primary_str == "nil":
                # Get the nil
                nil = primary_str
                self.log(f"INFO -> Nil: {nil}")
                return NilType()

            # Check if the primary is an identifier
            elif ctx.IDENTIFIER():
                # Get the identifier
                identifier = ctx.IDENTIFIER().getText()
                self.log(f"INFO -> Identifier: {identifier}")

                # First check if the identifier is called inside a function
                # This means the call is recursive
                if self.current_function is not None:
                    if identifier == self.current_function.id:
                        # If it is recursive, we assume the type of return is any
                        # because we can't infer the type of the return
                        return AnyType()
                    
                    else: 
                        # Search for the identifier in the symbol table
                        symbol = self.search_symbol(identifier, Variable)
                        # Check if the symbol is found
                        if symbol is None:
                            # If the symbol is not found, search for the identifier AS a function
                            symbol = self.search_symbol(identifier, Function)
                            # Check if the symbol is found
                            if symbol is None:
                                raise Exception(f"Identifier {identifier} not found in symbol table")

                            # The primary is a function, return the return type of the function
                            return symbol.return_type

                        # The primary is a variable, return the data type of the variable
                        return symbol.data_type
                        
                    
                else:
                    # If it isnt a recursive call
                    # Search for the identifier in the symbol table
                    symbol = self.search_symbol(identifier, Variable)
                    # Check if the symbol is found
                    if symbol is None:
                        # If the symbol is not found, search for the identifier AS a function
                        symbol = self.search_symbol(identifier, Function)
                        # Check if the symbol is found
                        if symbol is None:
                            raise Exception(f"Identifier {identifier} not found in symbol table")

                        # The primary is a function, return the return type of the function
                        return symbol.return_type

                    # The primary is a variable, return the data type of the variable
                    return symbol.data_type

            # Check if the primary is a this keyword
            elif primary_str == "this":
                self.log(f"INFO -> 'this' keyword found")
                # If we are not inside a class, the this keyword is invalid
                if self.current_class is None:
                    raise Exception(f"Invalid this keyword outside a class")

            # Check if the primary is a instantiation
            elif ctx.instantiation():
                return self.visitInstantiation(ctx.instantiation())

        else:
            # The primary has children, is a expression or a super call
            # Check if the primary is a expression
            if ctx.expression():
                return self.visitExpression(ctx.expression())

            # Check if the primary is a super call
            if ctx.getChild(0).getText() == "super":
                identifier = ctx.IDENTIFIER().getText()
                self.log(f"INFO -> Super call: {identifier}")
                self.super_call = True

                # Search for the function in the parent class
                if self.current_class is not None:
                    if self.current_class.parent is not None:
                        symbol = self.current_class.parent.search_method(identifier)
                        if symbol is None:
                            raise Exception(f"Method {identifier} not found in parent class {self.current_class.parent.id}")
                        
                        return symbol.return_type
                    
                    else:
                        raise Exception(f"Parent class not found for class {self.current_class.id}")
                
                else:
                    raise Exception(f"Super call outside of class")


    def visitInstantiation(self, ctx:compiscriptParser.InstantiationContext):
        self.log("VISIT -> Instantiation node")
        # Get the class identifier
        class_id = ctx.IDENTIFIER().getText()
        # Search for the class in the symbol table
        class_symbol = self.search_symbol(class_id, Class)
        # Check if the class is found
        if class_symbol is None:
            raise Exception(f"Class {class_id} not found in symbol table")
        
        self.log(f"INFO -> Instantiation for class: {class_id}")
        
        args = []   # List to store the arguments

        # Check if the instantiation has arguments
        if ctx.arguments():
            # Get the arguments
            args = self.visitArguments(ctx.arguments())

        # Search for the initializer method in the class
        initializer = class_symbol.search_method(f"init")
            
        # Check if the instantiation has proper amount of arguments
        if len(args) != len(initializer.parameters):
            raise Exception(f"Invalid amount of arguments for instantiation of class {class_id}, got: {len(args)}, expected: {len(initializer.parameters)}")

        # Check if the class is completed or not
        if not class_symbol.completed:
            # Check if any of the attributes of the reference class are any type
            i = 0
            offset = None
            for idx, attr in enumerate(class_symbol.attributes):
                
                offset = attr.offset if idx == 0 else offset # Get the offset of the first attribute
                
                # Check if the attribute is of any type
                if isinstance(attr.data_type, AnyType):
                    attr.set_type(args[i])
                    i += 1
                
                attr.offset = offset
                offset += attr.size

            # At this point it is safe to assume the instantiation is valid
            # Update the size of class symbol with the new attributes
            class_symbol.set_size()
            class_symbol.completed = True

        # This means variable instantiation is a instance of the class
        return InstanceType(size=class_symbol.size, class_ref=class_symbol)


    def visitArguments(self, ctx:compiscriptParser.ArgumentsContext):
        self.log("VISIT -> Arguments node")
        # Get the expression nodes
        args = []
        for expression in ctx.expression():
            # Visit the expression node
            self.log(f"INFO -> Expression in arguments: {expression.getText()}")
            args.append(self.visitExpression(expression))
        
        return args


    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        self.log("VISIT -> Parameters node")
        # Get the parameters identifiers
        for param in ctx.IDENTIFIER():
            # Get the parameter identifier
            param_id = param.getText()
            self.log(f"INFO -> Parameter: {param_id}")

            # Create a new variable symbol for the parameter
            parameter = Variable(param_id, type="param")

            # Set the parameter as any type
            parameter.set_type(AnyType())

            # Add the parameter to the current function
            self.current_function.parameters.append(parameter)

            # Add the parameter to the symbol table
            self.add_symbol(parameter)



    def visitStatement(self, ctx:compiscriptParser.StatementContext):
        self.log("VISIT -> Statement node")

        # Check for the statement type
        # Check if the statement is expression statement
        if ctx.exprStmt():
            self.log("INFO -> Expression statement")
            self.visitExprStmt(ctx.exprStmt())

        # Check if the statement is a if statement
        elif ctx.ifStmt():
            self.log("INFO -> If statement")
            self.visitIfStmt(ctx.ifStmt())

        # Check if the statement is a while statement
        elif ctx.whileStmt():
            self.log("INFO -> While statement")
            self.visitWhileStmt(ctx.whileStmt())

        # Check if the statement is a for statement
        elif ctx.forStmt():
            self.log("INFO -> For statement")
            self.visitForStmt(ctx.forStmt())

        # Check if the statement is a return statement
        elif ctx.returnStmt():
            self.log("INFO -> Return statement")
            self.visitReturnStmt(ctx.returnStmt())

        # Check if the statement is a print statement
        elif ctx.printStmt():
            self.log("INFO -> Print statement")
            self.visitPrintStmt(ctx.printStmt())

        # Check if the statement is a block statement
        elif ctx.block():
            self.log("INFO -> Block statement")
            self.visitBlock(ctx.block())


    def visitExprStmt(self, ctx:compiscriptParser.ExprStmtContext):
        self.log("VISIT -> ExprStmt node")
        # Visit the expression node
        self.visitExpression(ctx.expression())


    def visitIfStmt(self, ctx:compiscriptParser.IfStmtContext):
        self.log("VISIT -> IfStmt node")
        # Enter the if scope
        self.enter_scope(f"if_{self.if_qty}")
        self.if_qty += 1    # Increment the if quantity

        # Visit the expression node
        type = self.visitExpression(ctx.expression())
        # Check if the expression is a boolean type
        if not isinstance(type, BooleanType) and not isinstance(type, AnyType):
            raise Exception(f"Invalid type for if statement condition got: {type}, expected: bool")
                            
        # Visit the statement node
        self.visitStatement(ctx.statement(0))

        # Exit the if scope
        self.exit_scope()

        # Check if the if statement has an else statement
        if ctx.statement(1):
            self.log("INFO -> If statement has an else statement")
            # Enter the else scope
            self.enter_scope(f"else_{self.else_qty}")
            self.else_qty += 1  # Increment the else quantity
            # Visit the else statement node
            self.visitStatement(ctx.statement(1))
            # Exit the else scope
            self.exit_scope()


    def visitForStmt(self, ctx:compiscriptParser.ForStmtContext):
        self.log("VISIT -> ForStmt node")
        # Enter the for scope
        self.enter_scope(f"for_{self.for_qty}")
        self.for_qty += 1   # Increment the for quantity

        # Check if the for has the correct definition
        # First check for the variable declaration or expression statement
        if ctx.varDecl():
            self.log("INFO -> For statement with variable declaration")
            self.visitVarDecl(ctx.varDecl())
        elif ctx.exprStmt():
            self.log("INFO -> For statement with expression statement")
            self.visitExprStmt(ctx.exprStmt())
        else:
            raise Exception(f"Invalid for statement: {ctx.getText()}, missing variable declaration or expression statement")
        
        # Visit the expression node (condition)
        if ctx.expression(0):
            self.log("INFO -> For statement condition")
            self.visitExpression(ctx.expression(0))
        else:
            raise Exception(f"Invalid for statement: {ctx.getText()}, missing condition expression")
        
        # Visit the expression node (increment)
        if ctx.expression(1):
            self.log("INFO -> For statement increment")
            self.visitExpression(ctx.expression(1))
        else:
            raise Exception(f"Invalid for statement: {ctx.getText()}, missing increment expression")
        
        # Visit the statement node
        self.visitStatement(ctx.statement())

        # Exit the for scope
        self.exit_scope()


    def visitWhileStmt(self, ctx:compiscriptParser.WhileStmtContext):
        self.log("VISIT -> WhileStmt node")
        # Enter the while scope
        self.enter_scope(f"while_{self.while_qty}")
        self.while_qty += 1 # Increment the while quantity

        # Visit the expression node
        type = self.visitExpression(ctx.expression())
        # Check if the expression is a boolean type
        if not isinstance(type, BooleanType) and not isinstance(type, AnyType):
            raise Exception(f"Invalid type for while statement condition got: {type}, expected: bool")
        
        # Visit the statement node
        self.visitStatement(ctx.statement())

        # Exit the while scope
        self.exit_scope()


    def visitReturnStmt(self, ctx:compiscriptParser.ReturnStmtContext):
        self.log("VISIT -> ReturnStmt node")

        # Check if the function is not a constructor
        if self.in_init:
            raise Exception("Constructor cannot return a value")
        
        # Check if we are inside a function
        if self.current_function is None:
            raise Exception("Return statement outside a function")

        # Check if theres a return expression
        if ctx.expression():
            # Check if the function has multiple return statements
            if self.current_function.return_count == 0:
                # Visit the expression node and set the return type of the function
                return_type = self.visitExpression(ctx.expression())
                self.current_function.set_return_type(return_type)
                self.current_function.return_count += 1
                return return_type

        else:
            self.log("INFO -> Return statement without expression")
            # The function returns nil by default
            


    def visitPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        self.log("VISIT -> PrintStmt node")
        self.in_print = True    # Set the print flag to true
        # Visit the expression node
        self.visitExpression(ctx.expression())
        # Check if the print type is a string
        self.in_print = False   # Reset the print flag