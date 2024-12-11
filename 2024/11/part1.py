# load the data
with open("input.txt", "r") as fp:
    data = [int(c) for c in fp.read().strip().split()]

for i in range(30):
    print(len(data),',')
    new_data = []
    for s in data:
        if s == 0:
            new_data.append(1)
        elif len(str(s)) % 2 == 0:
            half = len(str(s)) // 2
            new_data.append(int(str(s)[:half]))
            new_data.append(int(str(s)[half:]))
        else:
            new_data.append(2024 * s)
    data = new_data.copy()

assert len(new_data) == 239714
