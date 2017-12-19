import networkx as nx
import generator_graph as gg
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
from operator import itemgetter


def stat_conference(graph, conference):
    '''
    This function calculates the induced graph selecting only the nodes that have in its attribute the conference passed in input. On this graph
    the method calculates the basic statistics and plot the sub_graph and the curves.
    :param graph: graph that the user wants to use for the statistics
    :param conference: input value of the attribute that the node of sub_graph needs to have
    :return: plot of the subgraph and the curve of the basic statistics (degree, closeness, betweeness)
    '''
    try:
        str(conference)
        nodes = [p for (p, d) in graph.nodes(data=True) if conference in d['id_conference']]
    except:
        nodes = [p for (p, d) in graph.nodes(data=True) if conference in d['id_conference_int']]

    sub_graph = graph.subgraph(nodes)

    ## Plot graphs
    gg.visualize_graph(sub_graph)

    ## Statistics
    degree_seq = sorted(nx.degree(sub_graph), key=itemgetter(0))
    nodes_lst, degree_lst = zip(*degree_seq)

    clos = sorted(nx.closeness_centrality(sub_graph, wf_improved=False).items(), key=itemgetter(0))
    closeness_lst = tuple(zip(*clos))[1]

    betw = sorted(nx.betweenness_centrality(sub_graph, normalized=False).items(), key=itemgetter(0))
    betweeness_lst = tuple(zip(*betw))[1]

    ## Legend
    blue_patch = mpatches.Patch(color='blue', label="Degree")
    orange_patch = mpatches.Patch(color='orange', label="Closeness")
    green_patch = mpatches.Patch(color='green', label="Betweeness")

    ## Plot Statistics
    f, ax = plt.subplots(1)
    ax.plot(nodes_lst, degree_lst)
    ax.plot(nodes_lst, closeness_lst)
    ax.plot(nodes_lst, betweeness_lst)
    ax.xaxis.set_major_formatter(plt.NullFormatter())

    plt.title("Statistics' plot")
    plt.legend(handles=[blue_patch, orange_patch, green_patch])
    plt.show()


def stat_authors(author, d, G):
    '''
    This function elaborates the induce graph which has the nodes that at most d hops distance with the input author
    :param author: input node
    :param d: hops distance
    :param G: input graph
    :return: plot of the induced graph
    '''

    try:
        str(author)
        source = [p for (p, d) in G.nodes(data=True) if d['author'] == author][0]
    except:
        source = author

    ## Selection of the paths that respect the constrition of d
    p = nx.shortest_path(G, source=source)
    p_path = {k: v for k, v in p.items() if len(v) <= d + 1 and len(v) > 1}

    ## Construction of the sub_graph
    nodes_p_path = list(p_path.keys())
    sub_graph = G.subgraph(nodes_p_path)

    ## Visualization of the graph
    gg.visualize_graph(sub_graph)
