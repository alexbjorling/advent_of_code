import re


class Rule:
    def __init__(self, var, op, val, target):
        self.var = var
        self.op = op
        assert op in '<>'
        self.val = int(val)
        self.target = target

    def true(self, part):
        if self.op == '<':
            return getattr(part, self.var) < self.val
        else:
            return getattr(part, self.var) > self.val


class Workflow:
    def __init__(self, rules, default):
        self.rules = rules
        self.default = default

    def apply(self, part):
        for r in self.rules:
            if r.true(part):
                return r.target
        return self.default


class Part:
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def sum(self):
        return self.x + self.m + self.a + self.s

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

# unpack the parts
part_list = []
for part in parts.split():
    x = re.search('x=([0-9]+)', part).groups()[0]
    m = re.search('m=([0-9]+)', part).groups()[0]
    a = re.search('a=([0-9]+)', part).groups()[0]
    s = re.search('s=([0-9]+)', part).groups()[0]
    part_list.append(Part(x, m, a, s))

# now send the parts through the workflows and sum the accepted ones
total = 0
for p in part_list:
    wf = 'in'
    while True:
        wf = workflow_map[wf].apply(p)
        if wf == 'A':
            total += p.sum()
        if wf in 'AR':
            break

assert total == 325952
