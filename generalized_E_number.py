import heapq

def dijkstra(graph, initial, end=None):
    '''
    Implementation of Dijkstra algorithm between two nodes
    :param graph: input graph
    :param initial: source node
    :param end: destination node
    :return: the weight of the shortest path between the source and the destination
    '''

    # we create a heap structure, through the heapq lib, in order to compute the algorithm faster
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
    #if no ending node is specified we compute the generalized dijkstra            
    if end == None:
        return visited
    else:
        #in the case that we specify the ending node we retrieve only the
#weight of the shortest path
        return visited[end]


def GroupNumber(graph, subset_of_nodes):
    '''
    In this method we calculate the group number associated to each node of the graph. This is done computing the shortest
    path between a node of the graph and every subnode of the subset (taking at the end the minimum value of the shortest path between 
    the 21 calculated)
    :param graph: input graph
    :param subset_of_nodes: group of nodes, maximum 21
    :return: dictionary -> keys: nodes in input, values: GroupNumber
    '''

    GroupNumber = {} #define a groupnumber dictionary {node: {sub_node : shortest_path)}}
    #we take all the nodes of the graph - the nodes of the subset
    
    difference_set = list(set(graph.nodes())-set(subset_of_nodes))
   
    for idx, node in enumerate(difference_set):
        #initially we set a general weight = to infinite and each time we find a lower weight
        #we substitute the previous value 
        weight = float('Inf')

        try:
            # Calculates the shortest path between the node and all the other nodes in the graph
            # We select the minimum distance from node to a node X such that X is in subset.
            all_paths = dijkstra(graph, node)
            GroupNumber[node] = min(all_paths[x] for x in subset_of_nodes)
        except:
            pass

    #we filter the result in order to delete the keys that have no value
    filtered = {}
    for i in GroupNumber:
        if GroupNumber[i] != {}:
            filtered[i] = GroupNumber[i]
    return filtered


#In order to reduce the computational cost of the GroupNumber algorithm we can do several things.
#First of all, because this is an undirected graph, we can compute just one time the shortest
#path between 2 nodes and then take same value for the reverse path.
#Secondly we can think to use a different version of the dijkstra algorithm that takes in input
#a list of nodes instead of a single one. This result in a multi-source dijkstra that assumes
#that all the nodes of the subset are already visited and assigns to them a weight cost of 0.
#Then for every subset's node we see what nodes of the graph are reachable (that are not visited
#yet). At the end we follow the path that has the lowest weight and use the single-source
#dijkstra from that node to the others.

