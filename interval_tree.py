
#Procedure to check whether a point stabs an interval
def interval_intersects(point, interval):
    return interval[0] <= point and point <= interval[1]

#Procedure to check whether the interval is at the left of an endpoint
def interval_at_left(point, interval):
    return interval[1] < point

#Procedure to check whether the interval is at the right of an endpoint
def interval_at_right(point, interval):
    return point < interval[0]

#Like a takeWhile but instead returns its count
#It is an output-sensitive procedure
def count_while(array, condition):
    count = 0
    while count < len(array) and condition(array[count]): count += 1
    return count

#A node in an interval tree has 3 childs
#It also contains 2 fields to store the intersecting intervals
#the first sorted by the starting endpoint and the second one
#by its ending endpoint (hence "reversed").
class TertiaryNode:
    def __init__(self, node):
        self.node = node
        self.left = None
        self.right = None
        self.intervals = []
        self.reversed_intervals = []

################################################################################################


#This procedure builds an interval tree, it takes as input the intervals
#and a sorted list of endpoints. We exploit sortedness of endpoints to
#build a balanced interval tree.

#Complexity analysis of the procedure is right after the function
def build_interval_tree(intervals, endpoints):
    if len(intervals) == 0 or len(endpoints) == 0:
        return None
    #It takes the median
    median_index = (len(endpoints) - 1) // 2
    median = endpoints[median_index]
    #We now compute the intervals intersecting with the endpoint,
    #and the ones being at the both right and left.
    #It is crucial that these lists of intervals are disjoints
    #(ie. intersection between them must be empty)
    intervals_left = []
    intervals_right = []
    intervals_intersected = []
    #Loops over the intervals and deposits them in the appropriate sublist
    for i in intervals:
        if interval_intersects(median, i):
            intervals_intersected.append(i)
        elif interval_at_left(median, i):
            intervals_left.append(i)
        elif interval_at_right(median, i):
            intervals_right.append(i)
    #We now create the node and deposit the median.
    n = TertiaryNode(median)
    if len(intervals_intersected) > 0:
        n.intervals = sorted(intervals_intersected)
        n.reversed_intervals = sorted(intervals_intersected, key= lambda i: (-i[1], -i[0]))
    #Now we build the left and right subtrees
    n.left = build_interval_tree(intervals_left, endpoints[:median_index])
    n.right = build_interval_tree(intervals_right, endpoints[median_index + 1:])
    return n

#The above function has cost O(cost_of_computing_intersections + cost_of_sorting)
#Let I denote the intersecting intervals. The cost is then O(n + |I| * log(|I|) )
#But this is not the whole story since we have a recursive procedure.
#To give a precise complexity cost we exploit the fact that intervals are disjoint.


#Suppose that we had an interval tree with 2 nodes and N intervals.
#Let n1 denote the set of intervals stored in the first node, and n2 the one being
#in the other node. So we have that N = |n1| + |n2|

#It is easy to see that the overall complexity of our procedure is O(|n1|*log(|n1|) + |n2|*log(|n2|)).
#know that

# |n1|*log(|n1|) + |n2|*log(|n2|) = O( (|n1| + |n2|) * log(|n1| + |n2|) )

#Proving the above statement is trivial if we use the definition of Big-O which encompasses
#limits.
#http://people.csail.mit.edu/alinush/6.006-spring-2014/big-oh-with-limits.pdf

#Since in our toy example N = |n1| + |n2| we have that
# |n1|*log(|n1|) + |n2|*log(|n2|) = O( N * log N )

#I have proved that with a toy example of 2 nodes but it is easily generalizable
#Just let N = sum (n_i)

#So the total complexity is O( N log N ) with N being the number of intervals.
#The linear term is subsumed by "N log N"


################################################################################################


#The complexity of the below procedure is banally O(log N + k) since the tree is binary.
#At the same time the complexity is linear in the number of reported intervals hence the term "K"

#I wish Python supported tail-call optimization, the below code would have looked nice in a
#functional language.

def query_interval_tree(point, node, count = 0, intersects = None):
    if intersects is None:
        intersects = lambda i : interval_intersects(point, i)
    if node is None:
        return count
    elif point == node.node:
        #The node is equal to the point query hence just return the count of 
        #of the intersecting intervals
        return count + len(node.intervals)
    elif point > node.node:
        #Since we are going right we want to inspect the intervals by their rightmosts endpoints
        return query_interval_tree(point, node.right, count + count_while(node.reversed_intervals, intersects), intersects)
    else:
        #Since we are going left we want to inspect the intervals by their leftmosts endpoints
        return query_interval_tree(point, node.left, count + count_while(node.intervals, intersects), intersects)