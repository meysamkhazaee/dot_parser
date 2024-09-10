import pydot

# Create a graph
graph = pydot.Dot(graph_type='digraph')

# Add nodes and edges
node1 = pydot.Node('Node1')
node2 = pydot.Node('Node2')
node2 = pydot.Node('Node2')
node3 = pydot.Node('Node3')
graph.add_node(node1)
graph.add_node(node2)
graph.add_node(node3)
graph.add_edge(pydot.Edge('Node1', 'Node2'))
graph.add_edge(pydot.Edge('Node1', 'Node2'))
graph.add_edge(pydot.Edge('Node1', 'Node2'))
graph.add_edge(pydot.Edge('Node2', 'Node3'))
graph.add_edge(pydot.Edge('Node2', 'Node1'))  # Adding an edge from Node2 to Node1

# Delete the edge Node2 -> Node1
# edges = graph.get_edge('Node2', 'Node1')
# for edge in edges:
#     graph.del_edge(edge.get_source(), edge.get_destination())

# Print the graph
print(graph.to_string())
