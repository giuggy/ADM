import networkx as nx
import json
from matplotlib import pylab as pl

def visualize_graph(graph):
    '''
    This function allows to visualize the graph in input
    :param graph: input graph
    :return: plot of the graph
    '''
    pl.figure()
    nx.draw_networkx(graph)
    pl.show()

def generate_graph(path):
    '''
    Generation of the graph
    :param path: path of the data that the code needs to parse
    :return: Graph
    '''

    ## Parsed of the data
    url = path
    with open(url) as jsonfile:
        data = json.load(jsonfile)

    ## Definition of the dictionaries
    # dictionary : keys -> id_authors, values -> authors with common publications
    dic_auth = {}
    # dictionary: keys -> id_authors, values -> important attributes
    dic_conf = {}
    # dictionary: keys -> id_authors, values -> publications
    dic_pub = {}

    ## Loop on data to take the important info
    for entry in data:
        authors = entry['authors']
        id_conf, title_conf, id_pub = entry['id_conference_int'], entry['id_conference'], entry['id_publication_int']
        ident, names = zip(*[(auth['author_id'], auth['author']) for auth in authors])
    ## The keys of the dictionaries are the author_ids
        for i in range(len(ident)):
            id_key, id_name = ident[i], names[i]
            lst = set(ident) - {id_key}
            conf = {'author': id_name, 'id_conference': (id_conf, title_conf)}

            try:
                dic_auth[id_key] = dic_auth[id_key].union(lst)
                dic_conf[id_key]['id_conference'].append(conf['id_conference'])
                dic_pub[id_key].append(id_pub)
            except:
                dic_auth[id_key] = lst

                conf['id_conference'] = [conf['id_conference']]
                dic_conf[id_key] = conf
                dic_pub[id_key] = [id_pub]

    ## Definition of graph with default attributes

    G = nx.from_dict_of_lists(dic_auth)
    nx.set_node_attributes(G, "", "author")
    nx.set_node_attributes(G, 0, "id_conference_int")
    nx.set_node_attributes(G, "", "id_conference")
    nx.set_node_attributes(G, 0, "id_publication_int")

    ## Setting of attributes per each node
    for u, v, d in G.edges(data=True):
        G.node[u]['author'] = dic_conf[u]['author']
        id_conf, id_conf_int = zip(*dic_conf[u]['id_conference'])
        G.node[u]["id_conference_int"], G.node[u]["id_conference"] = list(id_conf), list(id_conf_int)
        G.node[u]["id_publication_int"] = dic_pub[u]

        G.node[v]['author'] = dic_conf[v]['author']
        id_conf, id_conf_int = zip(*dic_conf[v]['id_conference'])
        G.node[v]["id_conference_int"], G.node[v]["id_conference"] = list(id_conf), list(id_conf_int)
        G.node[v]["id_publication_int"] = dic_pub[v]

        a, b = set(dic_pub[u]), set(dic_pub[v])
        d['weight'] = 1 - len(a.intersection(b)) / float(len(a.union(b)))

    return G

