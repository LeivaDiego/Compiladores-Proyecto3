from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from Analyzer.objetc_types import ObjectType, VariableType, FunctionType, ClassType
from Analyzer.data_types import DataType, NumberType, StringType, BooleanType, NilType
from Analyzer.scoping import Scope, ScopeManager


class SymbolTableGenerator(compiscriptVisitor):
    def __init__(self):
        self.current_class : ClassType = None
        self.current_function : FunctionType = None
        self.current_variable: VariableType = None
        self.scope_manager = ScopeManager()

    # Visit a parse tree produced by compiscriptParser#program.
    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        print("INFO -> Entered Program")
        self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#varDecl.
    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        print("INFO -> Entered Variable Declaration")
        variable_name = ctx.IDENTIFIER().getText()
        initialized = True if ctx.getChildCount() > 3 else False
        self.current_variable = VariableType(variable_name, ctx)
        self.current_variable.initialized = initialized
        if initialized:
            self.visitChildren(ctx)
            self.current_variable.set_size()
        
        self.scope_manager.add_symbol(self.current_variable)

    # Visit a parse tree produced by compiscriptParser#primary.
    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        print("INFO -> Entered Primary")
        if ctx.NUMBER():
            self.current_variable.data_type = NumberType()
        elif ctx.STRING():
            self.current_variable.data_type = StringType()
        elif ctx.getText() == "true" or ctx.getText() == "false":
            self.current_variable.data_type = BooleanType()
        elif ctx.getText() == "nil":
            self.current_variable.data_type = NilType()
        else:
            self.current_variable.data_type = DataType()
        