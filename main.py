import generator_graph as gg
import  statistics as s
import generalized_E_number as gEn

if __name__ == '__main__':

    # Part 1: Generation of graph

    G = gg.generate_graph("full_dblp.json")
    ### Visualization of the graph
    gg.visualize_graph(G)

    # Part 2: Statistics

    s.stat_conference(G, 'conf/pkdd/2017-1')
    s.stat_authors('mohammed j. zaki', 10, G)


    # Part 3: Generalized Erdos Number

    aris_id = 256176
    weight = gEn.dijkstra(G, 255207, aris_id)
    print(weight)

    ## Example of exercise 3.b -> we use 21 nodes connected to aris

    aris_connected = {}
    i = 0
    while len(aris_connected) < 21:
        try:
            aris_connected[G.nodes()[i]] = gEn.dijkstra(G, G.nodes()[i], aris_id)
        except:
            pass
        i += 1

    ##we can now take those nodes as the set of subnodes for the computation of the groupnumber
    subset_of_nodes = list(aris_connected.keys())
    result = gEn.GroupNumber(subset_of_nodes)
    print(result)
