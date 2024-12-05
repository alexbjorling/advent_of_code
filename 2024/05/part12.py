# load data
with open("input.txt", "r") as fp:
    data = fp.read().split("\n\n")

    rules = []
    for r in data[0].splitlines():
        rules.append(list(map(int, r.split("|"))))

    orders = []
    for o in data[1].splitlines():
        orders.append(list(map(int, o.split(","))))


# helper to see if an order is in the right order
def order_ok(order, rules):
    for rule in rules:
        try:
            p1 = order.index(rule[0])
            p2 = order.index(rule[1])
            if not p1 < p2:
                return False
        except ValueError:
            continue
    return True


# part 1
tot = 0
bad_orders = []
for order in orders:
    if order_ok(order, rules):
        tot += order[len(order) // 2]
    else:
        bad_orders.append(order)
assert tot == 6267


# part 2: swap elements according to the rules until the whole list is ok
tot = 0
for order in bad_orders:
    while not order_ok(order, rules):
        for rule in rules:
            try:
                p1 = order.index(rule[0])
                p2 = order.index(rule[1])
                if not p1 < p2:
                    order[p1], order[p2] = order[p2], order[p1]
            except ValueError:
                # rule doesn't apply
                continue
    tot += order[len(order) // 2]
assert tot == 5184