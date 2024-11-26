from CompiScript.compiscriptLexer import compiscriptLexer
from CompiScript.compiscriptParser import compiscriptParser
from antlr4 import FileStream, CommonTokenStream
from ParseTree.parse_tree import TreeVisualizer
from antlr4.error.ErrorStrategy import DefaultErrorStrategy, ParseCancellationException
from Utils.custom_exception import ThrowingErrorListener
from SemanticAnalyzer.semantic_analyzer import SemanticAnalyzer
from IntermediateCode.ci_generator import IntermediateCodeGenerator


def main():
    # Get the input file and create a file stream
    input_file = 'src/Input/Examples/Ejemplo1.cspt'
    input_stream = FileStream(input_file)

    # Create the lexer and use a custom error listener
    lexer = compiscriptLexer(input_stream)
    lexer.removeErrorListeners()  # Remove the default error listener
    lexer.addErrorListener(ThrowingErrorListener.INSTANCE)  # Add custom error listener

    # Create a token stream from the lexer
    token_stream = CommonTokenStream(lexer)

    # Create the parser and use a custom error listener
    parser = compiscriptParser(token_stream)
    parser._errHandler = DefaultErrorStrategy() # Set Error Strategy to stop parsing on first error
    parser.removeErrorListeners()   # Remove the default error listener
    parser.addErrorListener(ThrowingErrorListener.INSTANCE) # Add custom error listener

    # Start parsing from the program rule
    parse_tree = parser.program()

    # Create a TreeVisualizer object and visit the parse tree
    # tree_visualizer = TreeVisualizer(input_file)
    # tree_visualizer.visit(parse_tree)
    # tree_visualizer.render(output_file=tree_visualizer.name, 
    #                        format='png',
    #                        output_dir='src/ParseTree/Output')
    
    # Create a semantic analyzer and visit the parse tree
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(parse_tree)
    semantic_analyzer.display_table()

    # Create a CI Generator and visit the parse tree
    ci_generator = IntermediateCodeGenerator(semantic_analyzer.symbol_table)
    ci_generator.visit(parse_tree)
    ci_generator.generate_intermediate_code()

if __name__ == '__main__':
    # try:
        main()
    # except ParseCancellationException as e:
    #     print(e)
    # except Exception as e:
    #     print(f"ERROR -> {e}")