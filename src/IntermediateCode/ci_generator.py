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
    

    def search_parameter(self, id, function):
        # Iterate over the symbol table in reversed order
        for symbol in reversed(self.symbol_table):
            # Check if the symbol is in the valid scope, has the correct type (param)
            if symbol.id == id and isinstance(symbol, Variable) and symbol.type == "param" and symbol.scope.id == function:
                return symbol

        # At this point, the parameter was not found
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


    def visitClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        self.log("VISIT -> ClassDecl node")
        # Get the class id
        class_id = ctx.IDENTIFIER(0).getText()
        # Set the current class
        self.current_class = self.search_symbol(class_id, Class)
        # Turn on the class assignment flag
        self.in_class_assignment = True

        # Iterate over the class functions
        for function in ctx.function():
            # Visit the function
            self.visitFunction(function)

        # Turn off the class assignment flag
        self.in_class_assignment = False
        # Reset the current class
        self.current_class = None

        return

    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        self.log("VISIT -> Function node")
        # Get the function id
        fun_id = ctx.IDENTIFIER().getText()

        # Check if the function is a constructor for a class (init)
        if fun_id == "init" and self.current_class is not None:
            self.log(f"INFO -> This function is a constructor for class: {self.current_class.id}")
            self.in_init = True  # Set the init flag to True
            self.method_flag = True  # Set the method flag to True
        
        elif self.current_class is not None and self.in_class_assignment:
            self.log(f"INFO -> This function is a method for class: {self.current_class.id}")
            self.method_flag = True  # Set the method flag to True

        # Get the function name with the class id as prefix
        fun_id = f"{fun_id.lower()}_{self.current_class.id.lower()}" if self.current_class is not None else fun_id.lower()

        # Create a new function object
        self.current_function = Function(fun_id)

        # Switch context to the function (local scope)
        self.instruction_generator.switch_context(1)
        self.instruction_generator.add_label(fun_id)  # Add the function label to the instruction set

        # Visit the function children
        self.visit(ctx.block())

        # Check if the function has a return statement
        if not self.has_return:
            # If it doesnt, add a return statement
            self.instruction_generator.jump_return()

        self.has_return = False  # Reset the return flag

        # Switch context back to the global scope
        self.instruction_generator.switch_context(0)


    def visitArguments(self, ctx:compiscriptParser.ArgumentsContext):
        self.log("VISIT -> Arguments node")
        # Initialize the arguments list
        arguments = []
        
        if isinstance(ctx, compiscriptParser.ExpressionContext):
            # If the arguments are a single expression, visit the expression
            self.log(f"INFO -> Single expression in arguments: {ctx.getText()}")
            return self.visitExpression(ctx)
        
        else:
            # Get the arguments expressions
            expressions = ctx.expression()

            for expression in expressions:
                # Iterate over the arguments and get their values
                self.log(f"INFO -> Expression in arguments: {expression.getText()}")
                arguments.append(self.visitExpression(expression))
            
            return arguments
    

    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        self.log("VISIT -> Parameters node")
        # Get the parameters identifiers
        for param in ctx.IDENTIFIER():
            # Get the parameter identifier
            param_id = param.getText()
            self.log(f"INFO -> Parameter: {param_id}")
            # Create a new variable symbol for the parameter
            parameter = self.search_parameter(param, self.current_function.id)
            # Add the parameter to the current function
            parameter.scope.id = self.current_function.id


    def visitReturnStmt(self, ctx:compiscriptParser.ReturnStmtContext):
        self.log("VISIT -> ReturnStmt node")
        # Set the return flag to True
        self.has_return = True

        # Get the value of the return statement
        val = self.visit(ctx.expression())

        # Check if the value is a variable
        if isinstance(val, Variable):
            # If it is, we need to load the value to a register
            tmp = self.register_controller.get_register_with_symbol(val)
            if tmp is None:
                # If the register is not found, create a new register and load the value to it
                tmp = self.register_controller.new_temporal(val)
                self.instruction_generator.load(tmp, val.id)
            # Generate the return instruction
            returner = self.register_controller.return_register(val.data_type)
            # Move the value to the return register
            self.instruction_generator.move(returner, tmp)
            # Free the register
            self.register_controller.free_register(tmp)
            # Add the return instruction to the instruction set
            self.instruction_generator.jump_return()
            return returner
        
        # If the value is a register, we need to move the value to the return register
        elif isinstance(val, Register):
            returner = self.register_controller.return_register(val.value)
            self.register_controller.move(returner, val)    # Move the value to the return register
            self.instruction_generator.move(returner, val)  # Move the value to the return register
            self.register_controller.free_register(val)     # Free the register
            self.instruction_generator.jump_return()        # Add the return instruction to the instruction set
            return returner
        
        else:
            # If the value is not a variable, it is an immediate value
            temp = self.register_controller.new_temporal(val)
            # Check if the value is a string
            if isinstance(val, StringType):
                # If it is, load the value from the string constants buffer
                self.instruction_generator.load(temp, self.string_constants.get(val.value, "BUFFER"))
            else:
                # Otherwise, load the value to the register
                self.instruction_generator.load(temp, val.value)

            returner = self.register_controller.return_register(val.value)
            self.register_controller.move(returner, temp)   # Move the value to the return register
            self.instruction_generator.move(returner, temp) # Move the value to the return register
            self.register_controller.free_register(temp)    # Free the register
            self.instruction_generator.jump_return()        # Add the return instruction to the instruction set
            return returner


    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        self.log("VISIT -> VarDecl node")
        # Get the variable id
        var_id = ctx.IDENTIFIER().getText()
        # Search for the variable in the symbol table
        var:Variable = self.search_symbol(var_id, Variable)
        # Set current variable
        self.current_variable = var
        # Get the type of the variable
        type = self.visitExpression(ctx.expression())

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
        if isinstance(type, Register):
            self.instruction_generator.save(var_register, type) # Save the value to the register
            self.register_controller.free_register(type)    # Free the register
        # If it is not a register, it is a constant
        else:
            temp = self.register_controller.new_temporal(type)  # Create a temporal register
            # Check if the variable is a string
            if isinstance(type, StringType):
                # If it is, and the string is not in the string constants,
                # its in the buffer, so we need to load it to a register
                self.instruction_generator.load(temp, self.string_constants.get(type.value, "BUFFER"))
            
            # Otherwise assign the value to the register directly
            else:
                self.instruction_generator.load(temp, type.value)

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
            type = None # Initialize the variable type

            # Check if we are in a class constructor context
            if self.in_init and self.current_class is not None and ctx.call():
                # This means we are initializing a class attribute
                # Search for it and use the offset of the class attribute to access it
                type = self.visitAssignment(ctx.assignment())   # Get the value of the assignment
                var:Variable = self.current_class.search_attribute(var_id)   # Search for the attribute
                new_id = f"SELF::{var.id}" # Add the SELF prefix to the id

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
                    self.instruction_generator.load(var_register, new_id)   # Load the value to the register
                
                # If the value is a register, save it directly, 
                # otherwise load it to a register and free up the register that was holding the value
                if isinstance(type, Register):
                    self.instruction_generator.save(var_register, type) # Save the value to the register
                    self.register_controller.free_register(type)    # Free the register
                
                else:
                    # Create a temporal register
                    temp = self.register_controller.new_temporal(type)
                    # Check if the type is a variable and the data is anyType
                    # This means its a parameter, so we need to load the value to a register
                    if isinstance(type, Variable) and isinstance(type.data_type, AnyType):
                        self.instruction_generator.load(temp, f"PARAM::{type.id.replace('SELF::', '')}")

                    # Otherwise, if isnt a anyType, assign the value to the register directly
                    elif isinstance(type, Variable):
                        # Search for the register holding the value
                        tmp = self.register_controller.get_register_with_symbol(type)
                        # Check if the register is None
                        if tmp is None:
                            # If it is, create a new register and load the value to it
                            tmp = self.register_controller.new_temporal(type)
                            self.instruction_generator.load(tmp, type.id)

                        # Save the value to the register
                        self.instruction_generator.save(var_register, tmp)
                        # Free the register
                        self.register_controller.free_register(tmp)
                        
                    # If its a string and not in the string constants, 
                    # its in the buffer, so we need to load it to a register
                    elif isinstance(type, StringType):
                        self.instruction_generator.load(temp, self.string_constants.get(type.value, "BUFFER"))
                    
                    # Otherwise, assign the value to the register directly
                    else:
                        self.instruction_generator.load(temp, type.value)

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
                type = self.visitAssignment(ctx.assignment())
                var:Variable = self.current_class.search_attribute(var_id)
                new_id = f"SELF::{var.id}" # Add the SELF prefix to the id

                # Again, we handle the instantiation in the instantiation node
                if isinstance(var.data_type, InstanceType):
                    return
                
                # Get the current register holding the value of the variable,
                # otherwise load the value to a register
                var_register = self.register_controller.get_register_with_symbol(var)
                if var_register is None:
                    # If the register is not found, load the value to a register
                    var_register = self.register_controller.new_save(var.data_type, var)    # Create a new register
                    self.instruction_generator.load(var_register, new_id)   # Load the value to the register

                # If the value is a register, save it directly,
                # otherwise load it to a register and free up the register that was holding the value
                if isinstance(type, Register):
                    self.instruction_generator.save(var_register, type)
                    self.register_controller.free_register(type)

                else:
                    # Create a temporal register
                    temp = self.register_controller.new_temporal(type)
                    # Check if the type is a variable and the data is anyType
                    # This means its a parameter, so we need to load the value to a register
                    if isinstance(type, Variable) and isinstance(type.data_type, AnyType):
                        self.instruction_generator.load(temp, f"PARAM::{type.id.replace('SELF::', '')}")
                    
                    # Otherwise, if isnt a anyType, and its a string, load it to a register from 
                    # the string constants buffer
                    elif isinstance(type, StringType):
                        self.instruction_generator.load(temp, self.string_constants.get(type.value, "BUFFER"))
                    
                    else:
                        # Load the value to a register
                        self.instruction_generator.load(temp, type.value)

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
                type = self.visitCall(ctx.call())
            # If we are not in a class assignment context and there is no call
            # We are assigning a value to a variable
            else:
                type = self.visit(ctx.assignment())
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
                if isinstance(type, Register):
                    self.instruction_generator.save(var_register, type)
                    self.register_controller.free_register(type)

                else:
                    # Create a temporal register
                    temp = self.register_controller.new_temporal(type)
                    # Check if the value is a string and not in the string constants
                    # This means its in the buffer, so we need to load it to a register
                    if isinstance(type, StringType):
                        self.instruction_generator.load(temp, self.string_constants.get(type.value, "BUFFER"))
                    else:
                        # Load the value to a register
                        self.instruction_generator.load(temp, type.value)

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
                expression = self.visit(ctx.logic_and(i))
                # Free the registers of the comparison
                if isinstance(expression, Register):
                    self.register_controller.free_register(expression)

            # Visit the last child with the inverse tag and apply it,
            # then apply the jump call when condition was not met
            self.current_inverse_call = inverse_label
            expression = self.visit(ctx.logic_and(i))

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
                expression = self.visit(ctx.equality(i))
                # Free the registers of the comparison
                if isinstance(expression, Register):
                    self.register_controller.free_register(expression)

                # Add the label to the instruction set
                self.instruction_generator.add_label(next_label)
            
            # Visit the last child, and apply the jump call to the next comparison
            # only if the contition is met
            self.current_jump_call = original_jump
            expression = self.visit(ctx.equality(i))

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
                right = self.visit(ctx.comparison(i))
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
                    self.register_controller.free_register(right)
                    self.register_controller.free_register(left)
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
            left = self.visit(ctx.getChild(0))

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
                        tmp = self.register_controller.new_temporal(right.data_type, left)
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
                self.register_controller.free_register(right)
                self.register_controller.free_register(left)
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
                right = self.visit(ctx.factor(i))
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
                    if isinstance(left.value, StringType) or isinstance(right.value, StringType):
                        temp = self.register_controller.new_temporal(StringType(value=str(left)+str(right)))
                        self.instruction_generator.concatenate(temp, left, right)

                    else:
                        temp = self.register_controller.new_temporal(right.value)
                        self.instruction_generator.add(temp, left, right)

                else:
                    # Subtract operator
                    temp = self.register_controller.new_temporal(right.value)
                    self.instruction_generator.sub(temp, left, right)

                # Free the registers
                self.register_controller.free_register(right)
                self.register_controller.free_register(left)
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
                right = self.visit(ctx.unary(i))
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
                self.register_controller.free_register(right)
                self.register_controller.free_register(left)
                left = temp # Set the left expression to the temporal register

            return left
        
        else:
            # If the factor is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitUnary(ctx.unary(0))


    def visitUnary(self, ctx:compiscriptParser.UnaryContext):
        return super().visitUnary(ctx)


    def visitCall(self, ctx:compiscriptParser.CallContext):
        self.log("VISIT -> Call node")
        # Check if the call isnt a wrapper node
        if ctx.getChildCount() > 1:
            # Get the call type
            call_type = self.visitPrimary(ctx.primary())

            # Check if the call is a plain function call
            if ctx.getChild(1).getText() == "(":
                # Check if the function call has arguments
                if ctx.arguments():
                    args = self.visitArguments(ctx.arguments(0))

                    # Get the function ID
                    if ctx.primary().IDENTIFIER():
                        function_id = ctx.primary().IDENTIFIER().getText()
                        # Iterate over the arguments and save the values to the registers
                        for symbol in self.symbol_table:
                            # Check if the symbol exists in the symbol table
                            if symbol.id == function_id and isinstance(symbol, Function):
                                # Check if the arguments count is the same as the function parameters count
                                for i in range(0, len(symbol.parameters)):
                                    if isinstance(args[i], Variable):
                                        reference = self.register_controller.get_register_with_symbol(args[i])
                                        if reference is None:
                                            # If the register is not found, create a new register and load the value to it
                                            reference = self.register_controller.new_temporal(args[i])
                                        
                                        # Load the value to the register
                                        self.instruction_generator.load(Register(f"PARAM::{symbol.parameters[i].id}", None, None), reference.id)
                                        self.register_controller.free_register(reference)   # Free the register

                                    else:
                                        # If the argument is not a variable, load the value to a register
                                        self.instruction_generator.load(Register(f"PARAM::{symbol.parameters[i].id}", None, None), args[i].value)

                                # Generate the jump call to the function
                                self.instruction_generator.jump_link(f"{symbol.id.lower()}")

                                return symbol.return_type
                
                return call_type
            
            # Check if the call is a class instance attribute
            elif ctx.getChild(1).getText() == ".":
                # Get the attribute identifier
                attribute = ctx.IDENTIFIER(0).getText()
                # Check if the call is inside a class definition
                if self.in_class_assignment:
                    # Search for the attribute in the class symbol table
                    symbol = self.current_class.search_attribute(attribute)
                    if symbol:
                        # Create a copy of the symbol
                        # If we dont copy the symbol, we will be modifying the original symbol
                        # and thus altering the attribute id, making it impossible to search for it
                        copy = Variable(f"SELF::{symbol.id}", symbol.type)
                        # Set the attributes of the copy
                        copy.scope = symbol.scope
                        copy.offset = symbol.offset
                        copy.data_type = symbol.data_type

                        return copy
                
                    # At this point we are calling a method using this directive
                    method = self.current_class.search_method(attribute)
                    if method:
                        # Check if it has arguments
                        if ctx.arguments():
                            arguments = ctx.arguments(0)
                            for i in range(0, len(method.parameters)):
                                arg = self.visitArguments(arguments.children[i])
                                if isinstance(arg, Variable):
                                    # Get the reference to the register
                                    reference = self.register_controller.get_register_with_symbol(arg)
                                    if reference is None:
                                        # If the register is not found, create a new register and load the value to it
                                        reference = self.register_controller.new_temporal(arg)
                                    
                                    # Load the value to the register
                                    self.instruction_generator.load(Register(f"PARAM::{method.parameters[i].id}", None, None), reference.id)
                                    # Free the register
                                    self.register_controller.free_register(reference)
                                # If the argument is not a variable, load the value to a register
                                else:
                                    self.instruction_generator.load(Register(f"PARAM::{method.parameters[i].id}", None, None), arg.value)

                                # Generate the jump call to the method
                                self.instruction_generator.jump_link(f"{method.id.lower()}_{self.current_class.id.lower()}")
                                return method.return_type
                

                # Check if the call is a class method and outside a class definition
                elif ctx.getChild(3):
                    # Get the method identifier
                    method_id = ctx.IDENTIFIER(0).getText()
                    self.log(f"INFO -> Call for class method {method_id}")

                    # Search if the method is part of the instance
                    if ctx.primary().IDENTIFIER():
                        # Get the instance identifier
                        class_id = ctx.primary().IDENTIFIER().getText()
                        class_instance = self.search_symbol(class_id, Variable)
                        # Search for the class in the symbol table
                        class_symbol = self.search_symbol(class_instance.data_type.class_ref.id, Class)

                        # If found, search for the method in the class symbol table
                        if class_symbol is not None:
                            method = class_symbol.search_method(method_id)

                            # Check if the method is found
                            if method is not None:
                                # Initialize args
                                args = None
                                # If the method has arguments, visit them
                                if ctx.arguments():
                                    # Get the arguments
                                    args = self.visitArguments(ctx.arguments(0))

                                # Generate the load of the instance to a register
                                self.instruction_generator.load(Register("SELF", None, None), class_id)

                                # Iterate over the arguments and save the values to the registers
                                for i in range(0, len(method.parameters)):
                                    # Check if its a variable
                                    if isinstance(args[i], Variable):
                                        reference = self.register_controller.get_register_with_symbol(args[i])
                                        # Check if the register is found
                                        if reference is None:
                                            # If the register is not found, create a new register and load the value to it
                                            reference = self.register_controller.new_temporal(args[i])
                                        
                                        # Load the value to the register
                                        self.instruction_generator.load(Register(f"PARAM::{method.parameters[i].id}", None, None), reference.id)
                                        self.register_controller.free_register(reference)   # Free the register 

                                    else:
                                        # If the argument is not a variable, load the value to a register
                                        self.instruction_generator.load(Register(f"PARAM::{method.parameters[i].id}", None, None), args[i].value)

                                # Generate the jump call to the method
                                self.instruction_generator.jump_link(f"{method.id.lower()}_{class_symbol.id.lower()}")

                                return method.return_type
                            
                    # Search for the metho in the symbol table
                    for symbol in self.symbol_table:
                        # Check if the symbol exists in the symbol table
                        if symbol.id == method and isinstance(symbol, Function):
                            return symbol.return_type
                        
                    # At this point the method is not found in the symbol table
                    raise Exception(f"Method {method} not found in symbol table")
                
                else:
                    # We are outside a class definition, search for the attribute in the symbol table
                    for symbol in self.symbol_table:
                        # Check if the symbol exists in the symbol table
                        if symbol.id == attribute and isinstance(symbol, Variable):
                            return symbol
                        
        else:
            # If the call is a wrapper node, visit the children
            self.log("INFO -> Wrapper node, skipping...")
            return self.visitPrimary(ctx.primary())


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
                boolean = ctx.getText()
                self.log(f"INFO -> Boolean: {boolean}")
                # Return the boolean type with the value
                return BooleanType(value=boolean)
            
            # Check if the primary is a nil
            elif primary_str == "nil":
                # Get the nil
                nil = ctx.getText()
                self.log(f"INFO -> Nil: {nil}")
                # Return the nil type with the value
                return NilType()
            
            # Check if the primary is an identifier
            elif ctx.IDENTIFIER():
                # Get the identifier
                identifier = ctx.IDENTIFIER().getText()
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
            # The primary node has children, this means it is an expression
            # or a super call

            # Check if the primary is a expression
            if ctx.expression():
                return self.visit(ctx.expression())
            
            # Check if the primari is a super call
            if ctx.getChild(0).getText() == "super":
                # Get the identifier
                identifier = ctx.IDENTIFIER().getText()
                self.log(f"INFO -> Super call for method {identifier}")
                self.super_call = True  # Set the super call flag

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



    def visitInstantiation(self, ctx: compiscriptParser.InstantiationContext):
        self.log("VISIT -> Instantiation node")
        # Get the class identifier
        class_id = ctx.IDENTIFIER().getText()
        self.log(f"INFO -> Instantiation of class {class_id}")
        # Search for the class in the symbol table
        class_symbol = self.search_symbol(class_id, Class)  # We assume the class exists (semantic should have checked this)
        
        # Initialize instance arguments
        args = None
        
        # Check if the instantiation has arguments
        if ctx.arguments():
            # Get the arguments
            args = self.visitArguments(ctx.arguments())

        # Search for the initialization method in the class symbol table
        initializer = class_symbol.search_method("init")
        
        # Load the class instance to a register
        # We use the SELF keyword to identify the instance
        self.instruction_generator.load(Register("SELF", None, None), class_id)
        # Check if the instantiation has arguments
        for i in range(0, len(initializer.parameters)):
            # Check if its a variable
            if isinstance(args[i], Variable):
                # Get the reference
                reference = self.register_controller.get_register_with_symbol(args[i])
                # Check if the register is found
                if reference is None:
                    # If the register is not found, create a new register and load the value to it
                    reference = self.register_controller.new_temporal(args[i])

                # Load the value to the register (as param)
                self.instruction_generator.load(Register(f"PARAM::{initializer.parameters[i].id}", None, None), reference.id)
                self.register_controller.free_register(reference)   # Free the register

            else:
                # If the argument is not a variable, load the value to a register
                self.instruction_generator.load(Register(f"PARAM::{initializer.parameters[i].id}", None, None), args[i].value)

        # Generate the jump call to the initialization method
        self.instruction_generator.jump_link(f"{initializer.id.lower()}_{class_symbol.id.lower()}")


    def visitIfStmt(self, ctx:compiscriptParser.IfStmtContext):
        self.log("VISIT -> IfStmt node")
        # Create the labels
        true_label = self.create_label()  # Create the true label
        false_label = self.create_label() if ctx.statement(1) else ""   # Create the false label if there is an else statement
        end_label = self.create_label() # Create the end label

        # Sabe the original destination labels
        original_inverse = self.current_inverse_call
        original_jump = self.current_jump_call
        self.current_jump_call = true_label

        # Check if theres an else statement
        # If there is, invert the condition
        self.current_inverse_call = end_label if false_label == "" else false_label
        self.visit(ctx.expression())    # Visit the expression

        # Add the true label
        self.instruction_generator.add_label(true_label)
        self.visit(ctx.statement(0))    # Visit the true statement (block for true condition)
        self.instruction_generator.jump_to(end_label)  # Jump to the end label

        # If theres a false statemet, add the false label
        if ctx.statement(1):
            self.instruction_generator.add_label(false_label)
            self.visit(ctx.statement(1))    # Visit the false statement (block for false condition)

        # Add the end label
        self.instruction_generator.add_label(end_label)
        # Retrive the original destination labels
        self.current_inverse_call = original_inverse
        self.current_jump_call = original_jump


    
    def visitWhileStmt(self, ctx:compiscriptParser.WhileStmtContext):
        self.log("VISIT -> WhileStmt node")
        # Create the labels
        start_label = self.create_label()   # Create the start of loop label
        end_label = self.create_label() # Create the end of loop label

        # Save the original destination labels
        original_inverse = self.current_inverse_call
        original_jump = self.current_jump_call

        # Due to the nature of the while loop, just need to jump out of loop
        # if the condition is not met
        self.current_inverse_call = end_label
        self.current_jump_call = ""

        self.instruction_generator.add_label(start_label)  # Add the start label
        # Visit the expression
        self.visit(ctx.expression())
        # Visit the statement
        self.visit(ctx.statement())

        # Jump back to the start of the loop
        self.instruction_generator.jump_to(start_label)

        # Add the end label
        self.instruction_generator.add_label(end_label)
        # Retrive the original destination labels
        self.current_inverse_call = original_inverse
        self.current_jump_call = original_jump


    def visitForStmt(self, ctx:compiscriptParser.ForStmtContext):
        self.log("VISIT -> ForStmt node")
        # Create the labels
        start_label = self.create_label()   # Create the start of loop label
        end_label = self.create_label() # Create the end of loop label

        # Save the original destination labels
        original_inverse = self.current_inverse_call
        original_jump = self.current_jump_call

        # Check if theres an initialization statement
        if ctx.varDecl():
            self.visit(ctx.varDecl())

        elif ctx.exprStmt():
            self.visit(ctx.exprStmt())


        # Add the start label
        self.instruction_generator.add_label(start_label)

        # Similar to the while loop, just need to jump out of loop
        # if the condition is not met
        self.current_inverse_call = end_label
        self.current_jump_call = ""

        # Visit the expression
        self.visit(ctx.expression(0))

        # Return into the original destination labels
        self.current_inverse_call = original_inverse

        # Visit the statement
        self.visit(ctx.statement())

        # Check if theres more expressions
        if ctx.expression(1):
            self.visit(ctx.expression(1))

        # Jump back to the start of the loop
        self.instruction_generator.jump_to(start_label)

        # Add the end label
        self.instruction_generator.add_label(end_label)

        # Retrive the original destination labels
        self.current_inverse_call = original_inverse
        self.current_jump_call = original_jump


    def visitPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        # Get the expression to print
        to_print = self.visit(ctx.expression())

        # Check if the expression is a variable
        if isinstance(to_print, Variable):
            # Get the register with the symbol
            tmp = self.register_controller.get_register_with_symbol(to_print)
            # Check if the register is found
            if tmp is None:
                # If the register is not found, create a new register and load the value to it
                self.instruction_generator.load(tmp, to_print.id)
                tmp = self.register_controller.new_temporal(to_print.data_type, to_print)
            # Free the register
            self.register_controller.free_register(tmp)
            # Generate the print instruction
            self.instruction_generator.print_directive(to_print.data_type, self.string_constants, tmp.id)
        
        # Check if the expression is a registr
        elif isinstance(to_print, Register):
            self.register_controller.free_register(to_print)
            self.instruction_generator.print_directive(to_print.value, self.string_constants, to_print.id)
            
        # Otherwise, the expression is an immediate value
        else:
            self.instruction_generator.print_directive(to_print, self.string_constants)