import generator_graph as gg
import  statistics as s

if __name__ == '__main__':

    # Part 1: Generation of graph

    G = gg.generate_graph("reduced_dblp.json")
    ### Visualization of the graph
    gg.visualize_graph(G)

    # Part 2: Statistics

    s.stat_conference(G, 'conf/pkdd/2017-1')
    s.stat_authors('mohammed j. zaki', 10, G)
