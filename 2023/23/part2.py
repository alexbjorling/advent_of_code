import matplotlib.pyplot as plt
plt.ion()


# read the board
board = []
with open('input.txt', 'r') as fp:
    for line in fp:
        board.append('#' + line.strip() + '#')
board.insert(0, '#' * len(board[0]))
board.append('#' * len(board[0]))
start = (1, board[1].index('.'))  # padded
goal = (len(board)-2, board[-2].index('.'))  # padded


# find nodes in the real network
nodes = []
for i in range(len(board)):
    for j in range(len(board[i])):
        if board[i][j] == '#':
            continue
        count = 0
        for vel in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if board[i + vel[0]][j + vel[1]] != '#':
                count += 1
        if count >= 3:
            nodes.append((i, j))
nodes.append(start)
nodes.append(goal)


# recursive helper to build a network from the board
def find_connections(node, excl=None, steps=0):
    # exclude current node, otherwise excl is where we came from
    if excl is None:
        excl = node
    # have we found a node?
    if node in nodes and node != excl:
        return (node, steps)
    # ok then where can we go?
    options = []
    for vel in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        new = (node[0] + vel[0], node[1] + vel[1])
        if (board[new[0]][new[1]] != '#') and (new != excl):
            options.append(new)
    if len(options) == 1:
        return find_connections(options[0], excl=node, steps=steps+1)
    else:
        return [find_connections(new, excl=node, steps=steps+1) for new in options]


# make a network of connections
connections = {n:{} for n in nodes}
todo = [(1,2)]
done = []
while todo:
    node0 = todo.pop()
    if node0 not in done:
        done.append(node0)
        cxn = find_connections(node0)
        if type(cxn) is not list:
            cxn = [cxn,]
        for tup in cxn:
            if tup is None:
                continue
            n, d = tup
            connections[node0][n] = d
            todo.append(n)


# draw it
plt.figure()
level = 0
for node in nodes:
    for dest, dist in connections[node].items():
        plt.plot([node[0], dest[0]], [node[1], dest[1]], '-')
plt.pause(.1)


# keep a list of all possible histories, including those we've finished (for later)
paths = [[start,]]
stuck = 0
done = []

# loop over all possible paths until they are either done or stuck
# the edges are one-way, but don't gain anything by testing for that (tried it)
lengths = []
while paths:
    updated_paths = []
    for p in paths:
        # filter out the connections that won't revisit any squares (and therefore not go backwards)
        options = []
        non_options = []
        for new in connections[p[-1]].keys():
            if not new in p:
                options.append(new)
        # spawn new paths for all the valid options
        for opt in options:
            if opt == goal:
                done.append(p + [opt,])
            else:
                updated_paths.append(p + [opt,])  # copy
        # if we're stuck, increment a counter and move on
        else:
            stuck += 1
            continue

    paths = updated_paths

    tot = len(paths) + stuck + len(done)
    print(f'{tot: 10d} total paths, of which {len(paths): 8d} ({len(paths)/tot*100:.1f}%) active')

# go through the ones which got to the goal, measure their lengths and pick the longest
distances = []
for p in done:
    dist = 0
    for i in range(len(p)-1):
        dist += connections[p[i]][p[i+1]]
    distances.append(dist)

assert max(distances) == 6466
