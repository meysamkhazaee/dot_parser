import networkx as nx
import sys

# Function to read a .dot file and return a graph
def read_dot_file(file_name):
    try:
        return nx.drawing.nx_pydot.read_dot(file_name)
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return None

# Function to check if two graphs are isomorphic
def are_graphs_isomorphic(graph1, graph2):
    return nx.is_isomorphic(graph1, graph2)

# Comparison functions
def compare_node_edge_counts(graph1, graph2):
    nodes1 = graph1.number_of_nodes()
    nodes2 = graph2.number_of_nodes()
    edges1 = graph1.number_of_edges()
    edges2 = graph2.number_of_edges()
    
    if nodes1 != nodes2:
        print(f"Different number of nodes: {nodes1} vs {nodes2}")
    if edges1 != edges2:
        print(f"Different number of edges: {edges1} vs {edges2}")

def compare_degree_sequences(graph1, graph2):
    degree_seq1 = sorted([d for n, d in graph1.degree()], reverse=True)
    degree_seq2 = sorted([d for n, d in graph2.degree()], reverse=True)
    
    if degree_seq1 != degree_seq2:
        print(f"Different degree sequences:\nGraph1: {degree_seq1}\nGraph2: {degree_seq2}")

def compare_connected_components(graph1, graph2):
    cc1 = nx.number_connected_components(graph1)
    cc2 = nx.number_connected_components(graph2)
    
    if cc1 != cc2:
        print(f"Different number of connected components: {cc1} vs {cc2}")

# def compare_cycles(graph1, graph2):
#     cycles1 = list(nx.cycle_basis(graph1))
#     cycles2 = list(nx.cycle_basis(graph2))
    
#     if len(cycles1) != len(cycles2):
#         print(f"Different number of cycles: {len(cycles1)} vs {len(cycles2)}")

def compare_node_attributes(graph1, graph2, attribute):
    attrs1 = sorted(nx.get_node_attributes(graph1, attribute).values())
    attrs2 = sorted(nx.get_node_attributes(graph2, attribute).values())
    
    if attrs1 != attrs2:
        print(f"Different {attribute} attributes:\nGraph1: {attrs1}\nGraph2: {attrs2}")

def detailed_graph_comparison(graph1, graph2):
    print("\n--- Detailed Graph Comparison ---")
    compare_node_edge_counts(graph1, graph2)
    compare_degree_sequences(graph1, graph2)
    # compare_connected_components(graph1, graph2)
    # compare_cycles(graph1, graph2)
    
    # If graphs have specific node attributes, compare them
    # For example, if nodes have 'label' attributes
    compare_node_attributes(graph1, graph2, 'label')
    
    print("--- End of Comparison ---\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1.dot> <file2.dot>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    # Read the .dot files and create graphs
    graph1 = read_dot_file(file1)
    graph2 = read_dot_file(file2)

    if graph1 is None or graph2 is None:
        sys.exit(1)

    # Check if the graphs are isomorphic
    result = are_graphs_isomorphic(graph1, graph2)
    print(f"The graphs are isomorphic: {result}")

    if not result:
        # Perform detailed comparison to identify discrepancies
        detailed_graph_comparison(graph1, graph2)
