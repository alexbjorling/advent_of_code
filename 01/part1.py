with open('input.txt', 'r') as fp:
    total = 0
    for line in fp:
        # get first
        s = ''
        for char in line:
            if char in '1234567890':
                s += char
                break
        for char in line[::-1]:
            if char in '1234567890':
                s += char
                break
        total += int(s)
print(total)