# Interval trees

This is a Python implementation of 1-dimension interval trees which I have done for didactic purposes.
I had implemented and studied this data-structure in my undergrad, recently I came across with a problem which required this data-structure and decided to write my own implementation, it is contained in the **interval-trees.py** file.
The only query supported is counting the number of intervals stabbed by a given point.

Attached is also a sample program (**intervals.py**) that reads a file containing the intervals and another one containing the queries (give a look to the example files in the *test* folder).

In the source code you can find comments regarding the complexity analysis of the algorithm to construct a balanced interval-tree (I use a different argument to make the case compared to the one used in textbooks which is rather unintuitive in my opinion and does not please me since it looks *magic*).
I have done the same regarding the algorithm for query answering which is easier to see.