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
net = nx.Graph(connections)
#plt.figure()
#nx.draw(net, with_labels=True)

# return the biggest group of interconnected neighbors of n
def connected_kids(node):
    sub_conns = defaultdict(list)
    for n1 in net[node]:
        for n2 in net[n1]:
            if n2 in net[node]:
                sub_conns[n1].append(n2)
    net_ = nx.Graph(sub_conns)
    return max(nx.connected_components(net_), key=len)

# find size of the biggest subset connected to node
def search(node, debt=None):
    if debt is None:
        debt = set()

    new_nodes = [k for k in connected_kids(node) if k not in debt]
    good_nodes = []  # new nodes for which all of the debt is satisfied
    #print(node, new_nodes, debt)
    debt.add(node)
    for new_node in new_nodes:
        if debt.issubset(set(net[new_node])):
            debt.add(new_node)
            good_nodes.append(new_node)
    if good_nodes:
        return search(good_nodes[0], debt)
    return debt

longest = set()
for node in net:
    test_set = search(node)
    if len(test_set) > len(longest):
        longest = test_set
    #print("***", node, )
    #print(len(search(node)))

password = ",".join(sorted(longest))
assert password == "bv,cm,dk,em,gs,jv,ml,oy,qj,ri,uo,xk,yw"
