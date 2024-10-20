from CompiScript.compiscriptLexer import compiscriptLexer
from CompiScript.compiscriptParser import compiscriptParser
from antlr4 import FileStream, CommonTokenStream
from ParseTree.parse_tree import TreeVisualizer


def main():
    # Get the input file and create a file stream
    input_file = 'src/Input/test.cspt'
    input_stream = FileStream(input_file)

    # Create the lexer and use a custom error listener
    lexer = compiscriptLexer(input_stream)

    # Create a token stream from the lexer
    token_stream = CommonTokenStream(lexer)

    # Create the parser and use a custom error listener
    parser = compiscriptParser(token_stream)

    # Start parsing from the program rule
    parse_tree = parser.program()

    # Create a TreeVisualizer object and visit the parse tree
    tree_visualizer = TreeVisualizer(input_file)
    tree_visualizer.visit(parse_tree)
    tree_visualizer.render(output_file=tree_visualizer.name, 
                           format='png', 
                           output_dir='src/ParseTree/Output')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)