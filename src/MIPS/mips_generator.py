from CompiScript.compiscriptParser import compiscriptParser
from CompiScript.compiscriptVisitor import compiscriptVisitor
from Utils.file_utils import generate_name
from SemanticAnalyzer.symbols import Symbol, Variable, Function, Class
from SemanticAnalyzer.types import DataType, NumberType, StringType, BooleanType, NilType, AnyType
from MIPS.structures import DataStruct, DataSection, TAC, CodeBlock, TextSection

class MipsGenerator(compiscriptVisitor):
    def __init__(self, input_file, symbol_table, logging=False):
        self.logging = logging
        self.output_name = generate_name(path=input_file, base_name='mips_')
        self.symbol_table = symbol_table

        print(f"Generating MIPS code for {input_file}...")
        
        self.current_block = None
        self.current_tac = None
        self.data_section = DataSection()
        self.text_section = TextSection()
        self.current_data: DataStruct = None

    def log(self, message):
        if self.logging:
            print(message)

    def generate_file(self):
        with open(f"src/MIPS/Out/{self.output_name}.s", 'w') as file:
            file.write(str(self.data_section))
            file.write('\n\n')
            file.write(str(self.text_section))

    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.log("VISIT -> Program node")
        self.visitChildren(ctx)

    def visitPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        self.log("VISIT -> PrintStmt node")
        # We need to extract the strings from the print statement        
        self.visitChildren(ctx)
        # TODO: handle TAC to print the strings and variables

    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        self.log("VISIT -> Primary node")
        # Check if this is a terminal node
        if ctx.getChildCount() == 1:
            # Check if this is a string
            if ctx.STRING():
                # Extract the string and add it to the data section
                string = ctx.STRING().getText()
                self.current_data = DataStruct(f"str{self.data_section.str_count}", "asciiz", string)
                self.data_section.add_data(self.current_data)
                self.log(f"INFO -> Added string {string} to data section")

    