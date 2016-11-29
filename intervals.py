from itertools import groupby
from functools import partial
import sys

from interval_tree import build_interval_tree, query_interval_tree

intervals = []
endpoints = []

filename = sys.argv[1]

for line in open(filename):
    (a, b) = line.split()
    (a, b) = (int(a), int(b))
    intervals.append((a,b))
    endpoints.append(a)
    endpoints.append(b)

endpoints = [key for key, _ in groupby(sorted(endpoints))]

tree = build_interval_tree(intervals, endpoints)

with sys.stdin as f:
    for line in f.readlines():
        query = int(line)
        print(query_interval_tree(query, tree))