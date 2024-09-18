import pydot
import os
from logger import logger_class
# from IPython.display import Image, display

class process_graph:
    def __init__(self, infile_path):
        root_dir = os.path.dirname(__file__)

        full_path = os.path.join(root_dir, infile_path)
        full_path = os.path.normpath(full_path)
        file_name, file_ext = os.path.splitext(full_path)
        file_name = os.path.basename(file_name)

        logger_obj = logger_class(full_path, file_name)
        self.logger = logger_obj.get()

        # Load the DOT file
        graphs = pydot.graph_from_dot_file(full_path)
        if not graphs:
            self.logger.error("Failed to load the DOT file.")
            return

        self.root_graph = graphs[0]

        self.all_nodes = []
        self.update_all_nodes(self.root_graph)

        self.all_edges = []
        self.update_all_edges(self.root_graph)

    def return_nodes(self, graph):
        nodes = []
        for node in graph.get_nodes():
            nodes.append(node)
        return nodes

    def update_all_nodes(self, graph):
        self.all_nodes += self.return_nodes(graph)
        for sub_graph in graph.get_subgraphs():
            self.all_nodes += self.return_nodes(sub_graph)

    def return_edges(self, graph):
        edges = []
        for edge in graph.get_edges():
            edges.append(edge)
        return edges
    
    def update_all_edges(self, graph):
        self.all_edges += self.return_edges(graph)
        for sub_graph in graph.get_subgraphs():
            self.all_edges += self.return_edges(sub_graph)

    def remove_edge_graph(self, graph, source_node_name, destination_node_name):
        # Remove the edge directly from the graph using the node names
        graph.del_edge(source_node_name, destination_node_name)

        # If you want to delete the edge from subgraphs as well
        for subgraph in graph.get_subgraphs():
            self.remove_edge_graph(subgraph, source_node_name, destination_node_name)

    def remove_node_graph(self, graph, node_name):
        for node in graph.get_nodes():
            if node.get_name() == node_name:
                graph.del_node(node)

        for subgraph in graph.get_subgraphs():
            self.remove_node_graph(subgraph, node_name)
    
    # Function to combine consecutive nodes
    def combine_consecutive_nodes(self, graph):

        self.logger.debug(f"The initial number of nodes: {len(graph.get_nodes())}")
        
        deleted_node = 0
        inserted_node = 0

        # for node in graph.get_nodes():
        idx = 0
        while idx < len(self.all_nodes):

            node_name = self.all_nodes[idx].get_name()
            dst_of_node = [e.get_destination() for e in self.all_edges if e.get_source() == node_name]
            src_of_node = [e.get_source() for e in self.all_edges if e.get_destination() == node_name]
            
            if len(src_of_node) == 1:

                # check updated graph changes during loop itrations to prevdent bug.
                if src_of_node[0] in dst_of_node:
                    idx = idx + 1
                    continue

                # Combine the nodes
                child_of_src = [e.get_destination() for e in self.all_edges if e.get_source() == src_of_node[0]]

                if len(child_of_src) != 1:
                    idx = idx + 1
                    continue

                # ignore nodes that is in separate subgraphs 
                if False == self.are_nodes_in_same_subgraph(src_of_node[0],node_name, graph):
                    idx = idx + 1
                    continue

                self.remove_edge_graph(graph, src_of_node[0], node_name)
                new_node_name = src_of_node[0] + "_" + node_name
                source_node = [n for n in self.all_nodes if n.get_name() == src_of_node[0]]
                node_content = f"{source_node[0].get_label()}\n{self.all_nodes[idx].get_label()}".replace('"', '')
                new_node = pydot.Node(new_node_name, label=node_content, shape='Mrecord' ,fontsize=22 ,color='red')
                graph.add_node(new_node)
                self.all_nodes.append(new_node)
                inserted_node += 1

                for dest in dst_of_node:
                    new_edge = pydot.Edge(new_node.get_name(), dest)
                    graph.add_edge(new_edge)
                    self.all_edges.append(new_edge)
                    self.remove_edge_graph(graph, node_name, dest)

                # update edges
                for e in self.all_edges:
                    if e.get_destination() == src_of_node[0]:
                        new_edge = pydot.Edge(e.get_source(), new_node)
                        graph.add_edge(new_edge)
                        self.all_edges.append(new_edge)
                        self.remove_edge_graph(graph, e.get_source(), e.get_destination())

                self.remove_node_graph(graph, node_name)
                idx = idx - 1
                self.remove_node_graph(graph, src_of_node[0])
                self.all_nodes = []
                self.update_all_nodes(graph)
                self.all_edges = []
                self.update_all_edges(graph)
                deleted_node += 2
            idx = idx + 1

        self.logger.debug(f"The number of deleted nodes: {deleted_node}")
        self.logger.debug(f"The number of inserted nodes: {inserted_node}")
    
    def generate_png(self, out_path):
        self.root_graph.write_png(out_path)
        self.logger.info(f"graph saved to: {out_path}")

    def generate_dot(self, out_path):
        self.root_graph.write_raw(out_path)
        self.logger.info(f"Updated DOT file saved to: {out_path}")

    def handle_function_call_subgraph(self, graph):
        for edge in self.all_edges:
            edge_attributes = edge.get_attributes()
            
            # Check if lhead attribute exists
            if 'lhead' in edge_attributes:
                lhead_value = edge_attributes['lhead']
                
                # Retrieve the source and destination nodes of the edge
                source_node = edge.get_source()
                child_of_src = [e.get_destination() for e in self.all_edges if e.get_source() == source_node]
                destination_node = edge.get_destination()
                child_of_src.remove(destination_node)
                
                # Step 3: Find the corresponding subgraph
                for subgraph in graph.get_subgraphs():
                    if subgraph.get_name() == lhead_value:
                        
                        # Step 4: Get the first node in the subgraph
                        subgraph_nodes = subgraph.get_nodes()
                        if subgraph_nodes:
                            first_node_subgraph = subgraph_nodes[0].get_name()  # First node
                            last_node_subgraph = subgraph_nodes[-1].get_name()  # Last node

                            # Step 5: Find edges that end at destination_node and reconnect them to first_node_subgraph
                            for e in self.all_edges:
                                if e.get_destination() == destination_node:
                                    new_edge = pydot.Edge(e.get_source(), first_node_subgraph)
                                    graph.add_edge(new_edge)
                                    self.remove_edge_graph(graph, e.get_source(), destination_node)
                                    for child in child_of_src:
                                        new_edge = pydot.Edge(last_node_subgraph, child)
                                        graph.add_edge(new_edge)
                                        self.remove_edge_graph(graph, e.get_source(), child)

                            self.all_edges = []
                            self.update_all_edges(graph)

                            for node in self.all_nodes:
                                if node.get_name() == destination_node:
                                    graph.del_node(node) 

                            self.all_nodes = []
                            self.update_all_nodes(graph)

    def are_nodes_in_same_subgraph(self, node1, node2, graph):
        """
        Check if two nodes are in the same subgraph.
        """
        # Retrieve all subgraphs
        for subgraph in graph.get_subgraphs():
            # Get nodes in the current subgraph
            subgraph_nodes = {node.get_name() for node in subgraph.get_nodes()}
            
            # Check if both nodes are in the current subgraph
            if node1 in subgraph_nodes and node2 in subgraph_nodes:
                return True
        
        return False