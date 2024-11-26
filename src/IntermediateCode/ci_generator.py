from CompiScript.compiscriptParser import compiscriptParser
from CompiScript.compiscriptVisitor import compiscriptVisitor


class CIGenerator(compiscriptVisitor):

    def __init__(self, symbol_table, logging=False):
        print("Generating Intermediate Code...")
        self.symbol_table = symbol_table        # Reference to the symbol table
        self.logging = logging                  # Flag to enable logging


    def log(self, message):
        if self.logging:
            print(message)

    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.log("VISIT -> Program node")
        self.visitChildren(ctx)