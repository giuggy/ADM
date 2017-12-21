# ADM_homework_4


# Statistics {Exercise II}
  here we have two methods:
  
  1. stat_conference:
  There are two input for this function. One is the graph and the other is the conference with the unique string or int.
  The first step is to select the nodes that have the input conference in their attribute. With this list we extract the subgraph.
  In the end we calculate three statistics on this subgraph: degree, closeness, betweeness. the results are plotted in a unique graph. 
  
  2. stat_authors:
  This function takes three inputs. frist the author, the seconfd is "d" which represents maximum hopping distance, and the graph. If the author is a string, we find the id based on that string. If the author is an integer then we can use the ineger directly. Then with the method shortest path from the autho to every node, we find the dictionary of the authors for whom the distnace between the author and them is less or equal than "d". 
  Finally we take the nodes in the keys of dictionary of the shortest path and create a subgraph. 
  
