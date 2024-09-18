import pydot
import os

# Step 1: Load the DOT file
dot_file_path = 'input/singlefunctionscalls-cfg-goto.dot'  # Replace with your actual DOT file path
graphs = pydot.graph_from_dot_file(dot_file_path)
graph = graphs[0]  # Get the first graph if multiple graphs are parsed

for edge in graph.get_edges():
    edge_attributes = edge.get_attributes()
    
    # Check if lhead attribute exists
    if 'lhead' in edge_attributes:
        lhead_value = edge_attributes['lhead']
        
        # Retrieve the source and destination nodes of the edge
        source_node = edge.get_source()
        child_of_src = [e.get_destination() for e in graph.get_edges() if e.get_source() == source_node]
        print(child_of_src)
        destination_node = edge.get_destination()
        
        # Output the edge information with lhead attribute
        print(f"Edge from {source_node} -> {destination_node} has lhead attribute: {lhead_value}")
        
        # Step 3: Find the corresponding subgraph
        for subgraph in graph.get_subgraphs():
            if subgraph.get_name() == lhead_value:
                print(f"Found subgraph: {lhead_value}")
                
                # Step 4: Get the first node in the subgraph
                subgraph_nodes = subgraph.get_nodes()
                if subgraph_nodes:
                    first_node_subgraph = subgraph_nodes[0].get_name()  # First node
                    last_node_subgraph = subgraph_nodes[-1].get_name()  # Last node
                    print(f"First node of subgraph {lhead_value}: {first_node_subgraph}")
                    print(f"Last node of subgraph {lhead_value}: {first_node_subgraph}")

                    # Step 5: Find edges that end at destination_node and reconnect them to first_node_subgraph
                    for e in graph.get_edges():
                        if e.get_destination() == destination_node:
                            new_edge = pydot.Edge(e.get_source(), first_node_subgraph)
                            graph.add_edge(new_edge)
                            graph.del_edge(edge.get_source(), edge.get_destination())

                    # for node in graph.get_nodes():
                    #     if node.get_name() == destination_node:
                    #         graph.del_node(node) 

                    # for e in graph.get_edges():
                    #     if e.get_source() == source_node:
                    #         new_edge = pydot.Edge(last_node_subgraph, e.get_destination())
                    #         graph.add_edge(new_edge)
                    #         graph.del_edge(edge.get_source(), edge.get_destination())
  
                        
                else:
                    print(f"No nodes found in subgraph {lhead_value}")

# Optional: Save modified graph as a PNG
modified_png_path = os.path.join(os.path.dirname(__file__), 'modified_sample.png')
graph.write_png(modified_png_path)
