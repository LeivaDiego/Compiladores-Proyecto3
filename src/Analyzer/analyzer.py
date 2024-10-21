from CompiScript.compiscriptVisitor import compiscriptVisitor
from CompiScript.compiscriptParser import compiscriptParser
from Analyzer.objetc_types import ObjectType, VariableType, FunctionType, ClassType
from Analyzer.data_types import DataType, NumberType, StringType, BooleanType, NilType, Uninitialized


class SymbolTableGenerator(compiscriptVisitor):
    def __init__(self):
        self.current_class : ClassType = None
        self.current_function : FunctionType = None
        self.current_variable: VariableType = None

    # Visit a parse tree produced by compiscriptParser#program.
    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        print("INFO -> Entered Program")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#declaration.
    def visitDeclaration(self, ctx:compiscriptParser.DeclarationContext):
        print("INFO -> Entered Declaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#classDecl.
    def visitClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        print("INFO -> Entered Class Declaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#funDecl.
    def visitFunDecl(self, ctx:compiscriptParser.FunDeclContext):
        print("INFO -> Entered Function Declaration")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#varDecl.
    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        print("INFO -> Entered Variable Declaration")
        var_id = ctx.IDENTIFIER().getText()
        print(f"INFO -> Declaring Variable with ID: {var_id}")
        self.current_variable = VariableType(var_id, ctx)
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#statement.
    def visitStatement(self, ctx:compiscriptParser.StatementContext):
        print("INFO -> Entered Statement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#exprStmt.
    def visitExprStmt(self, ctx:compiscriptParser.ExprStmtContext):
        print("INFO -> Entered Expression Statement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#forStmt.
    def visitForStmt(self, ctx:compiscriptParser.ForStmtContext):
        print("INFO -> Entered For Statement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#ifStmt.
    def visitIfStmt(self, ctx:compiscriptParser.IfStmtContext):
        print("INFO -> Entered If Statement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#printStmt.
    def visitPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        print("INFO -> Entered Print Statement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#returnStmt.
    def visitReturnStmt(self, ctx:compiscriptParser.ReturnStmtContext):
        print("INFO -> Entered Return Statement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#whileStmt.
    def visitWhileStmt(self, ctx:compiscriptParser.WhileStmtContext):
        print("INFO -> Entered While Statement")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#block.
    def visitBlock(self, ctx:compiscriptParser.BlockContext):
        print("INFO -> Entered Block")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#funAnon.
    def visitFunAnon(self, ctx:compiscriptParser.FunAnonContext):
        print("INFO -> Entered Anonymous Function")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#expression.
    def visitExpression(self, ctx:compiscriptParser.ExpressionContext):
        print("INFO -> Entered Expression")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#assignment.
    def visitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        print("INFO -> Entered Assignment")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#logic_or.
    def visitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        print("INFO -> Entered Logic Or")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#logic_and.
    def visitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        print("INFO -> Entered Logic And")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#equality.
    def visitEquality(self, ctx:compiscriptParser.EqualityContext):
        print("INFO -> Entered Equality")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#comparison.
    def visitComparison(self, ctx:compiscriptParser.ComparisonContext):
        print("INFO -> Entered Comparison")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#term.
    def visitTerm(self, ctx:compiscriptParser.TermContext):
        print("INFO -> Entered Term")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#factor.
    def visitFactor(self, ctx:compiscriptParser.FactorContext):
        print("INFO -> Entered Factor")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#instantiation.
    def visitInstantiation(self, ctx:compiscriptParser.InstantiationContext):
        print("INFO -> Entered Instantiation")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#unary.
    def visitUnary(self, ctx:compiscriptParser.UnaryContext):
        print("INFO -> Entered Unary")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#call.
    def visitCall(self, ctx:compiscriptParser.CallContext):
        print("INFO -> Entered Call")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#primary.
    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        print("INFO -> Entered Primary")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#function.
    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        print("INFO -> Entered Function")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#parameters.
    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        print("INFO -> Entered Parameters")
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#arguments.
    def visitArguments(self, ctx:compiscriptParser.ArgumentsContext):
        print("INFO -> Entered Arguments")
        return self.visitChildren(ctx)
