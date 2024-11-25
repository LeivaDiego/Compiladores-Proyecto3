from IntermediateCode.structures import Register
from SemanticAnalyzer.types import *

class InstructionBuilder():

    def __init__(self):
        self.data_section = [".data"]           # Data section of the CI code

        self.main_section = [".text",           # Main section of the CI code
                             ".globl main", 
                             "main:"]

        self.local_context = []                 # Local context (function) of the CI code
        self.temporary_context = []             # Temporary context of the CI code
        self.instricion_block = []              # Current instruction block

    def chage_context(self, context: int):
        """
        Change the current context of the instruction block.
            0 -> main_section
            1 -> local_context
            2 -> temporary_context
        """
        if context == 0:
            self.instricion_block = self.main_section

        elif context == 1:
            self.instricion_block = self.local_context

        elif context == 2:
            self.instricion_block = self.temporary_context

    
    def add_temp_to_local(self):
        self.local_context.extend(self.temporary_context)
        self.temporary_context.clear()

    def push_temp_to_main(self):
        self.main_section.extend(self.temporary_context)
        self.temporary_context.clear()

    def add_label(self, label: str):
        self.instricion_block.append(f"{label}:")

    def concatenate(self, reg1: Register, reg2:Register, result: Register):
        self.instricion_block.append(f"concat {result.id}, {reg1.id}, {reg2.id}")

    def add(self, reg1: Register, reg2:Register, result: Register):
        self.instricion_block.append(f"add {result.id}, {reg1.id}, {reg2.id}")

    def substract(self, reg1: Register, reg2:Register, result: Register):
        self.instricion_block.append(f"sub {result.id}, {reg1.id}, {reg2.id}")

    def multiply(self, reg1: Register, reg2:Register, result: Register):
        self.instricion_block.append(f"mult {result.id}, {reg1.id}, {reg2.id}")

    def divide(self, reg1: Register, reg2:Register, result: Register):
        self.instricion_block.append(f"div {reg1.id}, {reg2.id}")
        self.instricion_block.append(f"mflo {result.id}") # Retrieve quotient

    def mod(self, reg1: Register, reg2:Register, result: Register):
        self.instricion_block.append(f"mod {reg1.id}, {reg2.id}")
        self.instricion_block.append(f"mfhi {result.id}")  # Retrieve remainder

    def move(self, source: Register, destination: Register):
        self.instricion_block.append(f"move {destination.id}, {source.id}")

    def load(self, source: Register, destination: Register):
        self.instricion_block.append(f"load {destination.id}, {source.id}")

    def store(self, source: Register, destination: Register):
        self.instricion_block.append(f"store {destination.id}, {source.id}")

    def jump(self, label: str):
        self.instricion_block.append(f"j {label}    # Jump to {label}")

    def jump_link(self, label: str):
        self.instricion_block.append(f"jal {label}  # Jump and link to {label}")

    def jump_return(self):
        self.instricion_block.append("jr $ra    # Jump to return address")

    def branch_equal(self, reg1: Register, reg2: Register, label: str):
        self.instricion_block.append(f"beq {reg1.id}, {reg2.id}, {label}")

    def branch_not_equal(self, reg1: Register, reg2: Register, label: str):
        self.instricion_block.append(f"bne {reg1.id}, {reg2.id}, {label}")

    def branch_less_than(self, reg1: Register, reg2: Register, label: str):
        self.instricion_block.append(f"blt {reg1.id}, {reg2.id}, {label}")

    def branch_less_than_equal(self, reg1: Register, reg2: Register, label: str):
        self.instricion_block.append(f"ble {reg1.id}, {reg2.id}, {label}")

    def branch_greater_than(self, reg1: Register, reg2: Register, label: str):
        self.instricion_block.append(f"bgt {reg1.id}, {reg2.id}, {label}")

    def branch_greater_than_equal(self, reg1: Register, reg2: Register, label: str):
        self.instricion_block.append(f"bge {reg1.id}, {reg2.id}, {label}")

    def reserve_space(self, size: int):
        self.instricion_block.append(f"subi $sp, $sp, {size}    # Reserve {size} bytes in stack")

    def free_space(self, size: int):
        self.instricion_block.append(f"addi $sp, $sp, {size}    # Free up {size} bytes in stack")

    
    def print(self, reg: Register):
        # Check the type of the register to print
        if isinstance(reg.type, NumberType):
            # Set mode to print number
            self.instricion_block.append(f"load $v0, 1")

        elif isinstance(reg.type, StringType):
            self.instricion_block.append(f"load $v0, 4")
        
        # Set the register to print
        self.instricion_block.append(f"move $a0, {reg.id}")
        self.instricion_block.append(f"syscall")
