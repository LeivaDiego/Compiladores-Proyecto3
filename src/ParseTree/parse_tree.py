from graphviz import Digraph
from antlr4 import ParserRuleContext
import os

class TreeVisualizer:
    """
    Class to visualize the parse tree generated by ANTLR4.

    Attributes:
        - graph: Digraph object from the graphviz library.
        - node_count: Integer to keep track of the number of nodes in the graph.

    Methods:
        - add_node: Adds a node to the graph.
        - add_edge: Adds an edge between two nodes.
        - visit: Visits a node in the parse tree and adds it to the graph.
        - render: Renders the graph to a file in the specified format and directory.
    """
    def __init__(self, file_path):
        print("Generating Parse Tree...")
        self.graph = Digraph(comment='Parse Tree')
        self.node_count = 0
        self.name = self.generate_name(file_path)

    def add_node(self, label):
        """
        Adds a node to the graph with the specified label.

        Args:
            - label: The label of the node.

        Returns:
            - The name of the node.
        """
        # Generate a unique node name
        node_name = f"node{self.node_count}"
        # Add the node to the graph
        self.graph.node(node_name, label)
        # Increment the node count
        self.node_count += 1

        return node_name


    def add_edge(self, parent, child):
        """
        Adds an edge between two nodes in the graph.

        Args:
            - parent: The name of the parent node.
            - child: The name of the child node.

        Returns:
            - None
        """
        self.graph.edge(parent, child)


    def visit(self, ctx: ParserRuleContext, parent=None):
        """
        Visits a node in the parse tree and adds it to the graph.

        Args:
            - ctx: The context node to visit.
            - parent: The parent node of the current context node.

        Returns:
            - The name of the current node.
        """        
        # Determine the label for the current node
        if ctx.getChildCount() == 0:  # Terminal node
            label = ctx.getText()
        else:  # Non-terminal node (rule)
            label = type(ctx).__name__.replace("Context", "")
        
        # Add the current node
        current_node = self.add_node(label)

        # If there is a parent, create an edge
        if parent:
            self.add_edge(parent, current_node)
        
        # Visit all children
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i), current_node)

        return current_node


    def render(self, output_file='parse_tree', format='png', output_dir='.', cleanup=True):
        """
        Renders the graph to a file in the specified format and directory.

        Args:
            - output_file: The name of the output file.
            - format: The format of the output file (e.g., 'png', 'pdf', 'svg').
            - output_dir: The directory where the output file will be saved.
            - cleanup: Whether to clean up the graph after rendering.

        Returns:
            - None
        """
        # Define the full output path
        output_path = f"{output_dir}/{output_file}"

        # Render the graph to the specified format and path
        self.graph.render(filename=output_path, format=format, cleanup=cleanup)

        print(f"SUCCESS -> Parse tree generated at: {output_path}.{format}\n")

    
    def generate_name(self, path):
        """
        Generates the output file name based on the input file name.

        Args:
            - path: The path to the input file.

        Returns:
            - The output file name.
        """
        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(path))[0]

        # Append the file name to the output file name
        output_file_name = f"parse_tree_{file_name}"

        return output_file_name