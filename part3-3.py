
# coding: utf-8

# In[1]:


import networkx as nx
import json
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import pylab as pl


# In[36]:


url = "reduced_dblp.json"
with open(url) as jsonfile:
    data = json.load(jsonfile)
data


# In[10]:


# 1.2 We create a dictionary that holds the authors' IDs
#as the keys and the co-authors as values.

dic_auth = {}
dic_conf = {}
dic_pub = {}
j  = 0
for entry in data:
    authors = entry['authors']
    id_conf, title_conf, id_pub = entry['id_conference_int'], entry['id_conference'], entry['id_publication_int']
    ident, names = zip(*[(auth['author_id'], auth['author']) for auth in authors])
    for i in range(len(ident)):
        id_key, id_name = ident[i], names[i] 
        lst = set(ident) - {id_key}
        conf = {'author': id_name, 'id_conference': (id_conf, title_conf)}
        
        try:
            dic_auth[id_key] = dic_auth[id_key]+ lst
            dic_conf[id_key]['id_conference'].append(conf['id_conference'])
            dic_pub[id_key].append(id_pub) 
        except:
            dic_auth[id_key] = lst

            conf['id_conference'] = [conf['id_conference']]
            dic_conf[id_key] = conf
            dic_pub[id_key] = [id_pub]

G = nx.Graph()
G=nx.from_dict_of_lists(dic_auth)
nx.set_node_attributes(G, "", "author")
nx.set_node_attributes(G, 0, "id_conference_int")
nx.set_node_attributes(G, "", "id_conference")
nx.set_node_attributes(G, 0, "id_publication_int")

for u,v,d in G.edges(data=True):

    G.node[u]['author'] = dic_conf[u]['author']
    id_conf, id_conf_int = zip(*dic_conf[u]['id_conference'])
    G.node[u]["id_conference_int"] , G.node[u]["id_conference"] = list(id_conf), list(id_conf_int) 
    G.node[u]["id_publication_int"] = dic_pub[u]
    
    G.node[v]['author'] = dic_conf[v]['author']
    id_conf, id_conf_int = zip(*dic_conf[v]['id_conference'])
    G.node[v]["id_conference_int"] , G.node[v]["id_conference"] = list(id_conf), list(id_conf_int) 
    G.node[v]["id_publication_int"] = dic_pub[v]
    
    a, b = set(dic_pub[u]), set(dic_pub[v])
    d['weight'] = 1 - len(a.intersection(b)) / float(len(a.union(b)))


'''pl.figure()
nx.draw_networkx(G)
pl.show()'''


# In[62]:


G.nodes(data=True)


# In[35]:


#filter(lambda (n, d): d['id_conference_int'] == 16501, G.nodes(data=True))

G.nodes(data = True)


# In[2]:


#we create a heap structure, through the heapq lib, in order to compute the algorithm faster
import heapq

def dijkstra(graph, initial, end):
    #we create a dictionary in which we store the visited nodes
    visited = {initial: 0}
    #we create a list, initializing the starting node with weight 0
    h = [(0, initial)]
    while h:
        #we obtain through the heappop command the value of h and then is popped out of the list
        current_weight, min_node = heapq.heappop(h)
        #for each neighbour(v) of a node we go through the minimum weight path
        for v in graph[min_node]:
            weight = current_weight + graph[min_node][v]['weight']
            #if we find a shorter path using another node we update the weight
            if v not in visited or weight < visited[v]:
                visited[v] = round(weight,2)
                heapq.heappush(h, (weight, v))
    #we return the weight of the node we are interested in    
    return visited[end]


# In[3]:


#Here we check what is the running time for the dijkstra algorithm that we wrote:
aris_id = 256176

import time
t = time.time()
dijkstra(G,20405,aris_id)
print(time.time()-t)

#we can see that the running time is close to the one using the nx
t = time.time()
nx.dijkstra_path_length(G,20405,aris_id)
print(time.time()-t)


# In[12]:


#let's find 21 nodes connected to aris
aris_id = 256176
aris_connected = {}
i=0
while len(aris_connected)<21: 
    try:
        aris_connected[G.nodes()[i]] = dijkstra(G, G.nodes()[i], aris_id)
    except:
        pass
    i+=1
aris_connected
#we can now take those nodes as the set of subnodes for the computation of the groupnumber


# In[19]:


#b)takes around 4 min to compute (21 subnodes and the small dataset)

#what we do here is to calculate the group number associated to each node of the graph.
#This is done computing the shortest path between a node of the graph and every subnode of
#the subset (taking at the end the minimum value of the shortest path between the 21 calculated)
subset_of_nodes = list(aris_connected.keys())
def GroupNumber(subset_of_nodes):
    GroupNumber = {} #define a groupnumber dictionary {node: {sub_node : shortest_path)}}
    #we take all the nodes of the graph - the nodes of the subset
    for node in [item for item in G.nodes() if item not in subset_of_nodes]:
        GroupNumber[node] = {}
        #initially we set a general weight = to infinite and each time we find a lower weight
        #we substitute the previous value 
        weight = float('Inf')
        #we need a try-except statement in order to avoid the error from the nodes that are not
        #connected to aris_id
        try:
            #calculate the shortest path between node and subnode and take the min value
            for subnode in subset_of_nodes:
                #we take the minimum path
                if dijkstra(G,node,subnode) < weight:
                    GroupNumber[node].clear()
                    GroupNumber[node] = dijkstra(G,node,subnode)
                    #update the current value of the weight
                    weight = GroupNumber[node]
        except:
            pass

    #we filter the result in order to delete the keys that have no value
    filtered = {}
    for i in GroupNumber:
        if GroupNumber[i] != {}:
            filtered[i] = GroupNumber[i]
    return filtered

#to know how much time it takes:
t=time.time()
a = GroupNumber(subset_of_nodes)
print(time.time()-t)


# In[23]:


a


# In[24]:


#In order to reduce the computational cost of the GroupNumber algorithm we can do several things.
#First of all, because this is an undirected graph, we can compute just one time the shortest
#path between 2 nodes and then take same value for the reverse path.
#Secondly we can think to use a different version of the dijkstra algorithm that takes in input
#a list of nodes instead of a single one. This result in a multi-source dijkstra that assumes
#that all the nodes of the subset are already visited and assigns to them a weight cost of 0.
#Then for every subset's node we see what nodes of the graph are reachable (that are not visited
#yet). At the end we follow the path that has the lowest weight and use the single-source
#dijkstra from that node to the others.

