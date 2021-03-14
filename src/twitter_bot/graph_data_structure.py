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
    # G = nx.Graph()
    # G.add_node(root_node)

    # for node,x,y in nodes:
    #     G.add_node(node)
    #     print(f"{x} {y} {node}")
    #     G.add_edge(root_node, node, weight=(y/x))
    
    plt.annotate(xy=[0,0], s=root_node)
    for node,x,y in nodes:
        plt.annotate(xy=[x,y], s=node)
        plt.plot([0,x], [0,y])

    #nx.draw(G, with_labels=True)
    plt.show()

    return G