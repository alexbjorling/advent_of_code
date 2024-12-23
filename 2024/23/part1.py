import re
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt; plt.ion()

# load the data as a dict of lists
connections = defaultdict(list)
with open("input.txt", "r") as fp:
    for line in fp:
        c1, c2 = re.findall("(.{2})-(.{2})", line)[0]
        connections[c1].append(c2)

# make a networkx graph
n = nx.Graph(connections)
plt.figure()
nx.draw(n, with_labels=True)

# for each node, find its connections pairwise and see which pairs are connected
groups = set()
for node in n:
    for n1 in n[node]:
        for n2 in n[node]:
            if n1 == n2:
                continue
            if n1 in n[n2] and "t" in (n1[0], n2[0], node[0]):
                groups.add(tuple(sorted([node, n1, n2])))

assert len(groups) == 1284