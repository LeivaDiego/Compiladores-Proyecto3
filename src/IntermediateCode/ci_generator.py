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


    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        self.log("VISIT -> VarDecl node")
        # Get the variable id
        var_id = ctx.IDENTIFIER().getText()
        # Search for the variable in the symbol table
        var = self.search_symbol(var_id, Variable)
        # Set current variable
        self.current_variable = var
        # Get the type of the variable
        var_type = self.visitExpression(ctx.expression())

        # Check if the variable is a class instance
        if isinstance(var.data_type, InstanceType):
            # This means we handle the class instance in the instantiation node
            # so we don't need to do anything here (skip it)
            return
        
        # If it isnt a class instance, we need to get the current register 
        # holding the value, otherwise we load the value to a register
        var_register = self.register_controller.get_register_with_symbol(var)

        # Check if the register is None
        if var_register is None:
            # The values has not been loaded to a register yet
            # Load the value to a register
            var_register = self.register_controller.new_save(var.data_type, var)
            # Generate the instruction
            self.instruction_generator.load(var_register, var_id)

        # Check if the variable is a Register
        # Get the value of the variable and save it directly to the register
        if isinstance(var_type, Register):
            self.instruction_generator.save(var_register, var_type) # Save the value to the register
            self.register_controller.free_register(var_type)    # Free the register
        # If it is not a register, it is a constant
        else:
            temp = self.register_controller.new_temporal(var_type)  # Create a temporal register
            # Check if the variable is a string
            if isinstance(var_type, StringType):
                # If it is, and the string is not in the string constants,
                # its in the buffer, so we need to load it to a register
                self.instruction_generator.load(temp, self.string_constants.get(var_type.value, "BUFFER"))
            
            # Otherwise assign the value to the register directly
            else:
                temp = self.instruction_generator.load(temp, var_type.value)

        # Reset the current variable
        self.current_variable = None
        # Free the register
        self.register_controller.free_register(var_register)


    def visitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        self.log("VISIT -> Assignment node")
        # Check if the assignment isn't a wrapper node
        if ctx.getChildCount() > 1:
            # Get the variable id
            var_id = ctx.IDENTIFIER().getText()
            var_type = None # Initialize the variable type

            # Check if we are in a class constructor context
            if self.in_init and self.current_class is not None and ctx.call():
                # This means we are initializing a class attribute
                # Search for it and use the offset of the class attribute to access it
                var_type = self.visitAssignment(ctx.assignment())   # Get the value of the assignment
                var = self.current_class.search_attribute(var_id)   # Search for the attribute
                var.id = f"SELF::{var.id}" # Add the SELF prefix to the id

                # Check if is and isntantiation object
                # We handle the instantiation in the instantiation node
                if isinstance(var.data_type, InstanceType):
                    return
                
                # Get the register holding the value of the variable,
                # otherwise load the value to a register
                var_register = self.register_controller.get_register_with_symbol(var)
                if var_register is None:
                    # If a register is not found, load the value to a register
                    var_register = self.register_controller.new_save(var.data_type, var)    # Create a new register
                    self.instruction_generator.load(var_register, var.id)   # Load the value to the register
                
                # If the value is a register, save it directly, 
                # otherwise load it to a register and free up the register that was holding the value
                if isinstance(var_type, Register):
                    self.instruction_generator.save(var_register, var_type) # Save the value to the register
                    self.register_controller.free_register(var_type)    # Free the register
                
                else:
                    # Create a temporal register
                    temp = self.register_controller.new_temporal(var_type)
                    # Check if the type is a variable and the data is anyType
                    # This means its a parameter, so we need to load the value to a register
                    if isinstance(var_type, Variable) and isinstance(var_type.data_type, AnyType):
                        self.instruction_generator.load(temp, f"PARAM::{var_type.id.replace('SELF::', '')}")

                    # Otherwise, if isnt a anyType, assign the value to the register directly
                    elif isinstance(var_type, Variable):
                        # Search for the register holding the value
                        tmp = self.register_controller.get_register_with_symbol(var_type)
                        # Check if the register is None
                        if tmp is None:
                            # If it is, create a new register and load the value to it
                            tmp = self.register_controller.new_temporal(var_type)
                            self.instruction_generator.load(tmp, var_type.id)

                        # Save the value to the register
                        self.instruction_generator.save(var_register, tmp)
                        # Free the register
                        self.register_controller.free_register(tmp)
                        
                    # If its a string and not in the string constants, 
                    # its in the buffer, so we need to load it to a register
                    elif isinstance(var_type, StringType):
                        self.instruction_generator.load(temp, self.string_constants.get(var_type.value, "BUFFER"))
                    
                    # Otherwise, assign the value to the register directly
                    else:
                        self.instruction_generator.load(temp, var_type.value)

                    # Save the value to the register
                    self.instruction_generator.save(var_register, temp)
                    # Free the register
                    self.register_controller.free_register(temp)
                
                # Free the register holding the value of the variable
                self.register_controller.free_register(var_register)

            # If we are not in a class constructor context but still in a class assignment
            elif ctx.call() and self.current_class is not None:
                # This means we are assigning a value to a class attribute
                # Search for the attribute in the class and use the offset to access it
                var_type = self.visitAssignment(ctx.assignment())
                # TODO: Implement the rest of the logic

    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        self.log("VISIT -> Primary node")
        # Check if the primary is a terminal node
        if ctx.getChildCount() == 1:
            primary_str = ctx.getText()

            # Check if the primary is a number
            if ctx.NUMBER():
                # Get the value
                number = ctx.NUMBER().getText()
                self.log(f"INFO -> Number: {number}")
                # Return the number type with the value
                return NumberType(value=number)
            
            # Check if the primary is a string
            elif ctx.STRING():
                # Get the value
                string = ctx.STRING().getText()
                self.log(f"INFO -> String: {string}")
                # Check if the string is not in the string constants
                if (string not in self.string_constants.keys()):
                    # if it isnt, add it to the string constants
                    self.string_constants[string] = f"STR_{self.strings_counter}"
                    self.strings_counter += 1   # Increment the counter
                    # Add the string to the data section
                    self.instruction_generator.add_to_data(StringType(value=string), self.string_constants[string])
                # Return the string type with the value
                return StringType(value=string)
            
            # Check if the primary is a boolean
            elif primary_str in ["true", "false"]:
                # Get the boolean
                boolean = primary_str
                self.log(f"INFO -> Boolean: {boolean}")
                # Return the boolean type with the value
                return BooleanType(value=boolean)
            
            # Check if the primary is a nil
            elif primary_str == "nil":
                # Get the nil
                nil = primary_str
                self.log(f"INFO -> Nil: {nil}")
                # Return the nil type with the value
                return NilType(value=nil)
            
            # Check if the primary is an identifier
            elif ctx.IDENTIFIER():
                # Get the identifier
                identifier = primary_str
                self.log(f"INFO -> Identifier: {identifier}")
                # Search for the identifier in the symbol table
                symbol = self.search_symbol(identifier, Variable)
                
                # Check if the symbol is a variable
                if symbol is None:
                    # If it is not a variable, search for it as a function
                    symbol = self.search_symbol(identifier, Function)
                    # Check if the symbol is a function
                    if symbol is None:
                        raise Exception(f"Identifier {identifier} not found in symbol table")
                    
                    # At this point the symbol is a function
                    # Return the function type
                    return symbol.return_type

                # At this point the symbol is a variable
                # Return the symbol
                return symbol
            
            # Check if the primary is 'this' directive
            elif primary_str == "this":
                self.log(f"INFO -> 'This' directive found")
                # If outside a class, this is not allowed
                if self.current_class is None:
                    raise Exception(f"'This' directive is not allowed outside a class")
            
            # Check if the primary is a class instantiation
            elif ctx.instantiation():
                self.visitInstantiation(ctx.instantiation())

        else:
            #TODO: this is an expression
            pass