import pydot
from IPython.display import Image, display
import os
import sys
import logging

def setup_logger(infile_name):

    """Sets up logging for the given input file."""
    logger = logging.getLogger(infile_name)
    logger.setLevel(logging.DEBUG)
    
    # Ensure the result directory exists
    result_dir = os.path.join(os.path.dirname(__file__), "result")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    handler = logging.FileHandler(filename=f"result/{infile_name}.log", mode='w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def process_graph(graph, logger):
    subgraphs = graph.get_subgraphs()
    for subgraph in subgraphs:
       logger.info(f"proccessing {subgraph.get_label()} subgraph ...")
       combine_consecutive_nodes(subgraph, logger)
    logger.info(f"proccessing root graph ...")
    combine_consecutive_nodes(graph, logger)

# Function to combine consecutive nodes
def combine_consecutive_nodes(graph, logger):

    visited  = []

    if len(graph.get_nodes()) == 0:

        for e in graph.get_edges():

            if e.get_source() not in visited:
                graph.add_node(pydot.Node(e.get_source()))
                visited.append(e.get_source())

            if e.get_destination() not in visited:
                graph.add_node(pydot.Node(e.get_destination()))
                visited.append(e.get_destination())

    logger.debug(f"The initial number of nodes: {len(graph.get_nodes())}")
    
    deleted_node = 0
    inserted_node = 0

    for node in graph.get_nodes():

        node_name = node.get_name()
        dst_of_node = [e.get_destination() for e in graph.get_edges() if e.get_source() == node_name]
        src_of_node = [e.get_source() for e in graph.get_edges() if e.get_destination() == node_name]
        
        if len(src_of_node) == 1:
            
            # check updated graph changes during loop itrations to prevdent bug.
            if src_of_node[0] in dst_of_node:
                continue

            # Combine the nodes
            child_of_src = [e.get_source() for e in graph.get_edges() if e.get_source() == src_of_node[0]]

            if len(child_of_src) != 1:
                continue

            graph.del_edge(src_of_node[0], node_name)
            new_node_name = src_of_node[0] + "_" + node_name
            source_node = [n for n in graph.get_nodes() if n.get_name() == src_of_node[0]]
            node_content = f"{source_node[0].get_label()}\n{node.get_label()}".replace('"', '')
            new_node = pydot.Node(new_node_name, label=node_content, shape='Mrecord' ,fontsize=22 ,color='red')
            graph.add_node(new_node)
            inserted_node += 1

            for dest in dst_of_node:
                graph.add_edge(pydot.Edge(new_node, dest))
                graph.del_edge(node_name, dest)

            # update edges
            for e in graph.get_edges():
                if e.get_destination() == src_of_node[0]:
                    graph.add_edge(pydot.Edge(e.get_source(), new_node))
                    graph.del_edge(e.get_source(), e.get_destination())
                
            graph.del_node(node_name)
            graph.del_node(src_of_node[0])
            deleted_node += 2

    logger.debug(f"The number of deleted nodes: {deleted_node}")
    logger.debug(f"The number of inserted nodes: {inserted_node}")

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

    logger = setup_logger(file_name)
    logger.debug(f"File path: {full_path}")
     
    # Load the DOT file
    graphs = pydot.graph_from_dot_file(full_path)
    if not graphs:
        logger.error("Failed to load the DOT file.")
        return

    graph = graphs[0]

    # Ensure the result directory exists
    result_dir = os.path.join(os.path.dirname(__file__), "result")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    # Save the original graph as a PNG file
    original_png_path = os.path.join(result_dir, f'{file_name}.png')
    graph.write_png(original_png_path)
    
    logger.info(f"Original graph saved to: {original_png_path}")

    # Display the original graph image
    display(Image(filename=original_png_path))

    # Process input graph
    process_graph(graph, logger)
    
    # Save the updated graph as a PNG file
    updated_png_path = os.path.join(result_dir, f'{file_name}_updated.png')
    graph.write_png(updated_png_path)
    
    logger.info(f"Updated graph saved to: {updated_png_path}")

    # Save the updated graph as a DOT file
    updated_dot_path = os.path.join(result_dir, f'{file_name}_updated.dot')
    graph.write_raw(updated_dot_path)
    
    logger.info(f"Updated DOT file saved to: {updated_dot_path}")

    # Display the updated graph image
    display(Image(filename=updated_png_path))

if __name__ == "__main__":
    main()
