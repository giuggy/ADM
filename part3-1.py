
# coding: utf-8

# In[1]:


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


# In[2]:


import heapq

def dijkstra(graph, initial, end=None):
    visited = {initial: 0}
    h = [(0, initial)]
    path = {}
    nodes = graph.nodes()

    while nodes and h:
        current_weight, min_node = heapq.heappop(h)
        try:
            while min_node not in nodes:
                current_weight, min_node = heapq.heappop(h)
        except IndexError:
            break

        nodes.remove(min_node)
        for v in graph[min_node]:
            weight = current_weight + graph[min_node][v]['weight']
            if v not in visited or weight < visited[v]:
                visited[v] = round(weight,2)
                heapq.heappush(h, (weight, v))
                path[v] = min_node 
    if end == None:
        paths = {}
        for node in graph:
            if node != initial:
                p = [node]
                while initial not in p:
                    p.append(path[p[-1]])
                    paths[node] = p[::-1]
        #if the end node is not specified we return the distances and path between the starting node and every other node
        return visited, paths
    
    # if we want the shortest path between 2 nodes we calculate the min path between them
    else:
        p = [end]
        while initial not in p:
            p.append(path[p[-1]])

        return visited[end],p[::-1] 



# In[3]:


dijkstra(G,'b')


# In[107]:


#b) we have a subset of nodes (subset_of_nodes)

#ex: take 2 nodes of the above graph and return the GroupNumber for each node of (Graph - nodes_in_subset)
#subset_of_nodes = input().split()
subset_of_nodes = list('ab')

GroupNumber = {} #define a groupnumber dictionary {node: {sub_node : shortest_path)}}
for node in [item for item in G.nodes() if item not in subset_of_nodes]:
    GroupNumber[node] = {}
    weight = float('Inf')
    for subnode in subset_of_nodes:
        #we take the minimum path
        if dijkstra(G, node, subnode)[0] < weight:
            GroupNumber[node].clear()
            GroupNumber[node][subnode] = dijkstra(G, node, subnode)
            weight = dijkstra(G, node, subnode)[0]

GroupNumber


# In[122]:


### Part 1: Building up the Graph


#############
# 1.1 : The first step to build the graph is to read the data from the json file;
# Therefor we import the "json" library and then
#define the URL to the file and read the data to a variable;
#The variable is called "data" in our code.

# takes almost 20 sec for the full data
import json
url = "/Users/MicheleDiMuccio/Desktop/AMD_HM4/reduced_dblp.json"
with open(url) as jsonfile:
    data = json.load(jsonfile)
    #print (data[0])


##############
# 1.2 We create a dictionary that holds the authors' IDs
#as the keys and the co-authors as values.

g = {}
for i in range(len(data)): # each i is a collection related to a published paper
    for j in data[i]['authors']: # each j is an author
        if j['author_id'] in g: # we are checking to see if the author's id is already in the dictionary g
            temp = [] # temporary list of co-authors
            for z in range(len(data[i]['authors'])):
                temp.append(data[i]['authors'][z]['author_id']) if data[i]['authors'][z]['author_id'] != j['author_id'] else True
            if len(temp) > 0:
                g[j['author_id']].append(temp)
        else:
            g[j['author_id']] = []
            temp = []
            for z in range(len(data[i]['authors'])):
                temp.append(data[i]['authors'][z]['author_id']) if data[i]['authors'][z]['author_id'] != j['author_id'] else True
            if len(temp) > 0:
                g[j['author_id']].append(temp)



##############
# 1.3 : We create another dictionary whose keys and values are authors' IDs and
# conferences' IDs respectively.
h = {} # dictionary of the ids and conference ids.
for i in range(len(data)):
    for j in data[i]['authors']:
        if j['author_id'] in h:
            h[j['author_id']].add(data[i]['id_conference_int'])
        else:
            h[j['author_id']] = set([])
            h[j['author_id']].add(data[i]['id_conference_int'])



###############
# 1.4 : Here we store the list of the authors' ids in a list called "nodeslist".
#We will create a graph next and then use this list as the list of the nodes.
nodeslist = list()
for i in g.keys():
    nodeslist.append(i)


###############
# 1.5 : Here we import the networkx library which we use it for creating our graph.
#Then we add the nodes from the list we defined in the previous step.
import networkx as nx
G = nx.Graph()
G.add_nodes_from(nodeslist)


###############
# 1.6: we add the edges and the wights of the edges using the
# jaccard similarity and finish producing our graph.
co_authors = list(g.values())
for i in co_authors: 
    for j in i:
        for k in j:
            for z in range(j.index(k), len(j)):
                G.add_edge(k,j[z],weight = 1 - (len(h[k] & h[j[z]])/len(h[k] | h[j[z]]))) if k != j[z] else True


# In[126]:


dijkstra(G, G.nodes()[0],G.nodes()[3])

