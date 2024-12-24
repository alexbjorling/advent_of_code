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

# loop until all nodes have values
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

# get values
binary = '0b'
zkeys = sorted([k for k in nodes.keys() if k.startswith("z")])[::-1]
for zk in zkeys:
    binary += str(nodes[zk][1])
assert eval(binary) == 65635066541798