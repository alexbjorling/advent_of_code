with open('input.txt', 'r') as fp:
    line = fp.read().strip()

def hash(string):
    current = 0
    for l in string:
        current += ord(l)
        current *= 17
        current %= 256
    return current

total = 0
for string in line.split(','):
    total += hash(string)

assert total == 503487