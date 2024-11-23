from CompiScript.compiscriptParser import compiscriptParser
from CompiScript.compiscriptVisitor import compiscriptVisitor
from Intermediate.tac_generator import TAC_Generator
from Utils.file_utils import generate_name

class IntermediateGenerator(compiscriptVisitor):
    def __init__(self, input_file, symbol_table, logging=False):
        print("Generating Intermediate Code...")

        self.logging = logging  # Flag to enable logging

        # Generate a MIPS file name based on the input file name
        self.out_name = generate_name(input_file)
        # Base MIPS code path
        self.base_mips_code = "src/Intermediate/Out/"

        # Symbol table
        self.symbol_table = symbol_table

        # Expression
        self.in_expression = False

        self.expr_tacs = {} # Dictionary to store all the expressions TACs


    def log(self, message):
        if self.logging:
            print(f"    {message}")

    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.log("VISIT -> Program node")
        # Visit all the children of the program node
        self.visitChildren(ctx)

    
    def visitExpression(self, ctx:compiscriptParser.ExpressionContext):
        self.log("VISIT -> Expression node")
        # Check if we are already in an expression
        if self.in_expression:
            return
        # Set the flag to True, and create a TAC generator object
        else:
            expr = ctx.getText()
            self.in_expression = True
            # The generator will create the TAC for the expression
            tac_gen = TAC_Generator(logging = self.logging, ctx = ctx)
            # Get the TAC for the expression
            self.expr_tacs[expr] = tac_gen.tac
            # Set the flag to False
            self.in_expression = False
            return