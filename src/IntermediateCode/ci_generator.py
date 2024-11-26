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

        # Jump Helpers
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
                    for attribute in self.search_symbol(symbol.data_type.class_ref.id, Class).attributes:
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
    

    def create_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
        

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
        var:Variable = self.search_symbol(var_id, Variable)
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

            # Save the value to the register
            self.instruction_generator.save(var_register, temp)
            # Free the register
            self.register_controller.free_register(temp)

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
                var:Variable = self.current_class.search_attribute(var_id)   # Search for the attribute
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
                var:Variable = self.current_class.search_attribute(var_id)
                var.id = f"SELF::{var.id}" # Add the SELF prefix to the id

                # Again, we handle the instantiation in the instantiation node
                if isinstance(var.data_type, InstanceType):
                    return
                
                # Get the current register holding the value of the variable,
                # otherwise load the value to a register
                var_register = self.register_controller.get_register_with_symbol(var)
                if var_register is None:
                    # If the register is not found, load the value to a register
                    var_register = self.register_controller.new_save(var.data_type, var)    # Create a new register
                    self.instruction_generator.load(var_register, var.id)   # Load the value to the register

                # If the value is a register, save it directly,
                # otherwise load it to a register and free up the register that was holding the value
                if isinstance(var_type, Register):
                    self.instruction_generator.save(var_register, var_type)
                    self.register_controller.free_register(var_type)

                else:
                    # Create a temporal register
                    temp = self.register_controller.new_temporal(var_type)
                    # Check if the type is a variable and the data is anyType
                    # This means its a parameter, so we need to load the value to a register
                    if isinstance(var_type, Variable) and isinstance(var_type.data_type, AnyType):
                        self.instruction_generator.load(temp, f"PARAM::{var_type.id.replace('SELF::', '')}")
                    
                    # Otherwise, if isnt a anyType, and its a string, load it to a register from 
                    # the string constants buffer
                    elif isinstance(var_type, StringType):
                        self.instruction_generator.load(temp, self.string_constants.get(var_type.value, "BUFFER"))
                    
                    else:
                        # Load the value to a register
                        self.instruction_generator.load(temp, var_type.value)

                    # Save the value to the register
                    self.instruction_generator.save(var_register, temp)
                    # Free the register
                    self.register_controller.free_register(temp)
                
                # Free the register holding the value of the variable
                self.register_controller.free_register(var_register)

            # If we are not in a class assignment context and theres a call
            elif ctx.call():
                # This means we are calling a function or a class instance attribute
                self.log(f"INFO -> Call for function or class instance attribute {var_id}")
                # Get the value from call
                var_type = self.visitCall(ctx.call())
            # If we are not in a class assignment context and there is no call
            # We are assigning a value to a variable
            else:
                var_type = self.visitAssignment(ctx.assignment())
                var:Variable = self.search_symbol(var_id, Variable)

                # If its a class instance, we handle the instantiation in the instantiation node
                if isinstance(var.data_type, InstanceType):
                    return
                
                # Get the current register holding the value of the variable,
                # otherwise load the value to a register
                var_register = self.register_controller.get_register_with_symbol(var)
                if var_register is None:
                    # If the register is not found, load the value to a register
                    var_register = self.register_controller.new_save(var.data_type, var)
                    self.instruction_generator.load(var_register, var_id)

                # If the value is a register, save it directly,
                # otherwise load it to a register and free up the register that was holding the value
                if isinstance(var_type, Register):
                    self.instruction_generator.save(var_register, var_type)
                    self.register_controller.free_register(var_type)

                else:
                    # Create a temporal register
                    temp = self.register_controller.new_temporal(var_type)
                    # Check if the value is a string and not in the string constants
                    # This means its in the buffer, so we need to load it to a register
                    if isinstance(var_type, StringType):
                        self.instruction_generator.load(temp, self.string_constants.get(var_type.value, "BUFFER"))
                    else:
                        # Load the value to a register
                        self.instruction_generator.load(temp, var_type.value)

                    # Save the value to the register
                    self.instruction_generator.save(var_register, temp)
                    # Free the register
                    self.register_controller.free_register(temp)

                # Free the register holding the value of the variable
                self.register_controller.free_register(var_register)

        else:
            # If the assignment is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitLogic_or(ctx.logic_or())
        

    def visitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        self.log("VISIT -> Logic_or node")
        # Check if the logic_or is a wrapper node
        if ctx.getChildCount() > 1:
            # We need to create tags for the logic_or node, 
            # At first ignore the inverse tag for the first child and apply it to the last
            inverse_label = self.current_inverse_call
            # Iterate over the children
            for i in range(0, len(ctx.logic_and())-1):
                # Visit the logic_and node for the current child
                expression = self.visitLogic_and(ctx.logic_and(i))
                # Free the registers of the comparison
                if isinstance(expression, Register):
                    self.register_controller.free_register(expression)

            # Visit the last child with the inverse tag and apply it,
            # then apply the jump call when condition was not met
            self.current_inverse_call = inverse_label
            expression = self.visitLogic_and(ctx.logic_and(i))

            # Free the registers of the comparison
            if isinstance(expression, Register):
                self.register_controller.free_register(len(ctx.logic_and())-1)
        else:
            # If the logic_or is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitLogic_and(ctx.logic_and(0))
        

    def visitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        self.log("VISIT -> Logic_and node")
        # Check if the logic_and is a wrapper node
        if ctx.getChildCount() > 1:
            # We add labels before the next comparison and if the condition is met
            # we jump to the next comparison
            original_jump = self.current_jump_call
            # Iterate over the children
            for i in range(0, len(ctx.equality())-1):
                # Create a label for the comparison
                next_label = self.create_label()
                self.current_jump_call = next_label
                # Visit the equality node for the current child
                expression = self.visitEquality(ctx.equality(i))
                # Free the registers of the comparison
                if isinstance(expression, Register):
                    self.register_controller.free_register(expression)

                # Add the label to the instruction set
                self.instruction_generator.add_label(next_label)
            
            # Visit the last child, and apply the jump call to the next comparison
            # only if the contition is met
            self.current_jump_call = original_jump
            expression = self.visitEquality(ctx.equality(i))

            # Free the registers of the comparison
            if isinstance(expression, Register):
                self.register_controller.free_register(len(ctx.equality())-1)
        
        else:
            # If the logic_and is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitEquality(ctx.equality(0))
        

    def visitEquality(self, ctx:compiscriptParser.EqualityContext):
        self.log("VISIT -> Equality node")
        # Check if the equality is a wrapper node
        if ctx.getChildCount() > 1:
            # Get the left and right expressions
            left = self.visitComparison(ctx.comparison(0))
            
            # Iterate over the rest of the children
            for i in range(1, len(ctx.comparison())):
                # Get the right expression
                right = self.visitComparison(ctx.comparison(i))
                # Get the operator (every second child)
                operator = ctx.getChild(2 * i - 1).getText() #-> "==" | "!="
                # Check if the left expression is a register
                if isinstance(left, Register):
                    # Check the type of register and get the value
                    if left.type == "return":
                        # A return register ($v0, $v1) value must 
                        # be moved to a temporal register in order to compare
                        # it with the right expression (and not lose the return value)
                        temp = self.register_controller.new_temporal(left.value, left.symbol)
                        self.register_controller.move(temp, left)  # Move the value to the temporal register
                        self.instruction_generator.move(temp, left)  # Move the value to the temporal register
                        self.register_controller.free_register(left)  # Free the return register
                        left = temp   # Set the left expression to the temporal register
                    
                    elif isinstance(left, Variable):
                        # If the left expression is a variable, we need to load the value to a register
                        tmp = self.register_controller.get_register_with_symbol(left)
                        if tmp is None:
                            # If the register is not found, create a new register and load the value to it
                            tmp = self.register_controller.new_temporal(left.data_type, left)
                            self.instruction_generator.load(tmp, left.id)
                        left = tmp   # Set the left expression to the

                    else:
                        # If the left expression is an immediate value, we need to load it to a register
                        temp = self.register_controller.new_temporal(left)
                        # check if the left expression is a string
                        if isinstance(left, StringType):
                            # If it is, load the value from the string constants buffer
                            self.instruction_generator.load(temp, self.string_constants.get(left.value, "BUFFER"))
                        else:
                            # Otherwise, load the value to the register
                            self.instruction_generator.load(temp, left.value)

                        left = temp   # Set the left expression to the temporal register

                    # Now we need to do the same for the right expression
                    # Check if the right expression is a register
                    if isinstance(right, Register):
                        if right.type == "return":
                            # A return register ($v0, $v1) value must
                            # be moved to a temporal register in order to compare
                            # it with the left expression (and not lose the return value)
                            temp = self.register_controller.new_temporal(right.value, right.symbol)
                            self.register_controller.move(temp, right)  # Move the value to the temporal register
                            self.instruction_generator.move(temp, right)  # Move the value to the temporal register
                            self.register_controller.free_register(right)  # Free the return register
                            right = temp   # Set the right expression to the temporal register

                    elif isinstance(right, Variable):
                        # If the right expression is a variable, we need to load the value to a register
                        tmp = self.register_controller.get_register_with_symbol(right)
                        if tmp is None:
                            # If the register is not found, create a new register and load the value to it
                            tmp = self.register_controller.new_temporal(right.data_type, right)
                            self.instruction_generator.load(tmp, right.id)
                        right = tmp
                    
                    else:
                        # If the right expression is an immediate value, we need to load it to a register
                        temp = self.register_controller.new_temporal(right)
                        # check if the right expression is a string
                        if isinstance(right, StringType):
                            # If it is, load the value from the string constants buffer
                            self.instruction_generator.load(temp, self.string_constants.get(right.value, "BUFFER"))
                        else:
                            # Otherwise, load the value to the register
                            self.instruction_generator.load(temp, right.value)

                        right = temp


                    # Now get the operators and compare the values
                    if operator == "==":
                        # Equal operator
                        # Check if theres a current jump call and inverse call
                        if self.current_jump_call != "":
                            self.instruction_generator.branch_equals(left, right, self.current_jump_call)
                        if self.current_inverse_call != "":
                            self.instruction_generator.branch_not_equals(left, right, self.current_inverse_call)
                    
                    elif operator == "!=":
                        # Not equal operator
                        if self.current_jump_call != "":
                            self.instruction_generator.branch_not_equals(left, right, self.current_jump_call)
                        if self.current_inverse_call != "":
                            self.instruction_generator.branch_equals(left, right, self.current_inverse_call)

                    # Free the registers
                    self.register_controller.free_register(left)
                    self.register_controller.free_register(right)
                    left = right # Set the left expression to the right expression
                return
            
            else:
                # If the equality is a wrapper node, visit the children
                self.log("INFO -> Wrapper node, skipping...")
                return self.visitComparison(ctx.comparison(0))
            

    def visitComparison(self, ctx:compiscriptParser.ComparisonContext):
        self.log("VISIT -> Comparison node")
        # Check if the comparison is a wrapper node
        if ctx.getChildCount() > 1:
            # Get the left expression
            left = self.visitTerm(ctx.term(0))

            # Iterate over the rest of the children
            for i in range(1, len(ctx.term())):
                # Get the right expression
                right = self.visitTerm(ctx.term(i))
                # Get the operator (every second child)
                operator = ctx.getChild(2 * i - 1).getText() #-> "<" | "<=" | ">" | ">="
                # Check if the left expression is a register
                if isinstance(left, Register):
                    # Check the type of register and get the value
                    if left.type == "return":
                        # A return register ($v0, $v1) value must 
                        # be moved to a temporal register in order to compare
                        # it with the right expression (and not lose the return value)
                        temp = self.register_controller.new_temporal(left.value, left.symbol)
                        self.register_controller.move(temp, left)  # Move the value to the temporal register
                        self.instruction_generator.move(temp, left)  # Move the value to the temporal register
                        self.register_controller.free_register(left)  # Free the return register
                        left = temp   # Set the left expression to the temporal register
                
                # Check if the left expression is a variable
                elif isinstance(left, Variable):
                    # If the left expression is a variable, we need to load the value to a register
                    tmp = self.register_controller.get_register_with_symbol(left)
                    if tmp is None:
                        # If the register is not found, create a new register and load the value to it
                        tmp = self.register_controller.new_temporal(left.data_type, left)
                        self.instruction_generator.load(tmp, left.id)
                    left = tmp

                else:
                    # If the left expression is an immediate value, we need to load it to a register
                    temp = self.register_controller.new_temporal(left)
                    # check if the left expression is a string
                    if isinstance(left, StringType):
                        # If it is, load the value from the string constants buffer
                        self.instruction_generator.load(temp, self.string_constants.get(left.value, "BUFFER"))
                    else:
                        # Otherwise, load the value to the register
                        self.instruction_generator.load(temp, left.value)

                    left = temp


                # Now we need to do the same for the right expression
                # Check if the right expression is a register
                if isinstance(right, Register):
                    if right.type == "return":
                        # A return register ($v0, $v1) value must
                        # be moved to a temporal register in order to compare
                        # it with the left expression (and not lose the return value)
                        temp = self.register_controller.new_temporal(right.value, right.symbol)
                        self.register_controller.move(temp, right)  # Move the value to the temporal register
                        self.instruction_generator.move(temp, right)  # Move the value to the temporal register
                        self.register_controller.free_register(right)  # Free the return register
                        right = temp   # Set the right expression to the temporal register
                
                # Check if the right expression is a variable
                elif isinstance(right, Variable):
                    # If the right expression is a variable, we need to load the value to a register
                    tmp = self.register_controller.get_register_with_symbol(right)
                    if tmp is None:
                        # If the register is not found, create a new register and load the value to it
                        tmp = self.register_controller.new_temporal(right.data_type, right)
                        self.instruction_generator.load(tmp, right.id)
                    right = tmp

                else:
                    # If the right expression is an immediate value, we need to load it to a register
                    temp = self.register_controller.new_temporal(right)
                    # check if the right expression is a string
                    if isinstance(right, StringType):
                        # If it is, load the value from the string constants buffer
                        self.instruction_generator.load(temp, self.string_constants.get(right.value, "BUFFER"))
                    else:
                        # Otherwise, load the value to the register
                        self.instruction_generator.load(temp, right.value)
                    right = temp

                # Now get the operators and compare the values
                temp = self.register_controller.new_temporal(right.value)

                if operator == ">=":
                    # Greater or equal operator
                    # Avoid the first jump if condition is not met, in order to prevent adding unnecessary labels
                    inverse_call = self.current_inverse_call
                    self.current_inverse_call = ""  # Reset the inverse call
                    # Generate the instruction
                    self.instruction_generator.branch_equals(left, right, self.current_jump_call)
                    # Revert the inverse call if the condition is not met of being less than
                    self.current_inverse_call = inverse_call
                    # Flip the condition and generate the instruction (since theres no greater than)
                    self.instruction_generator.save_less_than(temp, right, left) # Invert the condition
                    # If the condition is met, save the value of not equal zero
                    self.instruction_generator.branch_not_equals(temp, self.register_controller.zero, self.current_jump_call)
                    # If theres a reverse condition, apply it
                    if self.current_inverse_call != "":
                        self.instruction_generator.branch_equals(temp, self.register_controller.zero, self.current_inverse_call)

                elif operator == "<=":
                    # Less or equal operator
                    # Again avoid the first jump if condition is not met, in order to prevent adding unnecessary labels
                    inverse_call = self.current_inverse_call
                    self.current_inverse_call = ""  # Reset the inverse call
                    # Generate the instruction
                    self.instruction_generator.branch_equals(left, right, self.current_jump_call)
                    # Revert the inverse call if the condition is not met of being greater than
                    self.current_inverse_call = inverse_call
                    # Flip the condition and generate the instruction (since theres no less than)
                    self.instruction_generator.save_less_than(temp, left, right) # Invert the condition
                    # If the condition is met, save the value of not equal zero
                    self.instruction_generator.branch_not_equals(temp, self.register_controller.zero, self.current_jump_call)
                    # If theres a reverse condition, apply it
                    if self.current_inverse_call != "":
                        self.instruction_generator.branch_equals(temp, self.register_controller.zero, self.current_inverse_call)

                elif operator == "<":
                    # Less than operator
                    # Generate the instruction
                    self.instruction_generator.save_less_than(temp, left, right)
                    # If the condition is met, save the value of not equal zero (true false)
                    self.instruction_generator.branch_not_equals(temp, self.register_controller.zero, self.current_jump_call)
                    # If theres a reverse condition, apply it
                    if self.current_inverse_call != "":
                        self.instruction_generator.branch_equals(temp, self.register_controller.zero, self.current_inverse_call)

                elif operator == ">":
                    # Greater than operator
                    # Flip the condition and generate the instruction (since theres no greater than)
                    self.instruction_generator.save_less_than(temp, right, left)
                    # If the condition is met, save the value of not equal zero (true false)
                    self.instruction_generator.branch_not_equals(temp, self.register_controller.zero, self.current_jump_call)
                    # If theres a reverse condition, apply it
                    if self.current_inverse_call != "":
                        self.instruction_generator.branch_equals(temp, self.register_controller.zero, self.current_inverse_call)

                # Free the registers
                self.register_controller.free_register(left)
                self.register_controller.free_register(right)
                left = right # Set the left expression to the temporal register
            return
        
        else:
            # If the comparison is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitTerm(ctx.term(0))
        

    def visitTerm(self, ctx:compiscriptParser.TermContext):
        self.log("VISIT -> Term node")
        # Check if the term is a wrapper node
        if ctx.getChildCount() > 1:
            # Get the left expression
            left = self.visitFactor(ctx.factor(0))
            # Iterate over the rest of the children
            for i in range(1, len(ctx.factor())):
                # Get the right expression
                right = self.visitFactor(ctx.factor(i))
                # Get the operator (every second child)
                operator = ctx.getChild(2 * i - 1).getText() #-> "+" | "-"

                # Check if the left expression is a register
                if isinstance(left, Register):
                    # Check the type of register and get the value
                    if left.type == "return":
                        # A return register ($v0, $v1) value must 
                        # be moved to a temporal register in order to compare
                        # it with the right expression (and not lose the return value)
                        temp = self.register_controller.new_temporal(left.value, left.symbol)
                        self.register_controller.move(temp, left)  # Move the value to the temporal register
                        self.instruction_generator.move(temp, left)  # Move the value to the temporal register
                        self.register_controller.free_register(left)  # Free the return register
                        left = temp   # Set the left expression to the temporal register

                # Check if the left expression is a variable
                elif isinstance(left, Variable):
                    # If the left expression is a variable, we need to load the value to a register
                    tmp = self.register_controller.get_register_with_symbol(left)
                    if tmp is None:
                        # If the register is not found, create a new register and load the value to it
                        tmp = self.register_controller.new_temporal(left.data_type, left)
                        self.instruction_generator.load(tmp, left.id)
                    left = tmp

                else:
                    # If the left expression is an immediate value, we need to load it to a register
                    temp = self.register_controller.new_temporal(left)
                    # check if the left expression is a string
                    if isinstance(left, StringType):
                        # If it is, load the value from the string constants buffer
                        self.instruction_generator.load(temp, self.string_constants.get(left.value, "BUFFER"))
                    else:
                        # Otherwise, load the value to the register
                        self.instruction_generator.load(temp, left.value)
                    left = temp

                
                # Now we need to do the same for the right expression
                # Check if the right expression is a register
                if isinstance(right, Register):
                    if right.type == "return":
                        # A return register ($v0, $v1) value must
                        # be moved to a temporal register in order to compare
                        # it with the left expression (and not lose the return value)
                        temp = self.register_controller.new_temporal(right.value, right.symbol)
                        self.register_controller.move(temp, right) # Move the value to the temporal register
                        self.instruction_generator.move(temp, right) # Move the value to the temporal register
                        self.register_controller.free_register(right) # Free the return register
                        right = temp   # Set the right expression to the temporal register

                elif isinstance(right, Variable):
                    # If the right expression is a variable, we need to load the value to a register
                    tmp = self.register_controller.get_register_with_symbol(right)
                    if tmp is None:
                        # If the register is not found, create a new register and load the value to it
                        tmp = self.register_controller.new_temporal(right.data_type, right)
                        self.instruction_generator.load(tmp, right.id)
                    right = tmp

                else:
                    # If the right expression is an immediate value, we need to load it to a register
                    temp = self.register_controller.new_temporal(right)
                    # check if the right expression is a string
                    if isinstance(right, StringType):
                        # If it is, load the value from the string constants buffer
                        self.instruction_generator.load(temp, self.string_constants.get(right.value, "BUFFER"))
                    else:
                        # Otherwise, load the value to the register
                        self.instruction_generator.load(temp, right.value)
                    right = temp


                # Now get the operators and compare the values
                if operator == "+":
                    # Concatenate or add operator
                    # Check if the expressions are strings, this means we need to concatenate them
                    if isinstance(left, StringType) and isinstance(right, StringType):
                        temp = self.register_controller.new_temporal(StringType(value=f"{left.value}{right.value}"))
                        self.instruction_generator.load(temp, self.string_constants.get(left.value, "BUFFER"))

                    else:
                        temp = self.register_controller.new_temporal(left.value)
                        self.instruction_generator.add(temp, left, right)

                else:
                    # Subtract operator
                    temp = self.register_controller.new_temporal(left.value)
                    self.instruction_generator.sub(temp, left, right)

                # Free the registers
                self.register_controller.free_register(left)
                self.register_controller.free_register(right)
                left = temp # Set the left expression to the temporal register
            return left
        
        else:
            # If the term is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitFactor(ctx.factor(0))
        

    def visitFactor(self, ctx:compiscriptParser.FactorContext):
        self.log("VISIT -> Factor node")
        # Check if the factor is a wrapper node
        if ctx.getChildCount() > 1:
            # Get the left expression
            left = self.visitUnary(ctx.unary(0))
            # Iterate over the rest of the children
            for i in range(1, len(ctx.unary())):
                # Get the right expression
                right = self.visitUnary(ctx.unary(i))
                # Get the operator (every second child)
                operator = ctx.getChild(2 * i - 1).getText() #-> "*" | "/" | "%"

                # Check if the left expression is a register
                if isinstance(left, Register):
                    # Check the type of register and get the value
                    if left.type == "return":
                        # A return register ($v0, $v1) value must 
                        # be moved to a temporal register in order to compare
                        # it with the right expression (and not lose the return value)
                        temp = self.register_controller.new_temporal(left.value, left.symbol)
                        self.register_controller.move(temp, left)  # Move the value to the temporal register
                        self.instruction_generator.move(temp, left)  # Move the value to the temporal register
                        self.register_controller.free_register(left)  # Free the return register
                        left = temp   # Set the left expression to the temporal register

                # Check if the left expression is a variable
                elif isinstance(left, Variable):
                    # If the left expression is a variable, we need to load the value to a register
                    tmp = self.register_controller.get_register_with_symbol(left)
                    if tmp is None:
                        # If the register is not found, create a new register and load the value to it
                        tmp = self.register_controller.new_temporal(left.data_type, left)
                        self.instruction_generator.load(tmp, left.id)
                    left = tmp

                else:
                    # If the left expression is an immediate value, we need to load it to a register
                    temp = self.register_controller.new_temporal(left)
                    # check if the left expression is a string
                    if isinstance(left, StringType):
                        # If it is, load the value from the string constants buffer
                        self.instruction_generator.load(temp, self.string_constants.get(left.value, "BUFFER"))
                    else:
                        # Otherwise, load the value to the register
                        self.instruction_generator.load(temp, left.value)
                    left = temp

                
                # Now we need to do the same for the right expression
                # Check if the right expression is a register
                if isinstance(right, Register):
                    if right.type == "return":
                        # A return register ($v0, $v1) value must
                        # be moved to a temporal register in order to compare
                        # it with the left expression (and not lose the return value)
                        temp = self.register_controller.new_temporal(right.value, right.symbol)
                        self.register_controller.move(temp, right) # Move the value to the temporal register
                        self.instruction_generator.move(temp, right) # Move the value to the temporal register
                        self.register_controller.free_register(right) # Free the return register
                        right = temp   # Set the right expression to the temporal register

                elif isinstance(right, Variable):
                    # If the right expression is a variable, we need to load the value to a register
                    tmp = self.register_controller.get_register_with_symbol(right)
                    if tmp is None:
                        # If the register is not found, create a new register and load the value to it
                        tmp = self.register_controller.new_temporal(right.data_type, right)
                        self.instruction_generator.load(tmp, right.id)
                    right = tmp

                else:
                    # If the right expression is an immediate value, we need to load it to a register
                    temp = self.register_controller.new_temporal(right)
                    # check if the right expression is a string
                    if isinstance(right, StringType):
                        # If it is, load the value from the string constants buffer
                        self.instruction_generator.load(temp, self.string_constants.get(right.value, "BUFFER"))
                    else:
                        # Otherwise, load the value to the register
                        self.instruction_generator.load(temp, right.value)
                    right = temp

                # Now get the operators and compare the values
                temp = self.register_controller.new_temporal(right.value)

                if operator == "*":
                    # Multiply operator
                    self.instruction_generator.mult(temp, left, right)
                
                elif operator == "/":
                    # Divide operator
                    self.instruction_generator.div(temp, left, right)

                elif operator == "%":
                    # Modulus operator
                    self.instruction_generator.mod(temp, left, right)

                # Free the registers
                self.register_controller.free_register(left)
                self.register_controller.free_register(right)
                left = temp # Set the left expression to the temporal register

            return left
        
        else:
            # If the factor is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitUnary(ctx.unary(0))


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