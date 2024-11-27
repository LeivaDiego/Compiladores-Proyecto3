
from IntermediateCode.structures import Register
from SemanticAnalyzer.symbols import *
from SemanticAnalyzer.types import *


class InstructionGenerator():
    """
    Class that generates the 'semi' MIPS instructions for the intermediate code generation.
    """

    def __init__(self):
        self.data_section = [".data"]       # Data section of the Intermediate Code

        self.main_section =[".text",        # Main section of the Intermediate Code
                            ".globl main     # Entry point of the program",
                            'main:']
        
        # Local Context (for functions and other scoping)
        self.local_context = []             

        # Temporary context for instructions to be added onto main or local
        self.temporary_context = []

        # Instruction block to be used (initially main)
        self.instruction_block = self.main_section 

        self.has_buffer = False # Flag to check if buffer is already declared
    

    def switch_context(self, context:int):
        """
        Change the current context of the instruction block.
            0 -> main_section
            1 -> local_context
            2 -> temporary_context
        """
        if context == 0: #
            self.instruction_block = self.main_section 
        elif context == 1: #
            self.instruction_block = self.local_context
        elif context == 2: #
            self.instruction_block = self.temporary_context
        

    def push_temp_to_local(self):
        """
        Push the temporary instructions into the local context
        """
        self.local_context.extend(self.temporary_context)
        self.temporary_context = [] 
    

    def push_temp_to_main(self):
        """
        Push the temporal insturctions into main context
        """
        self.main_section.extend(self.temporary_context)
        self.temporary_context = [] 
    

    def add_label(self, label:str):
        """
        Adds a label into the instruction set,
        used for functions names, control structures, etc.
        """
        self.instruction_block.append(f'{label}:')
    

    def concatenate(self, result:Register, left:Register, right:Register):
        """
        Semi instruction to concatenate the value of two registers with one another,
        saves the result into the register passed as destination
        """
        # Semi instruction for concatenation
        self.instruction_block.append(f'concat {result.id}, {left.id}, {right.id}    # Concatenation operation')

        # Define the buffer if not already defined
        if not self.has_buffer :
            # Reserve buffer space (200 bytes for now)
            self.data_section.append("BUFFER: .space 200")
            self.has_buffer = True  # Set flag to True
            
            
    def add(self, result:Register, left:Register, right:Register):
        """
        Semi instruction to add the value of two registers with one another,
        saves the result into the register passed as result
        """
        self.instruction_block.append(f'add {result.id}, {left.id}, {right.id}    # Addition operation')
    

    def sub(self, result:Register, left:Register, right:Register):
        """
        Semi instruction to subtract the value of two registers with one another,
        saves the result into the register passed as result
        """
        self.instruction_block.append(f'sub {result.id}, {left.id}, {right.id}    # Subtraction operation')
    

    def mult(self, result:Register, left:Register, right:Register):
        """
        Semi instruction to multiply the value of two registers with one another,
        saves the result into the register passed as result
        """
        self.instruction_block.append(f'mult {result.id}, {left.id}, {right.id}    # Multiplication operation')
    

    def div(self, result:Register, left:Register, right:Register):
        """
        Semi instruction to divide the value of two registers with one another,
        saves the result (quotient) into the register passed as result
        """
        self.instruction_block.append(f"div {left.id}, {right.id}")
        self.instruction_block.append(f"mflo {result.id}    # Save the quotient (from LO register) into destination")

    
    def mod(self, result:Register, left:Register, right:Register):
        """
        Semi instruction to divide the value of two registers with one another,
        saves the result (remainder) into the register passed as result
        """
        self.instruction_block.append(f"div {left.id}, {right.id}")
        self.instruction_block.append(f"mfhi {result.id}    # Save the remainder (from HI register) into destination")


    def move(self, destination:Register, source:Register):
        """
        Semi instruction to move the value from source into the destination register
        """
        self.instruction_block.append(f'move {destination.id}, {source.id}    # Move value from {source.id} to {destination.id}')
    

    def load(self, destination:Register, source):
        """
        Semi instruction to load data into the destination register, the value
        can be a direction to memory, variable or immediate value
        """
        self.instruction_block.append(f'load {destination.id}, {source}    # Load data into register {destination.id}')
    
    def save(self, destination:Register, source:Register):
        """
        Semi instruction to save into the destination register the contents of the source register
        the destination register Must have loaded beforehand the corresponding symbol
        """
        self.instruction_block.append(f'save {destination.id}, {source.id}    # save data into register')
    

    def branch_equals(self, left:Register, right:Register, jump):
        """
        Semi intruction that compares two registers, if they are equals, jumps to the label
        """
        # Check if jump is not empty
        if jump != "":
            self.instruction_block.append(f'beq {left.id}, {right.id}, {jump}    # Jump to {jump} if equals')
        

    def branch_not_equals(self, left:Register, right:Register, jump):
        """
        Semi intruction that compares two registers, if they are not equals, jumps to the label
        """
        # Check if jump is not empty
        if jump != "":
            self.instruction_block.append(f'bne {left.id}, {right.id}, {jump}    # Jump to {jump} if not equals')
    

    def save_less_than(self, destination:Register, left:Register, right:Register):
        """
        Semi instruction that compares two registers, if left is less than right, 
        saves the result into the destination
        """
        self.instruction_block.append(f'slt {destination.id}, {left.id}, {right.id}   # Save 1 if {left.id} < {right.id} else 0')
    

    def reserve_stack(self, size):
        """
        Semi instruction to reserve space in the stack for local variables
        """
        self.instruction_block.append(f'subi $sp, $sp, {size}    # Allocate {size} bytes in the stack')


    def free_stack(self, size):
        """
        Semi instruction to free space in the stack for local variables
        """
        self.instruction_block.append(f'addi $sp, $sp, {size}    # Free up {size} bytes in the stack')


    def add_to_data(self, value, name="", is_attr=False):
        """
        Adds a value to the data section of the intermediate code
        Depending on the type of value, it will be added as a Number, String or Boolean
        """
        # Check the type of value
        # Check if the value is a Number
        if isinstance(value, NumberType):
            # If it's an attribute
            if (is_attr):
                 # Add the value to the data section with 0 as default value
                 self.data_section.append(f'    .word {value.value if value.value else "0"}')
            # If isn't an attribute
            else:
                # Add the value to the data section with the name as identifier and 0 as default value
                self.data_section.append(f'{name}: .word {value.value if value.value else "0"}')
        
        # Check if the value is a String
        elif isinstance(value, StringType):
            # If it's an attribute
            if (is_attr):
                # Add the value to the data section with the value as identifier and reserve 10 bytes for the string
                self.data_section.append(f'{("    .asciiz " + value.value )if value.value else " .space 10     # Reserve 10 bytes for the string"}')
            
            # If isn't an attribute
            else:
                # Add the value to the data section with the name as identifier and reserve 10 bytes for the string
                self.data_section.append(f'{name}: {(".asciiz " + value.value )if value.value else " .space 10     # Reserve 10 bytes for the string"}')
            
        # Check if the value is a Boolean
        elif isinstance(value, BooleanType):
            # If it's an attribute
            if (is_attr):
                # Add the value to the data section with 1 if True, 0 if False
                self.data_section.append(f'    .word {1 if value else 0}')
            # If isn't an attribute
            else:
                # Add the value to the data section with the name as identifier 
                # and 1 if True, 0 if False
                self.data_section.append(f'{name}: .word {1 if value else 0}')

        # Check if the value is a Class Instance       
        elif isinstance(value, InstanceType):
             # Set the label for the class instance only
             self.data_section.append(f'{name}:     # Class Instance {name}')
        

    def jump_to(self, label:str):
        """
        Semi instruction to jump to a label in the code
        Doesn't link, so it can't return
        """
        self.instruction_block.append(f'j {label}    # Jump to {label}')
    

    def jump_link(self, label:str):
        """
        Jump to the label and link, does return to caller,
        used for functions only
        """
        self.instruction_block.append(f'jal {label}    # Jump and link to {label}')
        

    def jump_return(self):
        """
        Semi instruction to return to the caller of a function,
        all the return values must be loaded into $v0 beforehand
        """
        self.instruction_block.append(f'jr $ra    # Return to caller')
        
    
    def print_directive(self, val, string_constants, ref_point=None):
        """
        Semi instruction set to print the value received,
        the reference is another register id that has the value
        """
        # Set the mode for the syscall
        mode = ""

        # Check the type of value
        # Check if the value is a Numeber
        if isinstance(val, NumberType):
            mode = "1"  # Set mode to print integer
            if ref_point:
                self.instruction_block.append(f"move $a0, {ref_point}   # Move register value to print into $a0")
            else:
                self.instruction_block.append(f"load $a0, {val}    # Load value to print into $a0")

        # Check if the value is a String
        elif isinstance(val, StringType):
            mode = "4"  # Set mode to print string

            # Check if the value is in the string constants
            if val in string_constants:
                # Load the string constant into $a0
                self.instruction_block.append(f"load $a0, {string_constants[val]}   # Load string to print into $a0")
            else:
                self.instruction_block.append("load $a0, BUFFER   # Load string buffer to print into $a0")

        # Add syscall instructions for printing
        self.instruction_block.append(f"load $v0, {mode}     # Set mode to print {mode}")
        self.instruction_block.append("syscall  # Print the value")
    

    def get_instruction_set(self):
        self.data_section.append("\n")  # Add a new line
        self.data_section.extend(self.main_section) # Add the main section

        # Add the end of program instructions
        self.data_section.append("# End of program")
        self.data_section.append("li $v0, 10     # Set mode to exit")
        self.data_section.append("syscall       # Exit the program")
        self.data_section.append("\n")

        # Add the local context to the data section
        self.data_section.extend(self.local_context)
        
        return self.data_section