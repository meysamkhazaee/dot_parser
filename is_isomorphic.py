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
