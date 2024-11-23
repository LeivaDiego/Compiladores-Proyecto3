
class DataStruct():
    def __init__(self, name, size, value):
        self.name = name
        self.size = f"{size}"
        self.value = value


    def __str__(self):
        return f"{self.name}: .{self.size} {self.value}"
    

class DataSection():
    def __init__(self):
        self.data = []
        self.str_count = 0
        self.add_new_line()

    def add_data(self, datastruct):
        self.data.append(datastruct)
        self.str_count += 1

    def add_new_line(self):
        self.data.append(DataStruct("newLine", "asciiz", r'"\n"'))

    def __str__(self):
        return '.data\n\t'+"\n\t".join([str(data) for data in self.data])
    

class TAC():
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


class ExpressionTAC():
    def __init__(self, result):
        self.result = result
        self.code = []

    def add_tac(self, tac):
        self.code.append(tac)

    def __str__(self):
        return '\n'.join([str(tac) for tac in self.code])
    

class CodeBlock():
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __str__(self):
        return f"\t{self.name}:\n" + '\n\t'.join([str(tac) for tac in self.code])
    

class TextSection():
    def __init__(self):
        self.code_blocks = []

    def add_code_block(self, code_block):
        self.code_blocks.append(code_block)

    def __str__(self):
        return '.text\n\t'+"\n\t".join([str(code_block) for code_block in self.code_blocks])