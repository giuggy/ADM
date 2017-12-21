# ADM_homework_4

# generator_graph.py {Exercise I}
  We need to ceate a graph to analyze our data. In order to do this, we have used "networkx" library to easily create a graph in which we can define edges as mutual pulications and, nodes as the authors, and other information as nodes' attributes.
  We have two functions in the generator_graph.py. 
  1. visualize_graph : This function is supposed to visualize the given graph using standard methods of "networkx" and "matplotlib".
  2. generate_graph : This function is supposed to get a path to the file as input and return a graph containing the information of the given file as output. 
    in the first step, it loads the data using "json" library's load method. then creates 3 empty dictionaries as follow:
      -- dic_auth : the keys will be the authors' ids, the values will be the co-authors
      -- dic_conf : the keys will be the authors' ids, the values will be important attributes like, the name, etc.
      -- dic_pub : the keys will be the authors' ids again, the values will be the pulcations by the author.
    
   
  
# Statistics {Exercise II}
  here we have two methods:
  
  1. stat_conference:
  There are two input for this function. One is the graph and the other is the conference with the unique string or int.
  The first step is to select the nodes that have the input conference in their attribute. With this list we extract the subgraph.
  In the end we calculate three statistics on this subgraph: degree, closeness, betweeness. the results are plotted in a unique graph. 
  
  2. stat_authors:
  This function takes three inputs. frist the author, the seconfd is "d" which represents maximum hopping distance, and the graph. If the author is a string, we find the id based on that string. If the author is an integer then we can use the ineger directly. Then with the method shortest path from the autho to every node, we find the dictionary of the authors for whom the distnace between the author and them is less or equal than "d". 
  Finally we take the nodes in the keys of dictionary of the shortest path and create a subgraph. 
  
