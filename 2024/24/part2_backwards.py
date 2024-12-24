"""
Thought I could check which output bits are wrong, then work backwards.

Won't work, all the output bits can be wrong depending on input.
"""

import re

# read nodes as dict  {name: [op, val, in1, in2]}
with open("input.txt", "r") as fp:
    one, two = fp.read().split("\n\n")
    nodes = {}

    for row in one.splitlines():
        k, v = row.split(":")
        nodes[k] = [None, int(v), None, None]

    for row in two.splitlines():
        inp1, op, inp2, outp = re.match("(.*) (AND|OR|XOR) (.*) -> (.*)", row).groups()
        nodes[outp] = [op, None, inp1, inp2]


# Return an evaluated copy of the input graph
def evaluate_graph(initial_graph):
    # copy
    nodes = {k: v.copy() for k, v in initial_graph.items()}
    # loop until done
    while None in [l[1] for l in nodes.values()]:
        for node, lst in nodes.items():
            op, val, inp1, inp2 = lst

            # already have value?
            if val is not None:
                continue

            # values on inputs?
            input_vals = nodes[inp1][1], nodes[inp2][1]
            if None not in input_vals:
                if op == "AND":
                    out = int(input_vals[0] and input_vals[1])
                elif op == "OR":
                    out = int(input_vals[0] or input_vals[1])
                elif op == "XOR":
                    out = int(input_vals[0] != input_vals[1])
                lst[1] = out
                nodes[node] = lst
    return nodes

def read_output(nodes):
    binary = '0b'
    zkeys = sorted([k for k in nodes.keys() if k.startswith("z")])[::-1]
    for zk in zkeys:
        binary += str(nodes[zk][1])
    return eval(binary)

# observation: any of the z outputs can be bad, depending on the input numbers
bad_outputs = set()
from random import randint
xs = [randint(0, 2**45-1) for i in range(20)]
ys = [randint(0, 2**45-1) for i in range(20)]
for x, y in zip(xs, ys):

    # set some input numbers at the x and y nodes, LSB first, zero padded
    xkeys = sorted([k for k in nodes.keys() if k.startswith("x")])
    xbin = "0" * 64 + bin(x)[2:]
    xbin = xbin[::-1]
    for i, k in enumerate(xkeys):
        nodes[k][1] = xbin[i]

    ybin = "0" * 64 + bin(y)[2:]
    ybin = ybin[::-1]
    ykeys = sorted([k for k in nodes.keys() if k.startswith("y")])
    for i, k in enumerate(ykeys):
        nodes[k][1] = ybin[i]

    # what should we get? LSB first, zero padded to number of z nodes
    zkeys = sorted([k for k in nodes.keys() if k.startswith("z")])
    z = x + y
    zbin = bin(z)[2:][::-1]
    zbin += "0" * (len(zkeys) - len(zbin))

    # evaluate the graph (use the copy if looping)
    nodes = evaluate_graph(nodes)

    # check the output for bad values, we get 8 incorrect z nodes right away
    should = {}
    zkeys = sorted([k for k in nodes.keys() if k.startswith("z")])  # LSB first
    for i, zk in enumerate(zkeys):
        wanted = int(zbin[i])
        if wanted != nodes[zk][1]:
            lst = nodes[zk]
            should[zk] = wanted
    print(f"{len(should)} output nodes have bad values")
    bad_outputs = bad_outputs.union(set(should.keys()))

    # traverse graph backwards, working out what we expect from the inputs
    while len(should):
        for node, wanted in should.items():
            op, _, inp1, inp2 = nodes[node]
            inval1 = nodes[inp1][1]
            inval2 = nodes[inp2][1]
            if op == "AND":
                out = int(inval1 and inval2)
            elif op == "OR":
                out = int(inval1 or inval2)
            elif op == "XOR":
                out = int(inval1 != inval2)

        break
    #        if out == wanted:

print(f"{len(bad_outputs)} unique bad outputs in total")
