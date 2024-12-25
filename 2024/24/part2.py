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


# Read the z bits and put them together to an integer
def read_output(nodes):
    binary = '0b'
    zkeys = sorted([k for k in nodes.keys() if k.startswith("z")])[::-1]
    for zk in zkeys:
        binary += str(nodes[zk][1])
    return eval(binary)


# Search for bad bits
for bit in range(45):
    x = 2**bit
    y = 0

    # set some input numbers at the x and y nodes, LSB first, zero padded
    xkeys = sorted([k for k in nodes.keys() if k.startswith("x")])
    xbin = "0" * 64 + bin(x)[2:]
    xbin = xbin[::-1]
    for i, k in enumerate(xkeys):
        nodes[k][1] = int(xbin[i])

    ybin = "0" * 64 + bin(y)[2:]
    ybin = ybin[::-1]
    ykeys = sorted([k for k in nodes.keys() if k.startswith("y")])
    for i, k in enumerate(ykeys):
        nodes[k][1] = int(ybin[i])

    new_nodes = evaluate_graph(nodes)
    z = read_output(new_nodes)
    if x + y != z:
        print(f"incorrect answer for bit {bit}: {x} + {y} != {z}")


# At this point, it was clear that a single 1 at input bits 12, 29, 33, or 37
# gave bad addition. I drew the circuits for those bits and compared them to
# the diagram for input bit 1, and easily saw which outputs were swapped.
swapped = ["z12", "fgc", "mtj", "z29", "dgr", "vvm", "z37", "dtv"]
ans = ','.join(sorted(swapped))
print(ans)
assert ans == "dgr,dtv,fgc,mtj,vvm,z12,z29,z37"
