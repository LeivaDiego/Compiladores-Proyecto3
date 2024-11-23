from CompiScript.compiscriptParser import compiscriptParser
from CompiScript.compiscriptVisitor import compiscriptVisitor


class ExpressionTAC():
    def __init__(self):
        self.instructions = []
        self.completed = False

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def set_completed(self):
        self.completed = True


class TAC_Generator(compiscriptVisitor):
    def __init__(self, logging=False, ctx:compiscriptParser.ExpressionContext=None):
    
        self.logging = logging      # Flag to enable logging    
        self.tac = ExpressionTAC()  # Expression TAC
        self.temp_count = 0         # Temp variable count

        self.log(f"TAC -> Generating for: {ctx.getText()}")
        self.visit(ctx)


    def log(self, message):
        if self.logging:
            print(f"        {message}")

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def visitExpression(self, ctx:compiscriptParser.ExpressionContext):
        self.log("TAC -> Expression node")
        # Initialize Expression object if its not available
        if not self.tac:
            self.tac = ExpressionTAC()
        # Visit all the children of the expression node
        self.visitAssignment(ctx.assignment())

    def visitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        self.log("TAC -> Assignment node")

        # Check if the assignment is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Assignment is not a wrapper node")
            # TODO: Implement TAC generation for assignment

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitLogic_or(ctx.logic_or())

    def visitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        self.log("TAC -> Logic_or node")
        # Check if the logic_or is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Logic_or is not a wrapper node")
            # TODO: Implement TAC generation for logic_or

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitLogic_and(ctx.logic_and(0))


    def visitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        self.log("TAC -> Logic_and node")
        # Check if the logic_and is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Logic_and is not a wrapper node")
            # TODO: Implement TAC generation for logic_and

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitEquality(ctx.equality(0))

    def visitEquality(self, ctx:compiscriptParser.EqualityContext):
        self.log("TAC -> Equality node")
        # Check if the equality is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Equality is not a wrapper node")
            # TODO: Implement TAC generation for equality

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitComparison(ctx.comparison(0))

    def visitComparison(self, ctx:compiscriptParser.ComparisonContext):
        self.log("TAC -> Comparison node")
        # Check if the comparison is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Comparison is not a wrapper node")
            # TODO: Implement TAC generation for comparison

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitTerm(ctx.term(0))


    def visitTerm(self, ctx:compiscriptParser.TermContext):
        self.log("TAC -> Term node")
        # Check if the term is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Term is not a wrapper node")
            # TODO: Implement TAC generation for term

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitFactor(ctx.factor(0))

    def visitFactor(self, ctx:compiscriptParser.FactorContext):
        self.log("TAC -> Factor node")
        # Check if the factor is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Factor is not a wrapper node")
            # TODO: Implement TAC generation for factor

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitUnary(ctx.unary(0))

    def visitUnary(self, ctx:compiscriptParser.UnaryContext):
        self.log("TAC -> Unary node")
        # Check if the unary is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Unary is not a wrapper node")
            # TODO: Implement TAC generation for unary

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitCall(ctx.call())

    def visitCall(self, ctx:compiscriptParser.CallContext):
        self.log("TAC -> Call node")
        # Check if the call is a wrapper node
        if ctx.getChildCount() > 1:
            self.log("TAC -> Call is not a wrapper node")
            # TODO: Implement TAC generation for call

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitPrimary(ctx.primary())

    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        self.log("TAC -> Primary node")
        # Check if the primary is a terminal node
        if ctx.getChildCount() == 1:
            self.log("TAC -> Primary is a terminal node")
            # TODO: Implement TAC generation for primary

        else:
            self.log("TAC -> This is a wrapper node, skipping...")
            self.visitExpression(ctx.expression())