import networkx as nx
import matplotlib.pyplot as plt
plt.ion()

# read the data and parse as dicts
conn = {}
with open('input.txt', 'r') as fp:
    for line in fp:
        nodes_ = line.replace(':', '').split()
        conn[nodes_[0]] = nodes_[1:]

# plot a spring graph to see which three connections to remove
n = nx.Graph(conn)
plt.figure()
nx.draw(n, with_labels=True)

# it's these three
n.remove_edge('lhn', 'hcf')
n.remove_edge('dfk', 'nxk')
n.remove_edge('fpg', 'ldl')

# now we have two connected components (isolated groups),
groups = list(nx.connected_components(n))
sizes = [len(x) for x in groups]
assert sizes[0] * sizes[1] == 543564
