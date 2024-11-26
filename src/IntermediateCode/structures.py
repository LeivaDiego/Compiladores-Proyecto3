
class Register():
    """
    A class to represent a register in the intermediate code.

    Attr:
        id (int): The id of the register. (such as $t0, $a0, etc.)
        type (str): The type of the register. (temporary, argument, return, etc.)
        value (str): The value of the register. (type of data: string, number, etc.)
        symbol (str): The symbol of the register.  (reference to a symbol table entry)
    """
    def __init__(self, id, data_type, value, symbol = None):
        self.id = id
        self.type = data_type
        self.value = value
        self.symbol = symbol


class Stack():
    """
    A class to represent a stack in the intermediate code.
    Its purpose is to make the use of native Python lists more readable.
    """
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop(-1)

    def peek(self):
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0