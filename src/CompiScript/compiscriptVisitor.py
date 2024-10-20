# Generated from compiscript.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .compiscriptParser import compiscriptParser
else:
    from compiscriptParser import compiscriptParser

# This class defines a complete generic visitor for a parse tree produced by compiscriptParser.

class compiscriptVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by compiscriptParser#program.
    def visitProgram(self, ctx:compiscriptParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#declaration.
    def visitDeclaration(self, ctx:compiscriptParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#classDecl.
    def visitClassDecl(self, ctx:compiscriptParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#funDecl.
    def visitFunDecl(self, ctx:compiscriptParser.FunDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#varDecl.
    def visitVarDecl(self, ctx:compiscriptParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#statement.
    def visitStatement(self, ctx:compiscriptParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#exprStmt.
    def visitExprStmt(self, ctx:compiscriptParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#forStmt.
    def visitForStmt(self, ctx:compiscriptParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#ifStmt.
    def visitIfStmt(self, ctx:compiscriptParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#printStmt.
    def visitPrintStmt(self, ctx:compiscriptParser.PrintStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#returnStmt.
    def visitReturnStmt(self, ctx:compiscriptParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#whileStmt.
    def visitWhileStmt(self, ctx:compiscriptParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#block.
    def visitBlock(self, ctx:compiscriptParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#funAnon.
    def visitFunAnon(self, ctx:compiscriptParser.FunAnonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#expression.
    def visitExpression(self, ctx:compiscriptParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#assignment.
    def visitAssignment(self, ctx:compiscriptParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#logic_or.
    def visitLogic_or(self, ctx:compiscriptParser.Logic_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#logic_and.
    def visitLogic_and(self, ctx:compiscriptParser.Logic_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#equality.
    def visitEquality(self, ctx:compiscriptParser.EqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#comparison.
    def visitComparison(self, ctx:compiscriptParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#term.
    def visitTerm(self, ctx:compiscriptParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#factor.
    def visitFactor(self, ctx:compiscriptParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#instantiation.
    def visitInstantiation(self, ctx:compiscriptParser.InstantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#unary.
    def visitUnary(self, ctx:compiscriptParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#call.
    def visitCall(self, ctx:compiscriptParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#primary.
    def visitPrimary(self, ctx:compiscriptParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#function.
    def visitFunction(self, ctx:compiscriptParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#parameters.
    def visitParameters(self, ctx:compiscriptParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiscriptParser#arguments.
    def visitArguments(self, ctx:compiscriptParser.ArgumentsContext):
        return self.visitChildren(ctx)



del compiscriptParser