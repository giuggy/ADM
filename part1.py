### Part 1: Building up the Graph


#############
# 1.1 : The first step to build the graph is to read the data from the json file;
# Therefor we import the "json" library and then
#define the URL to the file and read the data to a variable;
#The variable is called "data" in our code.

# takes almost 20 sec for the full data
import json
url = "C:/Users/Mohammad/Desktop/ADM/homework/4/reduced_dblp.json"
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



