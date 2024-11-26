from IntermediateCode.structures import *
from SemanticAnalyzer.types import *
from SemanticAnalyzer.symbols import *


class RegisterController(): 
    def __init__(self) -> None:
        # Dictionary for the registers in use
        self.in_use_registers = {} 

        # Counters for the registers
        self.temp_counter = 0    # Temporary registers counter
        self.arg_counter = 0    # Argument registers counter
        self.save_counter = 0    # Save registers counter
        self.stack_pointer = 0   # Stack pointer
        
        # Zero register (dedicated for the value 0)
        self.zero = Register("$zero", NumberType(value=0), 0)
        
        # Available registers stacks
        self.temp_stack = Stack() # Temporary registers available
        self.save_stack = Stack() # Save registers available
        # Theres no need for a stack for the argument registers, 
        # since they are not "reusable" like the temporals and save registers
        # we overwrite them every time we need to use them


    def free_register(self, register:Register):
        """
        Frees a register to be used again later

        Args:
            - register: the register to free
        """
        # Check the type of the register 
        # and push it to the corresponding stack
        if register.type == "tmp":
            self.temp_stack.push(register)

        elif register.type == "save": 
            self.save_stack.push(register)
        
        # Remove the register from the in_use_registers dictionary
        self.in_use_registers[register.id] = None
    

    def new_temporal(self, value:DataType, symbol=None):
        """
        Generates a new temporal register to hold a value

        Args:
            - value: the value to save into the register (can be any type from types.py)
            - symbol: if it holds a symbol value, like a variable for instance otherwise None as default
        """
        # Initialize the register
        register = None

        # Check if the temporal stack is empty
        if self.temp_stack.is_empty():
            # If it is empty, check if the counter is less than 10
            # There are only 10 temporary registers ($t0 to $t9)
            if self.temp_counter < 10:
                # Create the register id
                id = f"$t{self.temp_counter}"
                # Increment the counter
                self.temp_counter += 1
                # Create the register object
                register = Register(id, "tmp", value, symbol)

            # This means there are no more temporals available
            # We will use the stack pointer to store the value
            else: 
                # Get the stack offset (stack_pointer) and create the register id
                id = f'{self.stack_pointer}($sp)'
                # Create the register object
                register = Register(id, "sp", value, symbol)
                # Increment the stack pointer
                self.stack_pointer += value.size

        # If the stack is not empty
        else:
            # Pop the register from the stack
            register = self.temp_stack.pop()
            # Update the value and symbol
            register.value = value
            # If a symbol is passed, update the symbol
            register.symbol = symbol
           
        # Finally, save the symbol if it was passed, otherwise the value
        # and add the register to the in_use_registers dictionary
        self.in_use_registers[register.id] = symbol if symbol else value

        # Return the register
        return register
    

    def new_argument(self, value:DataType, symbol=None):
        """
        Generates a register to hold a value as a parameter,
        similar to the new_temporal method, but for arguments
        (argument registers are $a0 to $a3)

        Args:
            - value: the value to save into the register (can be any type from types.py)
            - symbol: if it holds a symbol value, like a variable for instance otherwise None as default
        """
        # Initialize the register
        register = None
        
        # Check if the argument counter is less than 3
        if self.arg_counter < 3:
            # Create the register id
            id = f"$a{self.arg_counter}"
            # Increment the counter
            self.arg_counter += 1
            # Create the register object
            register = Register(id, "arg", value, symbol)

        # If the counter is greater than 3 (no more argument registers available)
        # We will use the stack pointer to store the value
        else:
            # Get the stack offset (stack_pointer) and create the register id
            id = f'{self.stack_pointer}($sp)'
            # Create the register object
            register = Register(id,"sp", value, symbol)
            # Increment the stack pointer by the size of the value
            self.stack_pointer += value.size
           
        # Finally, save the symbol if it was passed, otherwise the value
        # and add the register to the in_use_registers dictionary
        self.in_use_registers[register.id] = symbol if symbol else value

        # Return the register
        return register 
    

    def reset_arguments(self):
        """
        Resets the argument counter
        """
        self.arg_count = 0
        

    def new_save(self, value:DataType, symbol):
        """
        Generates a register that will be used to save the values of variables into memory
        similar to the new_temporal method, but for save registers ($s0 to $s7)

        Args:
            - value: the value to save into the register (can be any type from types.py)
            - symbol: if it holds a symbol value, like a variable for instance otherwise None as default
        """
        # Initialize the register
        register = None
        # Check if the save stack is empty
        if self.save_stack.is_empty():
            # If it is empty, check if the counter is less than 7
            if self.save_counter < 7:
                # Create the register id
                id = f"$s{self.save_counter}"
                # Increment the counter
                self.save_counter += 1
                # Create the register object
                register = Register(id, "save", value, symbol)

            # If there are no more save registers available,
            # we will use the stack pointer to store the value (very unlikely scenario)
            else:
                # Get the stack offset (stack_pointer) and create the register id
                id = f'{self.stack_pointer}($sp)'
                # Create the register object
                register = Register(id, "sp", value, symbol)
                # Increment the stack pointer by the size of the value
                self.stack_pointer += value.size
        
        # If the stack is not empty
        else:
            # Pop the register from the stack
            register = self.temp_stack.pop()
            # Update the value and symbol
            register.value = value
            # If a symbol is passed, update the symbol
            register.symbol = symbol
           
        # Finally, save the symbol if it was passed, otherwise the value
        # and add the register to the in_use_registers dictionary
        self.in_use_registers[register.id] = symbol if symbol else value

        # Return the register
        return register


    def return_register(self, value:DataType): #set the value of the return register to the value passed   
        """
        Sets the return register to the value passed

        Args:
            - value: the value to set into the return register
        """
        # Set the value of the return register to the value passed
        self.in_use_registers["$v0"] = value
        # Return the register with the updated value
        return Register("$v0", "return", value)
    

    def move(self, destination:Register, source:Register):
        """
        Moves the value of the source register into the destination register
        and frees the source register

        Args:
            - destination: the register to move the value to
            - source: the register to move the value from
        """
        # Set the value of the destination register to the value of the source register 
        # and free the source register
        self.in_use_registers[destination.id] = source.symbol if source.symbol else source.value
        self.free_register(source)
        
        # Return the destination register
        destination.symbol = source.symbol
        destination.value = source.value
        
        # Return the destination register
        return destination
    

    def get_register_with_symbol(self, symbol:Symbol):
        """
        Searches for the register with the symbol passed,
        and returns the register if found, otherwise None

        Args:
            - symbol: the symbol to search for in the registers
        """
        # Iterate over the in_use_registers dictionary
        for id, value in self.in_use_registers.items():
            # Check if the value is a symbol and 
            # if it is the same as the symbol passed
            if value is symbol or value == symbol:
                # Check the type of the register
                type = ""
                # Check if the register is a temporary register
                if ("$t") in id:
                    type = "tmp"

                # Check if the register is an argument register
                elif ("$s") in id:
                    type = "save"

                # Return the register with the symbol
                return Register(id, type, value.data_type, value)
            
        # At this point, the register was not found
        return None