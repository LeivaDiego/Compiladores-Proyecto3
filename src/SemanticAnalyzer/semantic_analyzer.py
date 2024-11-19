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

        self.log(f"INFO -> Class declaration for: {class_id}")

        # Check if the class inherits from another class
        if ctx.IDENTIFIER(1):
            # Get the parent class identifier
            parent_id = ctx.IDENTIFIER(1).getText()
            self.log(f"INFO -> Inherits from class: {parent_id}")
            # TODO: search for the class in the symbol table

        # Create a new class symbol
        if parent_class is not None:
            # TODO: create a new class symbol with parent attributes and methods
            self.log(f"INFO -> Creating class symbol with parent attributes and methods")
        else:
            # The class is standalone without a parent
            self.log(f"INFO -> Creating standalone class symbol")
            # TODO: create a new class symbol without parent attributes and methods


        # Enter the class scope
        self.enter_scope(class_id)

        # Visit the class body
        for function in ctx.function():
            # Visit each function in the class body
            self.log(f"INFO -> Visiting function in class body")
            self.visitFunction(function)
            # TODO: visit the function node and add it to the symbol table

        # TODO: after visiting all the functions, set the size of the class

        # Exit the class scope
        self.exit_scope()

        # TODO: add the class symbol to the symbol table


    def visitFunDecl(self, ctx:compiscriptParser.FunDeclContext):
        self.log("VISIT -> FunDecl node")
        # Visit the function node
        self.visitFunction(ctx.function())

    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        self.log("VISIT -> Function node")
        # Get the function identifier
        fun_id = ctx.IDENTIFIER().getText()
        self.log(f"INFO -> Function declaration for: {fun_id}")

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

        # TODO: create a new function symbol

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

        # Check if the variable has an assignment
        if ctx.expression():
            # Visit the expression node
            self.visitExpression(ctx.expression())
            #TODO: assign the type of the expression to the variable
        else:
            # If the variable doesn't have an assignment we can't infer the type
            # set the type to any
            self.log(f"INFO -> Variable type set to any")


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
                self.log(f"INFO -> Assignment for a class attr {var_id}")
                # TODO: Get the class attribute id
                self.visitCall(ctx.call())
                # TODO: check for the class attribute in the instance
                

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
            for logic_and in ctx.logic_and():
                self.log(f"INFO -> logic_and node: {logic_and.getText()}")
                self.visitLogic_and(logic_and)
            

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
            for equality in ctx.equality():
                self.log(f"INFO -> equality node: {equality.getText()}")
                self.visitEquality(equality)
                
            
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
            for comparison in ctx.comparison():
                self.log(f"INFO -> Comparison node: {comparison.getText()}")
                self.visitComparison(comparison)

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
                self.log(f"INFO -> Term node: {term.getText()}")
                self.visitTerm(term)

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
                self.log(f"INFO -> Factor node: {factor.getText()}")
                self.visitFactor(factor)
                
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
                self.log(f"INFO -> Unary node: {unary.getText()}")
                self.visitUnary(unary)

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
            
            # TODO: Get the function identifier
            self.visitPrimary(ctx.primary())

            # Check if the call is a function call
            if ctx.getChild(1).getText() == "(":
                

                # Check if the function call has arguments
                if ctx.arguments():
                    # TODO: Get the function arguments
                    self.visitArguments(ctx.arguments(0))

            # Check if the call is a class attribute call
            elif ctx.getChild(1).getText() == ".":
                # Get the attribute identifier
                attribute = ctx.IDENTIFIER(0).getText()
                self.log(f"INFO -> Attribute: {attribute}")

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
                # TODO: check for the identifier in the symbol table

            # Check if the primary is a this keyword
            elif primary_str == "this":
                self.log(f"INFO -> this keyword")
                # TODO: check for the current class

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
        # Get the expression nodes
        for expression in ctx.expression():
            # Visit the expression node
            self.log(f"INFO -> Expression in arguments: {expression.getText()}")
            self.visitExpression(expression)


    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        self.log("VISIT -> Parameters node")
        # Get the parameters identifiers
        for param in ctx.IDENTIFIER():
            # Get the parameter identifier
            param_id = param.getText()
            self.log(f"INFO -> Parameter: {param_id}")

            # TODO: create a new variable symbol for the parameter
            # TODO: set the type of the variable as parameter type
            # TODO: set the parameter as any type
            # TODO: add the parameter to the symbol table


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
        self.enter_scope("if")

        # Visit the expression node
        self.visitExpression(ctx.expression())
        # TODO: check for the type of the expression

        # Visit the statement node
        self.visitStatement(ctx.statement(0))

        # Exit the if scope
        self.exit_scope()

        # Check if the if statement has an else statement
        if ctx.statement(1):
            self.log("INFO -> If statement has an else statement")
            # Enter the else scope
            self.enter_scope("else")
            # Visit the else statement node
            self.visitStatement(ctx.statement(1))
            # Exit the else scope
            self.exit_scope()


    def visitForStmt(self, ctx:compiscriptParser.ForStmtContext):
        self.log("VISIT -> ForStmt node")
        # Enter the for scope
        self.enter_scope("for")

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
        self.enter_scope("while")

        # Visit the expression node
        self.visitExpression(ctx.expression())

        # Visit the statement node
        self.visitStatement(ctx.statement())

        # Exit the while scope
        self.exit_scope()


    def visitReturnStmt(self, ctx:compiscriptParser.ReturnStmtContext):
        self.log("VISIT -> ReturnStmt node")

        # Check if theres a return expression
        if ctx.expression():
            # Visit the expression node
            self.visitExpression(ctx.expression())
        else:
            self.log("INFO -> Return statement without expression")
            # TODO: this means we are returning nil

    def visitPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        self.log("VISIT -> PrintStmt node")
        # Visit the expression node
        self.visitExpression(ctx.expression())
        #TODO: check for the type of the expression must be string