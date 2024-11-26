from CompiScript.compiscriptParser import compiscriptParser
from CompiScript.compiscriptVisitor import compiscriptVisitor
from IntermediateCode.instruction_builder import InstructionGenerator
from IntermediateCode.register_controller import RegisterController
from IntermediateCode.structures import Register
from SemanticAnalyzer.symbols import *
from SemanticAnalyzer.types import *



class IntermediateCodeGenerator(compiscriptVisitor):
    """
    Class that generates the intermediate code for the CompiScript language.
    By using the visitor pattern, this class visits the parse tree and generates
    the intermediate code for each node.

    Takes a similar approach to the SemanticAnalyzer, by using the symbol table
    """

    def __init__(self, symbol_table, logging=False):
        print("Generating Intermediate Code...")
        self.symbol_table = symbol_table        # Reference to the symbol table
        self.logging = logging                  # Flag to enable logging
        
        # Register Helpers
        self.instruction_generator = InstructionGenerator() # Object that builds semi mips instructions
        self.register_controller = RegisterController()     # Object that manages the registers (allocation, deallocation, etc)

        # Symbol Helpers
        self.current_variable: Variable = None  # Reference to the current variable
        self.current_function: Function = None  # Reference to the current function
        self.current_class: Class = None        # Reference to the current class
        self.current_jump_call = ""             # Reference to the current jump call
        self.current_inverse_call = ""          # Reference to the current inverse call
        
        
        # Helper flags
        self.in_init = False                    # Flag to indicate if we are in the init function
        self.in_class_assignment = False        # Flag to indicate if we are in a class assignment
        self.method_flag = False                # Flag to indicate if we are in a method
        self.in_print = False                   # Flag to indicate if we are in a print statement
        self.super_call = False                 # Flag to indicate if we are in a super call
        self.has_return = False                 # Flag to indicate if the function has a return statement
        
        # Counter and dictionaries
        self.strings_counter = 0                # Counter for the strings constants
        self.string_constants = {}              # Dictionary to store the string constants
        self.label_counter = 0                  # Counter for the labels

        # Adding constants to the data section
        self.add_symbols()


    def log(self, message):
        if self.logging:
            print(message)

    
    def add_symbols(self):
        """
        Function that adds the symbols entries to the symbol table to the data section
        of the intermediate code
        """
        # Iterate over the symbols
        for symbol in self.symbol_table:
            # Check if it is a variable (most important)
            if isinstance(symbol, Variable) and symbol.type == "var":
                # Add the variable to the data section
                self.instruction_generator.add_to_data(symbol.data_type, symbol.id)
                # Check if the variable is a class instance
                if isinstance(symbol.data_type, InstanceType):
                    # This means we need to add its attributes, so search for them
                    # in the class reference
                    for attribute in self.search_symbol(symbol.data_type.class_ref, Class):
                        # Add the attribute to the data section as an attribute of the class
                        # otherwize, it will be added as a variable (Pass True to is_attr)
                        self.instruction_generator.add_to_data(attribute.data_type, attribute.id, True)


    def generate_intermediate_code(self):
        # Open predefined output file
        with open("src/IntermediateCode/Output/intermediate_code.txt", "w") as file:
            # Generate the intermediate code
            file.write("\n".join(self.instruction_generator.get_instruction_set()))

        # Close the file
        file.close()
        print("SUCCESS -> Intermediate Code has been written to src/IntermediateCode/Output/intermediate_code.txt")


    def search_symbol(self, id, symbol_type:Symbol, function=None):
        """
        Search for a symbol in the symbol table and return it

        Args:
            id (str): The id of the symbol
            symbol (Symbol): The type of symbol to search for
            function (Function): The function to search for the symbol in (optional)
        """
        # Check if the function is provided
        if function:
            # Iterate over the symbol table in reversed order
            for symbol in reversed(self.symbol_table):
                # Check if the symbol is in the valid scope, has the correct type
                # and matches the id
                if symbol.id == id and isinstance(symbol, symbol_type) and symbol.scope.id == function:
                    return symbol
        # If the function is not provided
        else:
            # Iterate over the symbol table in reversed order
            for symbol in reversed(self.symbol_table):
                # Check if the symbol has correct type and matches the id
                if symbol.id == id and isinstance(symbol, symbol_type):
                    return symbol
                
        # At this point, the symbol was not found
        return None
        

    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        self.log("VISIT -> Program node")
        self.visitChildren(ctx)