# Generated from compiscript.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,45,307,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,1,0,5,0,60,8,0,10,0,12,0,63,9,0,1,0,1,0,1,1,
        1,1,1,1,1,1,3,1,71,8,1,1,2,1,2,1,2,1,2,3,2,77,8,2,1,2,1,2,5,2,81,
        8,2,10,2,12,2,84,9,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,3,4,95,
        8,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,5,106,8,5,1,6,1,6,1,6,
        1,7,1,7,1,7,1,7,1,7,3,7,116,8,7,1,7,3,7,119,8,7,1,7,1,7,3,7,123,
        8,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,135,8,8,1,9,1,9,
        1,9,1,9,1,10,1,10,3,10,143,8,10,1,10,1,10,1,11,1,11,1,11,1,11,1,
        11,1,11,1,12,1,12,5,12,155,8,12,10,12,12,12,158,9,12,1,12,1,12,1,
        13,1,13,1,13,3,13,165,8,13,1,13,1,13,1,13,1,14,1,14,3,14,172,8,14,
        1,15,1,15,1,15,3,15,177,8,15,1,15,1,15,1,15,1,15,3,15,183,8,15,1,
        16,1,16,1,16,5,16,188,8,16,10,16,12,16,191,9,16,1,17,1,17,1,17,5,
        17,196,8,17,10,17,12,17,199,9,17,1,18,1,18,1,18,5,18,204,8,18,10,
        18,12,18,207,9,18,1,19,1,19,1,19,5,19,212,8,19,10,19,12,19,215,9,
        19,1,20,1,20,1,20,5,20,220,8,20,10,20,12,20,223,9,20,1,21,1,21,1,
        21,5,21,228,8,21,10,21,12,21,231,9,21,1,22,1,22,1,22,1,22,3,22,237,
        8,22,1,22,1,22,1,23,1,23,1,23,3,23,244,8,23,1,24,1,24,1,24,3,24,
        249,8,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,5,24,258,8,24,10,24,
        12,24,261,9,24,1,24,3,24,264,8,24,1,25,1,25,1,25,1,25,1,25,1,25,
        1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,3,25,281,8,25,1,26,
        1,26,1,26,3,26,286,8,26,1,26,1,26,1,26,1,27,1,27,1,27,5,27,294,8,
        27,10,27,12,27,297,9,27,1,28,1,28,1,28,5,28,302,8,28,10,28,12,28,
        305,9,28,1,28,0,0,29,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,
        32,34,36,38,40,42,44,46,48,50,52,54,56,0,5,1,0,20,21,1,0,22,25,1,
        0,26,27,1,0,28,30,2,0,26,26,32,32,326,0,61,1,0,0,0,2,70,1,0,0,0,
        4,72,1,0,0,0,6,87,1,0,0,0,8,90,1,0,0,0,10,105,1,0,0,0,12,107,1,0,
        0,0,14,110,1,0,0,0,16,127,1,0,0,0,18,136,1,0,0,0,20,140,1,0,0,0,
        22,146,1,0,0,0,24,152,1,0,0,0,26,161,1,0,0,0,28,171,1,0,0,0,30,182,
        1,0,0,0,32,184,1,0,0,0,34,192,1,0,0,0,36,200,1,0,0,0,38,208,1,0,
        0,0,40,216,1,0,0,0,42,224,1,0,0,0,44,232,1,0,0,0,46,243,1,0,0,0,
        48,263,1,0,0,0,50,280,1,0,0,0,52,282,1,0,0,0,54,290,1,0,0,0,56,298,
        1,0,0,0,58,60,3,2,1,0,59,58,1,0,0,0,60,63,1,0,0,0,61,59,1,0,0,0,
        61,62,1,0,0,0,62,64,1,0,0,0,63,61,1,0,0,0,64,65,5,0,0,1,65,1,1,0,
        0,0,66,71,3,4,2,0,67,71,3,6,3,0,68,71,3,8,4,0,69,71,3,10,5,0,70,
        66,1,0,0,0,70,67,1,0,0,0,70,68,1,0,0,0,70,69,1,0,0,0,71,3,1,0,0,
        0,72,73,5,1,0,0,73,76,5,43,0,0,74,75,5,2,0,0,75,77,5,43,0,0,76,74,
        1,0,0,0,76,77,1,0,0,0,77,78,1,0,0,0,78,82,5,3,0,0,79,81,3,52,26,
        0,80,79,1,0,0,0,81,84,1,0,0,0,82,80,1,0,0,0,82,83,1,0,0,0,83,85,
        1,0,0,0,84,82,1,0,0,0,85,86,5,4,0,0,86,5,1,0,0,0,87,88,5,5,0,0,88,
        89,3,52,26,0,89,7,1,0,0,0,90,91,5,6,0,0,91,94,5,43,0,0,92,93,5,7,
        0,0,93,95,3,28,14,0,94,92,1,0,0,0,94,95,1,0,0,0,95,96,1,0,0,0,96,
        97,5,8,0,0,97,9,1,0,0,0,98,106,3,12,6,0,99,106,3,14,7,0,100,106,
        3,16,8,0,101,106,3,18,9,0,102,106,3,20,10,0,103,106,3,22,11,0,104,
        106,3,24,12,0,105,98,1,0,0,0,105,99,1,0,0,0,105,100,1,0,0,0,105,
        101,1,0,0,0,105,102,1,0,0,0,105,103,1,0,0,0,105,104,1,0,0,0,106,
        11,1,0,0,0,107,108,3,28,14,0,108,109,5,8,0,0,109,13,1,0,0,0,110,
        111,5,9,0,0,111,115,5,10,0,0,112,116,3,8,4,0,113,116,3,12,6,0,114,
        116,5,8,0,0,115,112,1,0,0,0,115,113,1,0,0,0,115,114,1,0,0,0,116,
        118,1,0,0,0,117,119,3,28,14,0,118,117,1,0,0,0,118,119,1,0,0,0,119,
        120,1,0,0,0,120,122,5,8,0,0,121,123,3,28,14,0,122,121,1,0,0,0,122,
        123,1,0,0,0,123,124,1,0,0,0,124,125,5,11,0,0,125,126,3,10,5,0,126,
        15,1,0,0,0,127,128,5,12,0,0,128,129,5,10,0,0,129,130,3,28,14,0,130,
        131,5,11,0,0,131,134,3,10,5,0,132,133,5,13,0,0,133,135,3,10,5,0,
        134,132,1,0,0,0,134,135,1,0,0,0,135,17,1,0,0,0,136,137,5,14,0,0,
        137,138,3,28,14,0,138,139,5,8,0,0,139,19,1,0,0,0,140,142,5,15,0,
        0,141,143,3,28,14,0,142,141,1,0,0,0,142,143,1,0,0,0,143,144,1,0,
        0,0,144,145,5,8,0,0,145,21,1,0,0,0,146,147,5,16,0,0,147,148,5,10,
        0,0,148,149,3,28,14,0,149,150,5,11,0,0,150,151,3,10,5,0,151,23,1,
        0,0,0,152,156,5,3,0,0,153,155,3,2,1,0,154,153,1,0,0,0,155,158,1,
        0,0,0,156,154,1,0,0,0,156,157,1,0,0,0,157,159,1,0,0,0,158,156,1,
        0,0,0,159,160,5,4,0,0,160,25,1,0,0,0,161,162,5,5,0,0,162,164,5,10,
        0,0,163,165,3,54,27,0,164,163,1,0,0,0,164,165,1,0,0,0,165,166,1,
        0,0,0,166,167,5,11,0,0,167,168,3,24,12,0,168,27,1,0,0,0,169,172,
        3,30,15,0,170,172,3,26,13,0,171,169,1,0,0,0,171,170,1,0,0,0,172,
        29,1,0,0,0,173,174,3,48,24,0,174,175,5,17,0,0,175,177,1,0,0,0,176,
        173,1,0,0,0,176,177,1,0,0,0,177,178,1,0,0,0,178,179,5,43,0,0,179,
        180,5,7,0,0,180,183,3,30,15,0,181,183,3,32,16,0,182,176,1,0,0,0,
        182,181,1,0,0,0,183,31,1,0,0,0,184,189,3,34,17,0,185,186,5,18,0,
        0,186,188,3,34,17,0,187,185,1,0,0,0,188,191,1,0,0,0,189,187,1,0,
        0,0,189,190,1,0,0,0,190,33,1,0,0,0,191,189,1,0,0,0,192,197,3,36,
        18,0,193,194,5,19,0,0,194,196,3,36,18,0,195,193,1,0,0,0,196,199,
        1,0,0,0,197,195,1,0,0,0,197,198,1,0,0,0,198,35,1,0,0,0,199,197,1,
        0,0,0,200,205,3,38,19,0,201,202,7,0,0,0,202,204,3,38,19,0,203,201,
        1,0,0,0,204,207,1,0,0,0,205,203,1,0,0,0,205,206,1,0,0,0,206,37,1,
        0,0,0,207,205,1,0,0,0,208,213,3,40,20,0,209,210,7,1,0,0,210,212,
        3,40,20,0,211,209,1,0,0,0,212,215,1,0,0,0,213,211,1,0,0,0,213,214,
        1,0,0,0,214,39,1,0,0,0,215,213,1,0,0,0,216,221,3,42,21,0,217,218,
        7,2,0,0,218,220,3,42,21,0,219,217,1,0,0,0,220,223,1,0,0,0,221,219,
        1,0,0,0,221,222,1,0,0,0,222,41,1,0,0,0,223,221,1,0,0,0,224,229,3,
        46,23,0,225,226,7,3,0,0,226,228,3,46,23,0,227,225,1,0,0,0,228,231,
        1,0,0,0,229,227,1,0,0,0,229,230,1,0,0,0,230,43,1,0,0,0,231,229,1,
        0,0,0,232,233,5,31,0,0,233,234,5,43,0,0,234,236,5,10,0,0,235,237,
        3,56,28,0,236,235,1,0,0,0,236,237,1,0,0,0,237,238,1,0,0,0,238,239,
        5,11,0,0,239,45,1,0,0,0,240,241,7,4,0,0,241,244,3,46,23,0,242,244,
        3,48,24,0,243,240,1,0,0,0,243,242,1,0,0,0,244,47,1,0,0,0,245,259,
        3,50,25,0,246,248,5,10,0,0,247,249,3,56,28,0,248,247,1,0,0,0,248,
        249,1,0,0,0,249,250,1,0,0,0,250,258,5,11,0,0,251,252,5,17,0,0,252,
        258,5,43,0,0,253,254,5,33,0,0,254,255,3,28,14,0,255,256,5,34,0,0,
        256,258,1,0,0,0,257,246,1,0,0,0,257,251,1,0,0,0,257,253,1,0,0,0,
        258,261,1,0,0,0,259,257,1,0,0,0,259,260,1,0,0,0,260,264,1,0,0,0,
        261,259,1,0,0,0,262,264,3,26,13,0,263,245,1,0,0,0,263,262,1,0,0,
        0,264,49,1,0,0,0,265,281,5,35,0,0,266,281,5,36,0,0,267,281,5,37,
        0,0,268,281,5,38,0,0,269,281,5,41,0,0,270,281,5,42,0,0,271,281,5,
        43,0,0,272,273,5,10,0,0,273,274,3,28,14,0,274,275,5,11,0,0,275,281,
        1,0,0,0,276,277,5,39,0,0,277,278,5,17,0,0,278,281,5,43,0,0,279,281,
        3,44,22,0,280,265,1,0,0,0,280,266,1,0,0,0,280,267,1,0,0,0,280,268,
        1,0,0,0,280,269,1,0,0,0,280,270,1,0,0,0,280,271,1,0,0,0,280,272,
        1,0,0,0,280,276,1,0,0,0,280,279,1,0,0,0,281,51,1,0,0,0,282,283,5,
        43,0,0,283,285,5,10,0,0,284,286,3,54,27,0,285,284,1,0,0,0,285,286,
        1,0,0,0,286,287,1,0,0,0,287,288,5,11,0,0,288,289,3,24,12,0,289,53,
        1,0,0,0,290,295,5,43,0,0,291,292,5,40,0,0,292,294,5,43,0,0,293,291,
        1,0,0,0,294,297,1,0,0,0,295,293,1,0,0,0,295,296,1,0,0,0,296,55,1,
        0,0,0,297,295,1,0,0,0,298,303,3,28,14,0,299,300,5,40,0,0,300,302,
        3,28,14,0,301,299,1,0,0,0,302,305,1,0,0,0,303,301,1,0,0,0,303,304,
        1,0,0,0,304,57,1,0,0,0,305,303,1,0,0,0,32,61,70,76,82,94,105,115,
        118,122,134,142,156,164,171,176,182,189,197,205,213,221,229,236,
        243,248,257,259,263,280,285,295,303
    ]

class compiscriptParser ( Parser ):

    grammarFileName = "compiscript.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'class'", "'extends'", "'{'", "'}'", 
                     "'fun'", "'var'", "'='", "';'", "'for'", "'('", "')'", 
                     "'if'", "'else'", "'print'", "'return'", "'while'", 
                     "'.'", "'or'", "'and'", "'!='", "'=='", "'>'", "'>='", 
                     "'<'", "'<='", "'-'", "'+'", "'/'", "'*'", "'%'", "'new'", 
                     "'!'", "'['", "']'", "'true'", "'false'", "'nil'", 
                     "'this'", "'super'", "','" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "NUMBER", "STRING", "IDENTIFIER", "WS", 
                      "ONE_LINE_COMMENT" ]

    RULE_program = 0
    RULE_declaration = 1
    RULE_classDecl = 2
    RULE_funDecl = 3
    RULE_varDecl = 4
    RULE_statement = 5
    RULE_exprStmt = 6
    RULE_forStmt = 7
    RULE_ifStmt = 8
    RULE_printStmt = 9
    RULE_returnStmt = 10
    RULE_whileStmt = 11
    RULE_block = 12
    RULE_funAnon = 13
    RULE_expression = 14
    RULE_assignment = 15
    RULE_logic_or = 16
    RULE_logic_and = 17
    RULE_equality = 18
    RULE_comparison = 19
    RULE_term = 20
    RULE_factor = 21
    RULE_instantiation = 22
    RULE_unary = 23
    RULE_call = 24
    RULE_primary = 25
    RULE_function = 26
    RULE_parameters = 27
    RULE_arguments = 28

    ruleNames =  [ "program", "declaration", "classDecl", "funDecl", "varDecl", 
                   "statement", "exprStmt", "forStmt", "ifStmt", "printStmt", 
                   "returnStmt", "whileStmt", "block", "funAnon", "expression", 
                   "assignment", "logic_or", "logic_and", "equality", "comparison", 
                   "term", "factor", "instantiation", "unary", "call", "primary", 
                   "function", "parameters", "arguments" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    NUMBER=41
    STRING=42
    IDENTIFIER=43
    WS=44
    ONE_LINE_COMMENT=45

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(compiscriptParser.EOF, 0)

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.DeclarationContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = compiscriptParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 16464824358506) != 0):
                self.state = 58
                self.declaration()
                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 64
            self.match(compiscriptParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classDecl(self):
            return self.getTypedRuleContext(compiscriptParser.ClassDeclContext,0)


        def funDecl(self):
            return self.getTypedRuleContext(compiscriptParser.FunDeclContext,0)


        def varDecl(self):
            return self.getTypedRuleContext(compiscriptParser.VarDeclContext,0)


        def statement(self):
            return self.getTypedRuleContext(compiscriptParser.StatementContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_declaration

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = compiscriptParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declaration)
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.classDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 67
                self.funDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 68
                self.varDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 69
                self.statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(compiscriptParser.IDENTIFIER)
            else:
                return self.getToken(compiscriptParser.IDENTIFIER, i)

        def function(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.FunctionContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.FunctionContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_classDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassDecl" ):
                return visitor.visitClassDecl(self)
            else:
                return visitor.visitChildren(self)




    def classDecl(self):

        localctx = compiscriptParser.ClassDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_classDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(compiscriptParser.T__0)
            self.state = 73
            self.match(compiscriptParser.IDENTIFIER)
            self.state = 76
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 74
                self.match(compiscriptParser.T__1)
                self.state = 75
                self.match(compiscriptParser.IDENTIFIER)


            self.state = 78
            self.match(compiscriptParser.T__2)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==43:
                self.state = 79
                self.function()
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 85
            self.match(compiscriptParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def function(self):
            return self.getTypedRuleContext(compiscriptParser.FunctionContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_funDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunDecl" ):
                return visitor.visitFunDecl(self)
            else:
                return visitor.visitChildren(self)




    def funDecl(self):

        localctx = compiscriptParser.FunDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_funDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.match(compiscriptParser.T__4)
            self.state = 88
            self.function()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(compiscriptParser.IDENTIFIER, 0)

        def expression(self):
            return self.getTypedRuleContext(compiscriptParser.ExpressionContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_varDecl

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarDecl" ):
                return visitor.visitVarDecl(self)
            else:
                return visitor.visitChildren(self)




    def varDecl(self):

        localctx = compiscriptParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_varDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(compiscriptParser.T__5)
            self.state = 91
            self.match(compiscriptParser.IDENTIFIER)
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 92
                self.match(compiscriptParser.T__6)
                self.state = 93
                self.expression()


            self.state = 96
            self.match(compiscriptParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprStmt(self):
            return self.getTypedRuleContext(compiscriptParser.ExprStmtContext,0)


        def forStmt(self):
            return self.getTypedRuleContext(compiscriptParser.ForStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(compiscriptParser.IfStmtContext,0)


        def printStmt(self):
            return self.getTypedRuleContext(compiscriptParser.PrintStmtContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(compiscriptParser.ReturnStmtContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(compiscriptParser.WhileStmtContext,0)


        def block(self):
            return self.getTypedRuleContext(compiscriptParser.BlockContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = compiscriptParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_statement)
        try:
            self.state = 105
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5, 10, 26, 31, 32, 35, 36, 37, 38, 39, 41, 42, 43]:
                self.enterOuterAlt(localctx, 1)
                self.state = 98
                self.exprStmt()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 99
                self.forStmt()
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 3)
                self.state = 100
                self.ifStmt()
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 4)
                self.state = 101
                self.printStmt()
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 5)
                self.state = 102
                self.returnStmt()
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 6)
                self.state = 103
                self.whileStmt()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 7)
                self.state = 104
                self.block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(compiscriptParser.ExpressionContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_exprStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStmt" ):
                return visitor.visitExprStmt(self)
            else:
                return visitor.visitChildren(self)




    def exprStmt(self):

        localctx = compiscriptParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_exprStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.expression()
            self.state = 108
            self.match(compiscriptParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self):
            return self.getTypedRuleContext(compiscriptParser.StatementContext,0)


        def varDecl(self):
            return self.getTypedRuleContext(compiscriptParser.VarDeclContext,0)


        def exprStmt(self):
            return self.getTypedRuleContext(compiscriptParser.ExprStmtContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.ExpressionContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_forStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStmt" ):
                return visitor.visitForStmt(self)
            else:
                return visitor.visitChildren(self)




    def forStmt(self):

        localctx = compiscriptParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_forStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self.match(compiscriptParser.T__8)
            self.state = 111
            self.match(compiscriptParser.T__9)
            self.state = 115
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.state = 112
                self.varDecl()
                pass
            elif token in [5, 10, 26, 31, 32, 35, 36, 37, 38, 39, 41, 42, 43]:
                self.state = 113
                self.exprStmt()
                pass
            elif token in [8]:
                self.state = 114
                self.match(compiscriptParser.T__7)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16464824239136) != 0):
                self.state = 117
                self.expression()


            self.state = 120
            self.match(compiscriptParser.T__7)
            self.state = 122
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16464824239136) != 0):
                self.state = 121
                self.expression()


            self.state = 124
            self.match(compiscriptParser.T__10)
            self.state = 125
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(compiscriptParser.ExpressionContext,0)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.StatementContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.StatementContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = compiscriptParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_ifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(compiscriptParser.T__11)
            self.state = 128
            self.match(compiscriptParser.T__9)
            self.state = 129
            self.expression()
            self.state = 130
            self.match(compiscriptParser.T__10)
            self.state = 131
            self.statement()
            self.state = 134
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 132
                self.match(compiscriptParser.T__12)
                self.state = 133
                self.statement()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(compiscriptParser.ExpressionContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_printStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrintStmt" ):
                return visitor.visitPrintStmt(self)
            else:
                return visitor.visitChildren(self)




    def printStmt(self):

        localctx = compiscriptParser.PrintStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_printStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.match(compiscriptParser.T__13)
            self.state = 137
            self.expression()
            self.state = 138
            self.match(compiscriptParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(compiscriptParser.ExpressionContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_returnStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = compiscriptParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_returnStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.match(compiscriptParser.T__14)
            self.state = 142
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16464824239136) != 0):
                self.state = 141
                self.expression()


            self.state = 144
            self.match(compiscriptParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(compiscriptParser.ExpressionContext,0)


        def statement(self):
            return self.getTypedRuleContext(compiscriptParser.StatementContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_whileStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = compiscriptParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 146
            self.match(compiscriptParser.T__15)
            self.state = 147
            self.match(compiscriptParser.T__9)
            self.state = 148
            self.expression()
            self.state = 149
            self.match(compiscriptParser.T__10)
            self.state = 150
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.DeclarationContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_block

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = compiscriptParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.match(compiscriptParser.T__2)
            self.state = 156
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 16464824358506) != 0):
                self.state = 153
                self.declaration()
                self.state = 158
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 159
            self.match(compiscriptParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunAnonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block(self):
            return self.getTypedRuleContext(compiscriptParser.BlockContext,0)


        def parameters(self):
            return self.getTypedRuleContext(compiscriptParser.ParametersContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_funAnon

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunAnon" ):
                return visitor.visitFunAnon(self)
            else:
                return visitor.visitChildren(self)




    def funAnon(self):

        localctx = compiscriptParser.FunAnonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_funAnon)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.match(compiscriptParser.T__4)
            self.state = 162
            self.match(compiscriptParser.T__9)
            self.state = 164
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==43:
                self.state = 163
                self.parameters()


            self.state = 166
            self.match(compiscriptParser.T__10)
            self.state = 167
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(compiscriptParser.AssignmentContext,0)


        def funAnon(self):
            return self.getTypedRuleContext(compiscriptParser.FunAnonContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = compiscriptParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_expression)
        try:
            self.state = 171
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 170
                self.funAnon()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(compiscriptParser.IDENTIFIER, 0)

        def assignment(self):
            return self.getTypedRuleContext(compiscriptParser.AssignmentContext,0)


        def call(self):
            return self.getTypedRuleContext(compiscriptParser.CallContext,0)


        def logic_or(self):
            return self.getTypedRuleContext(compiscriptParser.Logic_orContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_assignment

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = compiscriptParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_assignment)
        try:
            self.state = 182
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 176
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
                if la_ == 1:
                    self.state = 173
                    self.call()
                    self.state = 174
                    self.match(compiscriptParser.T__16)


                self.state = 178
                self.match(compiscriptParser.IDENTIFIER)
                self.state = 179
                self.match(compiscriptParser.T__6)
                self.state = 180
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 181
                self.logic_or()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Logic_orContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logic_and(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.Logic_andContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.Logic_andContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_logic_or

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogic_or" ):
                return visitor.visitLogic_or(self)
            else:
                return visitor.visitChildren(self)




    def logic_or(self):

        localctx = compiscriptParser.Logic_orContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_logic_or)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 184
            self.logic_and()
            self.state = 189
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==18:
                self.state = 185
                self.match(compiscriptParser.T__17)
                self.state = 186
                self.logic_and()
                self.state = 191
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Logic_andContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def equality(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.EqualityContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.EqualityContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_logic_and

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogic_and" ):
                return visitor.visitLogic_and(self)
            else:
                return visitor.visitChildren(self)




    def logic_and(self):

        localctx = compiscriptParser.Logic_andContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_logic_and)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.equality()
            self.state = 197
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 193
                self.match(compiscriptParser.T__18)
                self.state = 194
                self.equality()
                self.state = 199
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EqualityContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comparison(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.ComparisonContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.ComparisonContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_equality

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEquality" ):
                return visitor.visitEquality(self)
            else:
                return visitor.visitChildren(self)




    def equality(self):

        localctx = compiscriptParser.EqualityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_equality)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self.comparison()
            self.state = 205
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==20 or _la==21:
                self.state = 201
                _la = self._input.LA(1)
                if not(_la==20 or _la==21):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 202
                self.comparison()
                self.state = 207
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.TermContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.TermContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_comparison

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = compiscriptParser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 208
            self.term()
            self.state = 213
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 62914560) != 0):
                self.state = 209
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 62914560) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 210
                self.term()
                self.state = 215
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.FactorContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.FactorContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = compiscriptParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 216
            self.factor()
            self.state = 221
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26 or _la==27:
                self.state = 217
                _la = self._input.LA(1)
                if not(_la==26 or _la==27):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 218
                self.factor()
                self.state = 223
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unary(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.UnaryContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.UnaryContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_factor

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactor" ):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = compiscriptParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 224
            self.unary()
            self.state = 229
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1879048192) != 0):
                self.state = 225
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1879048192) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 226
                self.unary()
                self.state = 231
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InstantiationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(compiscriptParser.IDENTIFIER, 0)

        def arguments(self):
            return self.getTypedRuleContext(compiscriptParser.ArgumentsContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_instantiation

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInstantiation" ):
                return visitor.visitInstantiation(self)
            else:
                return visitor.visitChildren(self)




    def instantiation(self):

        localctx = compiscriptParser.InstantiationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_instantiation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self.match(compiscriptParser.T__30)
            self.state = 233
            self.match(compiscriptParser.IDENTIFIER)
            self.state = 234
            self.match(compiscriptParser.T__9)
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16464824239136) != 0):
                self.state = 235
                self.arguments()


            self.state = 238
            self.match(compiscriptParser.T__10)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unary(self):
            return self.getTypedRuleContext(compiscriptParser.UnaryContext,0)


        def call(self):
            return self.getTypedRuleContext(compiscriptParser.CallContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_unary

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary" ):
                return visitor.visitUnary(self)
            else:
                return visitor.visitChildren(self)




    def unary(self):

        localctx = compiscriptParser.UnaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_unary)
        self._la = 0 # Token type
        try:
            self.state = 243
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [26, 32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 240
                _la = self._input.LA(1)
                if not(_la==26 or _la==32):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 241
                self.unary()
                pass
            elif token in [5, 10, 31, 35, 36, 37, 38, 39, 41, 42, 43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 242
                self.call()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self):
            return self.getTypedRuleContext(compiscriptParser.PrimaryContext,0)


        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(compiscriptParser.IDENTIFIER)
            else:
                return self.getToken(compiscriptParser.IDENTIFIER, i)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.ExpressionContext,i)


        def arguments(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.ArgumentsContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.ArgumentsContext,i)


        def funAnon(self):
            return self.getTypedRuleContext(compiscriptParser.FunAnonContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_call

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)




    def call(self):

        localctx = compiscriptParser.CallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_call)
        self._la = 0 # Token type
        try:
            self.state = 263
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10, 31, 35, 36, 37, 38, 39, 41, 42, 43]:
                self.enterOuterAlt(localctx, 1)
                self.state = 245
                self.primary()
                self.state = 259
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,26,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 257
                        self._errHandler.sync(self)
                        token = self._input.LA(1)
                        if token in [10]:
                            self.state = 246
                            self.match(compiscriptParser.T__9)
                            self.state = 248
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16464824239136) != 0):
                                self.state = 247
                                self.arguments()


                            self.state = 250
                            self.match(compiscriptParser.T__10)
                            pass
                        elif token in [17]:
                            self.state = 251
                            self.match(compiscriptParser.T__16)
                            self.state = 252
                            self.match(compiscriptParser.IDENTIFIER)
                            pass
                        elif token in [33]:
                            self.state = 253
                            self.match(compiscriptParser.T__32)
                            self.state = 254
                            self.expression()
                            self.state = 255
                            self.match(compiscriptParser.T__33)
                            pass
                        else:
                            raise NoViableAltException(self)
                 
                    self.state = 261
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,26,self._ctx)

                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 262
                self.funAnon()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(compiscriptParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(compiscriptParser.STRING, 0)

        def IDENTIFIER(self):
            return self.getToken(compiscriptParser.IDENTIFIER, 0)

        def expression(self):
            return self.getTypedRuleContext(compiscriptParser.ExpressionContext,0)


        def instantiation(self):
            return self.getTypedRuleContext(compiscriptParser.InstantiationContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_primary

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimary" ):
                return visitor.visitPrimary(self)
            else:
                return visitor.visitChildren(self)




    def primary(self):

        localctx = compiscriptParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_primary)
        try:
            self.state = 280
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [35]:
                self.enterOuterAlt(localctx, 1)
                self.state = 265
                self.match(compiscriptParser.T__34)
                pass
            elif token in [36]:
                self.enterOuterAlt(localctx, 2)
                self.state = 266
                self.match(compiscriptParser.T__35)
                pass
            elif token in [37]:
                self.enterOuterAlt(localctx, 3)
                self.state = 267
                self.match(compiscriptParser.T__36)
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 4)
                self.state = 268
                self.match(compiscriptParser.T__37)
                pass
            elif token in [41]:
                self.enterOuterAlt(localctx, 5)
                self.state = 269
                self.match(compiscriptParser.NUMBER)
                pass
            elif token in [42]:
                self.enterOuterAlt(localctx, 6)
                self.state = 270
                self.match(compiscriptParser.STRING)
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 7)
                self.state = 271
                self.match(compiscriptParser.IDENTIFIER)
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 8)
                self.state = 272
                self.match(compiscriptParser.T__9)
                self.state = 273
                self.expression()
                self.state = 274
                self.match(compiscriptParser.T__10)
                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 9)
                self.state = 276
                self.match(compiscriptParser.T__38)
                self.state = 277
                self.match(compiscriptParser.T__16)
                self.state = 278
                self.match(compiscriptParser.IDENTIFIER)
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 10)
                self.state = 279
                self.instantiation()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(compiscriptParser.IDENTIFIER, 0)

        def block(self):
            return self.getTypedRuleContext(compiscriptParser.BlockContext,0)


        def parameters(self):
            return self.getTypedRuleContext(compiscriptParser.ParametersContext,0)


        def getRuleIndex(self):
            return compiscriptParser.RULE_function

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)




    def function(self):

        localctx = compiscriptParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_function)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 282
            self.match(compiscriptParser.IDENTIFIER)
            self.state = 283
            self.match(compiscriptParser.T__9)
            self.state = 285
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==43:
                self.state = 284
                self.parameters()


            self.state = 287
            self.match(compiscriptParser.T__10)
            self.state = 288
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParametersContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self, i:int=None):
            if i is None:
                return self.getTokens(compiscriptParser.IDENTIFIER)
            else:
                return self.getToken(compiscriptParser.IDENTIFIER, i)

        def getRuleIndex(self):
            return compiscriptParser.RULE_parameters

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameters" ):
                return visitor.visitParameters(self)
            else:
                return visitor.visitChildren(self)




    def parameters(self):

        localctx = compiscriptParser.ParametersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_parameters)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 290
            self.match(compiscriptParser.IDENTIFIER)
            self.state = 295
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 291
                self.match(compiscriptParser.T__39)
                self.state = 292
                self.match(compiscriptParser.IDENTIFIER)
                self.state = 297
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(compiscriptParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(compiscriptParser.ExpressionContext,i)


        def getRuleIndex(self):
            return compiscriptParser.RULE_arguments

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArguments" ):
                return visitor.visitArguments(self)
            else:
                return visitor.visitChildren(self)




    def arguments(self):

        localctx = compiscriptParser.ArgumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_arguments)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 298
            self.expression()
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==40:
                self.state = 299
                self.match(compiscriptParser.T__39)
                self.state = 300
                self.expression()
                self.state = 305
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





