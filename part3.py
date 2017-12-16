
# coding: utf-8

# In[536]:


"""
An example using Graph as a weighted network.
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

G=nx.Graph()

G.add_edge('a','b',weight=0.6)
G.add_edge('a','c',weight=0.1)
G.add_edge('c','d',weight=0.1)
G.add_edge('c','e',weight=0.7)
G.add_edge('c','f',weight=0.9)
G.add_edge('a','d',weight=0.3)

elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]

pos=nx.spring_layout(G) # positions for all nodes

# nodes
nx.draw_networkx_nodes(G,pos,node_size=700)

# edges
nx.draw_networkx_edges(G,pos,edgelist=elarge,
                    width=6)
nx.draw_networkx_edges(G,pos,edgelist=esmall,
                    width=6,alpha=0.5,edge_color='b',style='dashed')

# labels
nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

plt.axis('off')
#plt.savefig("weighted_graph.png") # save as png
plt.show() # display


# In[473]:


#dijkstra algorithm generalized (if we don't put the end node) otherwise he calculates the path between 2 nodes
def dijkstra(graph, start, end = None):
    #ficreate the graph dictionary in the form {node: {neighbour: weight}
    graph_dict = {}
    for node in graph:
        graph_dict[node] = {}
        for neighbour in graph[node]:
            graph_dict[node][neighbour] = graph[node][neighbour].get('weight')
    
    # empty dictionary to hold distances
    distances = {} 
    # list of vertices in path to current vertex
    predecessors = {} 
    
    # get all the nodes that need to be assessed
    to_assess = graph_dict.keys() 

    # set all initial distances to infinity
    #  and no predecessor for any node
    for node in graph_dict:
        distances[node] = float('inf')
        predecessors[node] = None
    
    # set the initial collection of 
    # permanently labelled nodes to be empty
    sp_set = []

    # set the distance from the start node to be 0
    distances[start] = 0
    
    # as long as there are still nodes to assess:
    while len(sp_set) < len(to_assess):
        # chop out any nodes with a permanent label
        still_in = {node: distances[node]                    for node in [node for node in                    to_assess if node not in sp_set]}
        # find the closest node to the current node
        closest = min(still_in, key = distances.get)
        
        # and add it to the permanently labelled nodes
        sp_set.append(closest)
                
        # then for all the neighbours of 
        # the closest node (that was just added to
        # the permanent set)
        
        #this for cycle takes too much time if there are many nodes
        for node in graph_dict[closest]:
            # if a shorter path to that node can be found
            if distances[node] > distances[closest] +                       graph_dict[closest][node]:

                # update the distance with 
                # that shorter distance
                distances[node] = round(distances[closest] +                       graph_dict[closest][node],2)
                
                # set the predecessor for that node
                predecessors[node] = closest

    #if the end node is not specified we return the distances and path between the starting node and every other node
    if end == None:
        paths = {}
        for node in graph_dict:
            if node != start:
                path = [node]
                while start not in path:
                    path.append(predecessors[path[-1]])
                    paths[node] = path[::-1]

        return distances,paths
            
    # once the loop is complete the final 
    # path needs to be calculated - this can
    # be done by backtracking through the predecessors
    else:
        path = [end]
        while start not in path:
            path.append(predecessors[path[-1]])

        # return the path in order start -> end, and it's cost
        return path[::-1], round(distances[end],2)


# In[474]:


#b) we have a subset of nodes (subset_of_nodes)

#ex: take 2 nodes of the above graph and return the GroupNumber for each node of (Graph - nodes_in_subset)
#subset_of_nodes = input().split()
subset_of_nodes = list('ac')

GroupNumber = {} #define a groupnumber dictionary {node: {sub_node : shortest_path)}}
for node in G:
    if node not in subset_of_nodes:
        GroupNumber[node] = {}
        for i in range(1, len(subset_of_nodes)):
            #we take the minimum path
            GroupNumber[node][subset_of_nodes[i-1]] = dijkstra(G, node, subset_of_nodes[i-1])
            if GroupNumber[node][subset_of_nodes[i-1]][1] > dijkstra(G, node, subset_of_nodes[i])[1]:
                GroupNumber[node][subset_of_nodes[i]] = dijkstra(G, node, subset_of_nodes[i])
                GroupNumber[node].pop(subset_of_nodes[i-1])
GroupNumber

