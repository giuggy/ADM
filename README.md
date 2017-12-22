# ADM_homework_4

# main.py:
We have created this file to call all the functions we have build in order to find the results for inputs. First, it creates a graph based on the json file, then it calls the "visualize_graph" function for the graph created in the previous step. Then produces the statistics for the input conference or author. 

# generator_graph.py {Exercise I}
  We need to create a graph to analyze our data. In order to do this, we have used "networkx" library to easily create a graph in which we can define edges as mutual publications and, nodes as the authors, and other information as nodes' attributes.
  We have two functions in the generator_graph.py. 
  1. visualize_graph : This function is supposed to visualize the given graph using standard methods of "networkx" and "matplotlib".
  2. generate_graph : This function is supposed to get a path to the file as input and return a graph containing the information of the given file as output. 
    in the first step, it loads the data using "json" library's load method. then creates 3 empty dictionaries as follow:
      - dic_auth : the keys will be the authors' ids, the values will be the co-authors
      - dic_conf : the keys will be the authors' ids, the values will be important attributes like, the name, etc.
      - dic_pub : the keys will be the authors' ids again, the values will be the publcations by the author.
    We have used a "for loop" to populate the dictionaries. We loop over the data and for each entry  extract conference id, title of the conference, and publication id. We created two lists , one for ids and the other for names, and using the ids list, and "try and except" populated the three dictionaries we had build in at first. 
    Then, using from_dict_of_lists method of networkx library, created a graph, called G, with dic_auth which is a dictionary of lists. 
    Then, we added the attributes to the nodes looping on the edges of our graph G. We strongly needed the attributes to calculate the Jaccard similarity of the authors which was the next step. Since this loop was around the nodes which had at least one edge, we have to also set the attributes of the isolated nodes. We found the isolated nodes with standard method of isolates in networkx library and set the attributes for those nodes for further use.
    The process of creating the graph ended with returning the graph G.
    
   
  
# Statistics {Exercise II}
  Here, we have two methods:
  
  1. stat_conference:
  There are two input for this function. One is the graph and the other is the conference with the unique string or int.
  The first step is to select the nodes that have the input conference in their attribute. With this list we extract the subgraph.
  In the end we calculate three statistics on this subgraph: degree, closeness, betweeness. the results are plotted in a unique graph. 
  
  2. stat_authors:
  This function takes three inputs. first the author, the second is "d" which represents maximum hopping distance, and the graph. If the author is a string, we find the id based on that string. If the author is an integer then we can use the integer directly. Then with the method shortest path from the author to every node, we find the dictionary of the authors for whom the distance between the author and them is less or equal than "d". 
  Finally we take the nodes in the keys of dictionary of the shortest path and create a subgraph. 
  


# Generalized Erdos Number {Exercise III}
  In the file "generalized_E_number.py", we can find two functions.
  The first one implements the dijkstra's algorithm: it returns the weight of the shortest path between two nodes in the case  that the ending node is specify; it returns, instead, all the shortest path from the starting node to the others if no ending node is specified. The time of execution that we have obtained is more or less similar to the time requested by the method of networkx.
  
  The second function implements the method of Group number. First, it calculates the shortest path between all the subset's nodes passed in input and the nodes in the graph. In the end, since we'll have different values (equal to len(subset)) of the shortest path for each node of the graph, the result is computed taking the minimum weight in the set of the shortest paths calculated previously.
  
  In conclusion we discuss about how it is possible to optimize the calculation of the Group Number, considering the property of the graph and theorizing a faster multisource dijkstra algorithm.
  
