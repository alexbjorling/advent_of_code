"""
Like part1, but deals not with specific Part objects but instead with Set
objects, which are combined ranges of Parts.
"""

import re


class Rule:
    def __init__(self, var, op, val, target):
        self.var = var
        self.op = op
        assert op in '<>'
        self.val = int(val)
        self.target = target

    def apply(self, input_set):
        # apply this rule to a Set object, return {set: result} as the rule might split a set.
        # result can be None (if nothing has been applied) or the name of a new workflow, or
        # R/A
        results = {}

        input_rng = getattr(input_set, self.var)
        applies_completely = (
            ((self.op == '<') and (input_rng[0] < self.val and input_rng[1] < self.val))
            or ((self.op == '>') and (input_rng[0] > self.val and input_rng[1] > self.val))
        )
        doesnt_apply = (
            ((self.op == '<') and (input_rng[0] >= self.val and input_rng[1] >= self.val))
            or ((self.op == '>') and (input_rng[0] <= self.val and input_rng[1] <= self.val))
        )

        if applies_completely:
            results[input_set] = self.target
        elif doesnt_apply:
            results[input_set] = None
        else:
            split_at = (self.val if self.op == '<' else self.val + 1 )
            s1, s2 = input_set.split(self.var, split_at)
            if self.op == '<':
                results[s1] = self.target
                results[s2] = None
            elif self.op == '>':
                results[s1] = None
                results[s2] = self.target

        return results


class Workflow:
    def __init__(self, rules, default):
        self.rules = rules
        self.default = default


class Set:
    """
    Represents a set of inclusve x- m- a- and s-ranges.
    """
    def __init__(self, x, m, a, s):
        self.x = x  # 2-tuples
        self.m = m
        self.a = a
        self.s = s
        self.size()  # to make sure the input is ok

    def size(self):
        prod = 1
        for rng in (self.x, self.m, self.a, self.s):
            prod *= (rng[1] - rng[0] + 1)  # inclusive
        return prod

    def split(self, var, pos):
        # return two ranges, where the 'var' property is split so that the second start at pos
        c1, c2 = Set(self.x, self.m, self.a, self.s), Set(self.x, self.m, self.a, self.s)
        old = self.__getattribute__(var)
        setattr(c1, var, (old[0], pos-1))
        setattr(c2, var, (pos, old[1]))
        return c1, c2


# load data
with open('input.txt', 'r') as fp:
    workflows, parts = fp.read().split('\n\n')

# unpack the workflows
workflow_map = {}
for w in workflows.split():
    rule_list = []
    name, rules = re.match('(.+)\{(.+)\}', w).groups()
    for r in rules.split(',')[:-1]:
        var, op, val, target = re.match('([xmas])(.)([0-9]+):(.+)', r).groups()
        rule_list.append(Rule(var, op, val, target))
    default = rules.split(',')[-1]
    workflow_map[name] = Workflow(rule_list, default)

# recursively sum up the accepted ranges
def evaluate(input_set, workflow_map, wf='in', rule=0):
    workflow =workflow_map[wf]
    if rule == len(workflow.rules):
        # we've come to the end of this workflow
        if workflow.default in workflow_map:
            return evaluate(input_set, workflow_map, workflow.default, rule=0)
        else:
            return input_set.size() if workflow.default == 'A' else 0
    accepted = 0
    # we have one or two subsets now, go over them
    for st, res in workflow.rules[rule].apply(input_set).items():
        if res == 'A':
            accepted += st.size()
        elif res == 'R':
            # reject the whole thing
            continue
        elif res is None:
            # no new target, evaluate the next rule
            accepted += evaluate(st, workflow_map, wf, rule+1)
        else:
            # new target, go to that workflow
            accepted += evaluate(st, workflow_map, res, rule=0)
    return accepted

starting_set = Set(*((1, 4000),)*4)
assert evaluate(starting_set, workflow_map) == 125744206494820
