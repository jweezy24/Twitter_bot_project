import networkx as nx
import matplotlib.pyplot as plt

''' 
This method will create a graph object for the visualization.
input:
    list of nodes with distances
output:
    graph object with the nodes with their distances.
'''
def create_graph_obj(root_node, nodes):
    G = nx.Graph()
    G.add_node(root_node)

    for node,x,y in nodes:
        G.add_node(node)
        print(f"{x} {y} {node}")
        G.add_edge(root_node, node, weight=(y/x))
    
    
    nx.draw(G, with_labels=True)
    plt.show()

    return G