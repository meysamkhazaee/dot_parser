import pydot
from IPython.display import Image, display
import os
import sys
import time

# Function to combine consecutive nodes
def combine_consecutive_nodes(graph):
    nodes_to_remove = set()
    new_edges = []
    node_map = {}  # To keep track of combined nodes
    
    nodes = graph.get_nodes()
    edges = graph.get_edges()

    visited  = []
    if len(nodes) == 0:
        for e in edges:
            if e.get_source() not in visited:
                graph.add_node(pydot.Node(e.get_source()))
                visited.append(e.get_source())
            if e.get_destination() not in visited:
                graph.add_node(pydot.Node(e.get_source()))
                visited.append(e.get_source())

    nodes = graph.get_nodes()
    for node in nodes:
        node_name = node.get_name()
        dst_of_node = [e.get_destination() for e in edges if e.get_source() == node_name]
        src_of_node = [e.get_source() for e in edges if e.get_destination() == node_name]
        
        if len(dst_of_node) == 1 and len(src_of_node) == 1:
            # Combine the nodes
            child_of_src = [e.get_source() for e in edges if e.get_source() == src_of_node[0]]
            if len(child_of_src) != 1:
                continue
            new_node_name = src_of_node[0] + "_" + node_name
            source_node = [n for n in nodes if n.get_name() == src_of_node[0]]
            node_content = f"{source_node[0].get_label()}\n{node.get_label()}".replace('"', '')
            new_node = pydot.Node(new_node_name, label=node_content)
            graph.add_node(new_node)
            graph.add_edge(pydot.Edge(new_node, dst_of_node[0]))
            for e in edges:
                if e.get_destination() == src_of_node[0]:
                    graph.add_edge(pydot.Edge(e.get_source(), new_node))
                    graph.del_edge(e.get_source(), e.get_destination())
                elif e.get_source() == src_of_node[0]:
                    graph.del_edge(e.get_source(), e.get_destination())
                elif e.get_destination() == dst_of_node[0]:
                    graph.del_edge(e.get_source(), e.get_destination())
                
            graph.del_node(node_name)
            graph.del_node(src_of_node[0])

    
    return graph

def main():
    
    # Handle command-line arguments or prompt the user for input
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to the DOT file: ")

    root = os.path.dirname(__file__)

    full_path = os.path.join(root, file_path)
    full_path = os.path.normpath(full_path)
    file_name, file_ext = os.path.splitext(full_path)
    file_name = os.path.basename(file_name)
    
    # Load the DOT file
    graphs = pydot.graph_from_dot_file(full_path)
    if not graphs:
        print("Failed to load the DOT file.")
        return

    graph = graphs[0]

    # if not os.path.exists(os.path.join(root, "result")):
    #     os.makedirs(os.path.join(root, "result"))
    
    # # Save the graph as a PNG file
    # graph.write_png(f'result/{file_name}.png')

    # # Display the base graph image
    # display(Image(filename=f'result/{file_name}.png'))

    # # Combine consecutive nodes
    # graph = combine_consecutive_nodes(graph)
    
    # # Save the updated graph as a PNG file
    # graph.write_png(f'result/{file_name}_updated.png')

    # # Display the updated graph image
    # image_path = f'result/{file_name}_updated.png'
    # display(Image(filename=image_path))

    # Ensure the result directory exists
    result_dir = os.path.join(os.path.dirname(__file__), "result")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    # Save the original graph as a PNG file
    original_png_path = os.path.join(result_dir, f'{file_name}.png')
    graph.write_png(original_png_path)

    # Display the original graph image
    display(Image(filename=original_png_path))

    # Combine consecutive nodes
    graph = combine_consecutive_nodes(graph)
    
    # Save the updated graph as a PNG file
    updated_png_path = os.path.join(result_dir, f'{file_name}_updated.png')
    graph.write_png(updated_png_path)

    # Save the updated graph as a DOT file
    updated_dot_path = os.path.join(result_dir, f'{file_name}_updated.dot')
    graph.write_raw(updated_dot_path)

    # Display the updated graph image
    display(Image(filename=updated_png_path))

if __name__ == '__main__':
    main()