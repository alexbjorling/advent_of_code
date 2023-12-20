import re

class Module:
    low_sent = 0
    high_sent = 0

    def __init__(self, name):
        self.name = name
        self.destinations = []
        self.sources = []

    def add_destinations(self, destinations):
        self.destinations = destinations

    def add_source(self, source):
        self.sources.append(source)

    def send(self, val):
        for d in self.destinations:
            msg = 'high' if val else 'low'
            # print(f'{self.name} -{msg}-> {d.name}')
            d.recv(val, sender=self)
            if val:
                Module.high_sent += 1
            else:
                Module.low_sent += 1
        return self.destinations[:]

    def process(self):
        return []

    def recv(self, val, sender):
        pass


class FlipFlop(Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.state = False
        self.outbox = []

    def recv(self, val, sender):
        if val:
            self.outbox.append(None)
        else:
            self.state = not self.state
            self.outbox.append(self.state)

    def process(self):
        val = self.outbox.pop(0)
        if val is not None:
            return self.send(val)
        else:
            return []


class Conjunction(Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.recent = {}

    def add_source(self, source):
        super().add_source(source)
        self.recent[source] = False

    def recv(self, val, sender):
        self.recent[sender] = val
        summary = {k.name:v for k, v in self.recent.items()}

    def process(self):
        unique = set(self.recent.values())
        val = not (len(unique) == 1 and unique.pop())
        return self.send(val)


class Broadcaster(Module):
    def recv(self, val, sender):
        self.val = val

    def process(self):
        return self.send(self.val)


class Button(Module):
    def press(self):
        return self.send(False)


# parse the input
with open('input.txt', 'r') as fp:
    lines = fp.read().strip().split('\n')
data = []
for line in lines:
    module_type, name, destinations = re.match('([\%\&]*)([a-z]+).* -> (.*)', line).groups()
    destinations = [d.strip() for d in destinations.split(',')]
    data.append((module_type, name, destinations))

# pass 1: create the modules
modules = {}
for (module_type, name, destinations) in data:
    if module_type == '&':
        modules[name] = Conjunction(name)
    elif module_type == '%':
        modules[name] = FlipFlop(name)
    elif name == 'broadcaster':
        modules[name] = Broadcaster(name)

# pass 2: connect up the modules
for (module_type, name, destinations) in data:
    for d in destinations:
        if d not in modules:
            modules[d] = Module(d)
    targets = [modules[d] for d in destinations]
    modules[name].add_destinations(targets)
    for t in targets:
        t.add_source(modules[name])

# now process the network
button = Button('button')
button.destinations.append(modules['broadcaster'])

# N button presses
for i in range(1000):
    process_queue = button.press()
    while process_queue:
        m = process_queue.pop(0)  # could use a queue
        process_queue += m.process()

assert Module.high_sent * Module.low_sent == 886701120
