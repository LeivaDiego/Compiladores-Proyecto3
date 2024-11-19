from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from SemanticAnalyzer.symbols import Symbol, Variable, Function, Class, Scope
from SemanticAnalyzer.types import DataType, StringType, BooleanType, NumberType, NilType, AnyType


class SemanticAnalyzer(compiscriptVisitor):
    def __init__(self, logging=False):
        self.logging = logging # Flag to enable logging
        print("Starting Semantic Analysis...")
        # Scoping and symbol table
        self.current_scope: Scope = None        # The current scope
        self.scope_stack: list[Scope] = []      # The scope stack
        self.symbol_table = []                  # The symbol table

        # Symbol helpers
        self.current_variable: Variable = None  # The current variable
        self.current_function: Function = None  # The current function
        self.class_stack: list[Class] = []      # The class stack (for nested classes)
        self.current_class: Class = None        # The current class


    def log(self, message):
        if self.logging:
            print(f"    {message}")


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
            symbol.scope = self.current_class.scope
        else:
            # Otherwise, set the scope to the current scope
            symbol.scope = self.current_scope

        # Add the symbol to the symbol table
        self.symbol_table.append(symbol)
        # Log the symbol addition
        self.log(f"ADDED SYMBOL -> {symbol}")


    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.log("VISIT -> Program node")
        # Enter the global scope
        self.enter_scope("global")
        # visit the children of the program node
        self.visitChildren(ctx)


    def visitExpression(self, ctx:compiscriptParser.ExpressionContext):
        self.log("VISIT -> Expression node")
        self.log(f"INFO -> Expression: {ctx.getText()}")
        # Check if the expression is an assignment
        if ctx.assignment():
            self.visitAssignment(ctx.assignment())
        # Check if the expression is a anonymous function
        elif ctx.funAnon():
            self.visitFunAnon(ctx.funAnon())
        else:
            # The expression is not a valid expression
            raise Exception(f"Invalid expression: {ctx.getText()}")
        

    def visitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        self.log("VISIT -> Assignment node")
        # Check if the assignment isn't a wrapper node
        if ctx.getChildCount() > 1:
            # Get the variable id
            var_id = ctx.IDENTIFIER().getText()
            # Check if the assignment is for a class attribute
            if ctx.call():
                # TODO: Get the class attribute id
                self.visitCall(ctx.call())
                # TODO: check for the class attribute in the instance
                self.log(f"INFO -> Assignment for a class attr")

            else:
                # The assignment is for a variable
                # TODO: check for the variable in the symbol table
                self.log(f"INFO -> Assignment for a variable")
            
            # Visit the assignment node
            self.visitAssignment(ctx.assignment())

        else:
            # The assignment is a wrapper node, skip it
            # and visit the logic_or node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitLogic_or(ctx.logic_or())

    
    def visitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        self.log("VISIT -> Logic_or node")

        # Check if the logic_or isn't a wrapper node
        if ctx.getChildCount() > 1:
            logic_ands = []
            # TODO: Get the logic_and nodes and visit them
            self.log(f"INFO -> Logic_or node: {ctx.getText()}")

        else:
            # The logic_or is a wrapper node, skip it
            # and visit the logic_and node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitLogic_and(ctx.logic_and(0))


    def visitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        self.log("VISIT -> Logic_and node")

        # Check if the logic_and isn't a wrapper node
        if ctx.getChildCount() > 1:
            equalities = []
            # TODO: Get the equality nodes and visit them
            self.log(f"INFO -> Logic_and node: {ctx.getText()}")
            
        else:
            # The logic_and is a wrapper node, skip it
            # and visit the equality node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitEquality(ctx.equality(0))


    def visitEquality(self, ctx:compiscriptParser.EqualityContext):
        self.log("VISIT -> Equality node")

        # Check if the equality isn't a wrapper node
        if ctx.getChildCount() > 1:
            comparisons = []
            # TODO: Get the comparison nodes and visit them
            self.log(f"INFO -> Equality node: {ctx.getText()}")

        else:
            # The equality is a wrapper node, skip it
            # and visit the comparison node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitComparison(ctx.comparison(0))


    def visitComparison(self, ctx:compiscriptParser.ComparisonContext):
        self.log("VISIT -> Comparison node")

        # Check if the comparison isn't a wrapper node
        if ctx.getChildCount() > 1:
            terms = []
            # Get the term nodes
            for term in ctx.term():
                # TODO: visit the term node and get type
                self.visitTerm(term)
                self.log(f"INFO -> Term node: {term}")

        else:
            # The comparison is a wrapper node, skip it
            # and visit the term node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitTerm(ctx.term(0))

    
    def visitTerm(self, ctx:compiscriptParser.TermContext):
        self.log("VISIT -> Term node")

        # Check if the term isn't a wrapper node
        if ctx.getChildCount() > 1:
            factors = []
            # Get the factor nodes
            for factor in ctx.factor():
                # TODO: visit the factor node and get type
                self.visitFactor(factor)
                self.log(f"INFO -> Factor node: {factor}")

        else:
            # The term is a wrapper node, skip it
            # and visit the factor node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitFactor(ctx.factor(0))


    def visitFactor(self, ctx:compiscriptParser.FactorContext):
        self.log("VISIT -> Factor node")

        # Check if the factor isn't a wrapper node
        if ctx.getChildCount() > 1:
            # Get the unary nodes
            for unary in ctx.unary():
                # TODO: visit the unary node and get type
                self.visitUnary(unary)
                self.log(f"INFO -> Unary node: {unary}")

        else:
            # The factor is a wrapper node, skip it
            # and visit the unary node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitUnary(ctx.unary(0))


    def visitUnary(self, ctx:compiscriptParser.UnaryContext):
        self.log("VISIT -> Unary node")

        # Check if the unary isn't a wrapper node
        if ctx.getChildCount() > 1:
            # Check if the unary is a negation operator
            if ctx.getChild(0).getText() in ["!", "-"]:
                # Get the negation operator
                negation = ctx.getChild(0).getText()
                # Visit the unary node
                self.visitUnary(ctx.unary())
                # TODO: check for the type of the unary node
            
            else:
                # If isnt a negation operator, its not a valid unary operator
                raise Exception(f"Invalid unary operator: {ctx.getChild(0).getText()}")

        else:
            # The unary is a wrapper node, skip it
            # and visit the primary node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitCall(ctx.call())


    def visitCall(self, ctx:compiscriptParser.CallContext):
        self.log("VISIT -> Call node")

        # Check if the call isn't a wrapper node
        if ctx.getChildCount() > 1:
            # Check if the call is a function call
            if ctx.arguments():
                # TODO: Get the function arguments
                self.visitArguments(ctx.arguments())

            # Check if theres an identifier (idk why...)
            elif ctx.IDENTIFIER():
                # Get the identifier
                identifier = ctx.IDENTIFIER().getText()
                # TODO: maybe search for the identifier...

        else:
            # The call is a wrapper node, skip it
            # and visit the primary node
            self.log("INFO -> Wrapper node, skipping...")
            self.visitPrimary(ctx.primary())


    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        self.log("VISIT -> Primary node")

        # Check if the primary is a terminal node
        if ctx.getChildCount() == 1:
            primary_str = ctx.getText()

            # Check if the primary is a number
            if ctx.NUMBER():
                # Get the number
                number = ctx.NUMBER().getText()
                self.log(f"INFO -> Number: {number}")

            # Check if the primary is a string
            elif ctx.STRING():
                # Get the string
                string = ctx.STRING().getText()
                self.log(f"INFO -> String: {string}")

            # Check if the primary is a boolean
            elif primary_str in ["true", "false"]:
                # Get the boolean
                boolean = primary_str
                self.log(f"INFO -> Boolean: {boolean}")

            # Check if the primary is a nil
            elif primary_str == "nil":
                # Get the nil
                nil = primary_str
                self.log(f"INFO -> Nil: {nil}")

            # Check if the primary is an identifier
            elif ctx.IDENTIFIER():
                # Get the identifier
                identifier = ctx.IDENTIFIER().getText()
                self.log(f"INFO -> Identifier: {identifier}")

            # Check if the primary is a instantiation
            elif ctx.instantiation():
                self.visitInstantiation(ctx.instantiation())

        else:
            # The primary has children, is a expression or a super call
            # Check if the primary is a expression
            if ctx.expression():
                self.visitExpression(ctx.expression())

            # Check if the primary is a super call
            if ctx.getChild(0).getText() == "super":
                identifier = ctx.IDENTIFIER().getText()
                self.log(f"INFO -> Super call: {identifier}")


    def visitInstantiation(self, ctx:compiscriptParser.InstantiationContext):
        self.log("VISIT -> Instantiation node")
        # Get the class identifier
        class_id = ctx.IDENTIFIER().getText()
        # TODO: check for the class in the symbol table
        
        # Check if the instantiation has arguments
        if ctx.arguments():
            # Get the arguments
            self.visitArguments(ctx.arguments())


    def visitArguments(self, ctx:compiscriptParser.ArgumentsContext):
        self.log("VISIT -> Arguments node")
        # Visit each expression in the arguments
        for expression in ctx.expression():
            self.visitExpression(expression)
            # TODO: check for the type of the expression node
            self.log(f"INFO -> Argument: {expression.getText()}")