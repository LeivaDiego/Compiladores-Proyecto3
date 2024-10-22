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
        self.scope_manager.enter_scope()
        self.visitChildren(ctx)

    # Visit a parse tree produced by compiscriptParser#varDecl.
    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        print("INFO -> Entered Variable Declaration")
        var_id = ctx.IDENTIFIER().getText()
        print(f"INFO -> Declaring Variable with ID: {var_id}")
        self.current_variable = VariableType(var_id, ctx)
        self.current_variable.set_initialized()
        self.scope_manager.current_scope.add_symbol(self.current_variable)

    # Visit a parse tree produced by compiscriptParser#primary.
    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        print("INFO -> Entered Primary")
        