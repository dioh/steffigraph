import matplotlib.pyplot as plt
import networkx as nx 
import random as rnd
import collections
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or pydot")

def gen_degree_value(length, alpha=10, beta=1):
    deg_seq = [int(rnd.gammavariate(alpha, beta)) for i in xrange(length)]  
    if sum(deg_seq) % 2 == 1:                                               
        deg_seq[-1] += 1                         
    return deg_seq                               


def draw_graph(G, layout_program='sfdp'):
    # Layout program options follow the Graphviz convention:
    # dot  filter for drawing directed graphs
    # neato  filter for drawing undirected graphs
    # twopi  filter for radial layouts of graphs
    # circo  filter for circular layout of graphs
    # fdp  filter for drawing undirected graphs
    # sfdp  filter for drawing large undirected graphs
    # patchwork  filter for squarified tree maps
    # osage  filter for array-based layout

    pos = graphviz_layout(G, prog=layout_program, root=0)
    nx.draw(G, pos,
        with_labels=False,
        alpha=0.3,
        node_size=20) 
    plt.show()

def draw_degree_histogram(G):
    # Draw the histogram of the graph in question with superimposed graph structure.
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    pos = nx.spring_layout(G)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)

    plt.show()


def generate_graph(n, *args, **kwargs):
    G = nx.configuration_model(gen_degree_value(n),
            kwargs.get('alfa', None),
            kwargs.get('beta', None)) 
    return G


G = generate_graph(100) 


draw_graph(G)
#draw_degree_histogram(G)
